from llama_index import PromptHelper, SimpleWebPageReader, GPTSimpleVectorIndex, GPTListIndex, GPTTreeIndex
import os
import requests
import uuid
import json
import base64
from pathlib import Path
from llama_index import download_loader
from llama_index.readers.file.tabular_parser import CSVParser
from langchain.agents import initialize_agent, Tool
from langchain import OpenAI
from llama_index import Document
from langchain import PromptTemplate
import re
from langchain.chains import LLMChain
import asyncio
import pandas as pd
import fuzzywuzzy
from fuzzywuzzy import process
import numpy as np
from berri_ai.agents.DataAnalysisPrompt import PANDAS_CHAIN_DEFAULT_PROMPT
from berri_ai.search_strategies.bm25.DocStore_CSV import DocStore
from berri_ai.ComplexInformationQA import ComplexInformationQA
import os

os.environ[
  "OPENAI_API_KEY"] = "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"


class DataAnalysisQA:

  def __init__(self,
               df,
               openai_api_key,
               additional_functions=None,
               additional_descriptions=None):
    self.df = df
    self.openai_api_key = openai_api_key
    if additional_functions != None and additional_descriptions != None and len(
        additional_functions) == len(additional_descriptions):
      self.additional_functions = additional_functions
      self.additional_descriptions = additional_descriptions
    self.unique_values = []
    for column in self.df.columns:
      unique_val = self.df[column].unique().ravel()
      self.unique_values.extend(unique_val)

  def likely_col(self, keywords):
    output = ""
    if len(keywords) > 1:
      output += ". These are the keywords from the user's query: " + ' '.join(
        keywords)
    unique_values = []
    for column in self.df.columns:
      unique_val = self.df[column].unique().ravel()
      unique_values.extend(unique_val)
    no_col = True
    for keyword in keywords:
      potential_val_cols = []
      scores = process.extract(keyword, unique_values)
      scores = set(x for x in scores if x[1] > 90)
      if len(scores) > 0:
        for score in scores:
          # get all the potential columns this value could belong to
          for col in self.df.columns:
            if self.df[col].isin([score[0]]).any():
              potential_val_cols.append((score[0], col))
      print(potential_val_cols)
      if len(potential_val_cols) > 0:
        output_str = ". When the user says " + keyword + ' , they are most likely referring to one of these values / inside these columns: '
        print(scores)
        for idx, potential_val_col in enumerate(potential_val_cols):
          output_str += '. Value ' + str(idx) + ': ' + str(
            potential_val_col[0]) + ' Column ' + str(idx) + ': ' + str(
              potential_val_col[1])
        output += output_str
        no_col = False
    if no_col:
      output = ""
    return output

  def keyword_extractor(self, query_str):
    llm = OpenAI(temperature=0.7)
    prefix = """A user is asking questions about a spreadsheet. Extract the keywords from the user query that might make sense as names of columns or values in a spreadsheet. If you are not certain, say 'I am not certain', do not make things up. If there are multiple keywords, separate them with a comma (,).
    \n
    User Query: Top cat5 by YoY
    Keywords: cat5, YoY 
    \n
    User Query: How many sku's do we have for variant handles?
    Keywords: sku, variant handle 
    \n
    User Query: Top cat5 by YoY that is very low competition
    Keywords: cat5, YoY, very low competition
    \n
    User Query: """
    input = prefix + query_str
    input += "\n Keywords: "
    return llm(input)

  def check_if_col_or_not_v_2(self, user_query):
    # use llm to get keywords
    keywords = self.keyword_extractor(user_query)
    keywords = keywords.split(",")
    updated_query = user_query
    # use fuzzy match to compare keyword in keywords to column names and see if there's a likely match
    values = []
    for keyword in keywords:
      # List of tuples containing the similarity score and the string
      scores = process.extract(keyword, self.df.columns.unique().ravel())

      # Sort the list of tuples by similarity score
      sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
      if int(
          sorted_scores[0][1]
      ) < 85:  # if the keyword match is below 85/100, then it's probably a value inside a column, and not a column name.
        values.append(keyword.strip())
      elif int(sorted_scores[0][1]) >= 90:
        updated_query += '. When the user says ' + keyword + ' they are most likely referring to this column: ' + sorted_scores[
          0][0] + '.'
      print("sorted_scores: ", sorted_scores)
    return updated_query, values

  def sanity_checker(self, user_intent, pandas_expression):
    prompt_template = """
      You are an AI assistant, helping a user formulate pandas expressions based on their queries about the data. Ensure the given pandas expression is a valid pandas expression and aligns with the user's intent. If 'Initial Pandas Expression' aligns to 'User Intent' and is a valid pandas expression, simply output the same in 'Final Pandas Expression', do not change anything.
    
      Format: 
      User Intent: The question the user is trying to ask about their data. 
      Initial Pandas Expression: An initial approach to answering this question, expressed in pandas. 
      Thought: Think if the initial pandas expression expresses the user's intent correctly.
      Final Pandas Expression: If you think the initial pandas expression expression correctly, output the same as Initial Pandas Expression. Else re-write expression to better express the user's intent.
    
      User Intent: {user_intent}
    
      Initial Pandas Expression: {initial_pandas_expression}
    
      Thought: 
      """
    prompt = PromptTemplate(
      input_variables=["user_intent", "initial_pandas_expression"],
      template=prompt_template)
    formatted_prompt = prompt.format(
      user_intent=user_intent, initial_pandas_expression=pandas_expression)
    llm = OpenAI(temperature=0.7, best_of=3)
    pd_output = llm(formatted_prompt)
    return pd_output

  def pandas_chain(self, user_query, sheet_col_names):
    prompt_template = """
      You are an AI assistant, helping a user formulate pandas expressions based on their queries about the data. The data has been loaded into a pandas dataframe called 'df'. 
    
    Here are your instructions: 
    1. For a user's question, explain what you think the user is trying to achieve and write a pandas expression to answer their question. 
    2. In cases where a user is asking about a value contained inside a column, you will receive both the column name and the value in the column it is equal to. Do not rewrite it or spell it differently. This will cause your query expression to break
    3. When writing the pandas expression, assume the dataframe is called 'df'. Do not call it anything else.
    4. Output the value of the pandas expression as a string and do not return the row index (.to_string(index=False))
    5. Use Sanity Check to check if the answer is very long (e.g. the entire column). If so, rewrite your expression to only return the head(). 
    6. If you are uncertain what the user is asking, say "Hmm, I'm not sure". Do not make things up.
    
    Given these column names: brands_boolean	cat1	cat2	cat3	cat4	cat5	Search Volume	YoY	absolute growth	cluster	cluster_proba	monthly Search Volume	monthly absolute growth	MoM	YoY 1 month absolute growth	YoY 1 month	YoY 24 month absolute growth	YoY 24 month	arrow_YoY	pred_YoY	pred_confidence	pred_YoY_score	cat_ranking	top_affinity_group	top_brands	image	description	filter_cluster	filter_trends_curve	in_out	Search Volume score	Search Volume score_label	pred_YoY score_label	brands Volume	brand count	brands Volume score	brands Volume score_label	concentration score	concentration score_label
    
    Write a pandas expression that answers this query: top cat5 by Search Volume
    
    What do you think the user intent here is? Think step-by-step.
    
    I think the user is trying to find the top category 5 (cat5) items by Search Volume. We can use the `pandas.DataFrame.sort_values()` method to sort the dataframe by the 'Search Volume' column in descending order.
    
    Initial Pandas Expression: df.sort_values('Search Volume', ascending=False)['cat5'].to_string(index=False)
    
    
    Given these column names: brands_boolean	cat1	cat2	cat3	cat4	cat5	Search Volume	YoY	absolute growth	cluster	cluster_proba	monthly Search Volume	monthly absolute growth	MoM	YoY 1 month absolute growth	YoY 1 month	YoY 24 month absolute growth	YoY 24 month	arrow_YoY	pred_YoY	pred_confidence	pred_YoY_score	cat_ranking	top_affinity_group	top_brands	image	description	filter_cluster	filter_trends_curve	in_out	Search Volume score	Search Volume score_label	pred_YoY score_label	brands Volume	brand count	brands Volume score	brands Volume score_label	concentration score	concentration score_label
    
    Write a pandas expression that answers this query: top cat5 by YoY
    
    
    What do you think the user intent here is? Think step-by-step. It seems like the user is asking for the top values of cat5 by the YoY column.
    
    Initial Pandas Expression: df.sort_values(by='YoY', ascending=False).head(1)['cat5'].to_string(index=False)
    
    
    Given these column names: brands_boolean	cat1	cat2	cat3	cat4	cat5	Search Volume	YoY	absolute growth	cluster	cluster_proba	monthly Search Volume	monthly absolute growth	MoM	YoY 1 month absolute growth	YoY 1 month	YoY 24 month absolute growth	YoY 24 month	arrow_YoY	pred_YoY	pred_confidence	pred_YoY_score	cat_ranking	top_affinity_group	top_brands	image	description	filter_cluster	filter_trends_curve	in_out	Search Volume score	Search Volume score_label	pred_YoY score_label	brands Volume	brand count	brands Volume score	brands Volume score_label	concentration score	concentration score_label
    
    Write a pandas expression that answers this query: brands searched alongside hair serum?.When the user says hair serum. It is equal to the 'hair serum' value in the cat5 column.
    
    What do you think the user intent here is? Think step-by-step. I think the user is trying to find the top brands searched alongside hair serum. We can use the `pandas.DataFrame.loc[]` method to filter the dataframe to only rows where the 'cat3' column is equal to 'hair serum'. Then we can use the `pandas.DataFrame.sort_values()` method to sort the dataframe by the 'Search Volume' column in descending order.
    
    Initial Pandas Expression: df.loc[df['cat3'] == 'hair serum'].sort_values('Search Volume', ascending=False)['top_brands'].head().to_string(index=False)
    
    Given these column names: {sheet_col_names}
    
    Write a pandas expression that answers this query: {user_query}
    
    What do you think the user intent here is? Think step-by-step.
      """
    prompt = PromptTemplate(input_variables=["sheet_col_names", "user_query"],
                            template=prompt_template)

    formatted_prompt = prompt.format(sheet_col_names=sheet_col_names,
                                     user_query=user_query)
    llm = OpenAI(temperature=0.7, best_of=3)
    pd_output = llm(formatted_prompt)
    return pd_output

  def conditional_search(self, query):
    sheet_col_names = ", ".join([col for col in self.df.columns])
    pd_output = self.pandas_chain(user_query=query,
                                  sheet_col_names=sheet_col_names)
    # extract pandas expression
    if "Initial Pandas Expression" in pd_output:
      # run eval
      print(pd_output)
      pandas_expression = pd_output.split(
        "Initial Pandas Expression:")[1].strip()
      final_pd_output = self.sanity_checker(query, pandas_expression)
      print(final_pd_output)
      pandas_expression = final_pd_output.split(
        "Final Pandas Expression:")[1].strip()
      match = re.search("(?:`)?df(.*)", pandas_expression).group(1)
      if match:
        match = match.replace("df", "self.df")
        df_expression = "self.df" + match
        print("df_expression: ", df_expression)
        value = eval(df_expression)
        return (value,
                pd_output + "\n Post Sanity Checker: " + final_pd_output)
      else:
        return pd_output
    else:
      return pd_output

  def query(self, user_input: str):

    # check if column or not
    user_input, values = self.check_if_col_or_not_v_2(user_input)
    print(values)
    likely_columns = ""
    if len(values) > 0:
      likely_columns = self.likely_col(values)
      print("likely columns: ", likely_columns)
    # pass in query + context into conditional search and get answer
    final_input_str = user_input + "." + likely_columns
    print("final_input_str: ", final_input_str)
    output = self.conditional_search(final_input_str)
    if len(output) == 2:
      response = output[0]
      references = "I think the keywords mentioned were: " + ",".join(values) + ". And my final input into the pandas expression model was: " + final_input_str + ". And this is what the model came up with: " + output[1]
      return {"response": response, "references": references}
    return {"response": "I am not certain, could you rephrase that?", "references": "I checked if your question had keywords that either belonged to a column or could possibly be a value in the spreadsheet"}