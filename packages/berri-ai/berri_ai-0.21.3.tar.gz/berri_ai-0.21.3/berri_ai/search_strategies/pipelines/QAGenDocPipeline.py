import asyncio
from langchain import OpenAI, LLMChain, PromptTemplate
import asyncio
from llama_index import Document
from time import time
from typing import Any, List, Optional, Tuple, Union
from langchain.text_splitter import RecursiveCharacterTextSplitter
class QAGenDocPipeline:
    """A simple example class"""
    text_splitter = RecursiveCharacterTextSplitter(# Set a really small chunk size, just to show.
            chunk_size = 750,
            chunk_overlap  = 200,
            length_function = len)
    
    def __init__(self, openai_api_key: str, documents: List[Document]):
      self.openai_api_key = openai_api_key
      self.documents = documents 
      self.chunks, self.references = self.chunk_and_ref_creator()
    
    def chunk_and_ref_creator(self):
      # iterate through the GPT-Index documents 
      texts = []
      references = []
      for doc in self.documents:
        # get the text
        text = doc.text
        # run them through a textsplitter 
        chunks = self.text_splitter.split_text(text)
        # return a list of text + doc_id's 
        texts.extend(chunks)
        references.extend(doc.doc_id*len(chunks))
      return texts, references

    async def async_generate(self, chain, chunk):
      resp = await chain.arun(chunk=chunk)
      print(resp)
      return resp

    async def qa_generate_concurrently(self, openai_api_key, chunks, references, prompt=None):
      import os
      os.environ["OPENAI_API_KEY"] = openai_api_key
      if prompt == None: 
        prompt = "You're an AI assistant to customer support agents. Generate the 5 most likely questions a customer might ask for this given piece of context from a company's documentation: "
      llm = OpenAI(temperature=0.7)
      prompt = PromptTemplate(
          input_variables=["chunk"],
          template= prompt + "{chunk}",
      )
      chain = LLMChain(llm=llm, prompt=prompt)
      results = []
      print(len(chunks))
      if len(chunks) > 100: 
        # batch token limit is 250,000
        chunks = [chunks[i:i+100] for i in range(0, len(chunks), 100)] #chunk in batches of 200 -> each chunk is of size ~1k tokens
        for chunk_idx, chunk in enumerate(chunks): 
          tasks = [self.async_generate(chain, c) for c in chunk]
          result = await asyncio.gather(*tasks)
          results += [Document(c, doc_id = references[idx*chunk_idx])  for idx, c in enumerate(chunk)]
          time.sleep(5)
      else: 
        tasks = [self.async_generate(chain, chunk) for chunk in chunks]
        results = await asyncio.gather(*tasks)
        results = [Document(c, doc_id = references[idx])  for idx, c in enumerate(chunks)]
      return results
    
    
    def run(self):
      return asyncio.run(self.qa_generate_concurrently(self.openai_api_key, self.chunks, self.references))