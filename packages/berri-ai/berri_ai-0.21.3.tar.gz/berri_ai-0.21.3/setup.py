# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['berri_ai',
 'berri_ai.agents',
 'berri_ai.search_strategies.bm25',
 'berri_ai.search_strategies.pipelines']

package_data = \
{'': ['*']}

install_requires = \
['fuzzywuzzy>=0.18.0,<0.19.0',
 'html2text>=2020.1.16,<2021.0.0',
 'llama-index==0.4.34',
 'mixpanel>=4.10.0,<5.0.0',
 'nltk>=3.8.1,<4.0.0',
 'numpy>=1.18,<2.0',
 'openai>=0.27.2,<0.28.0',
 'pipreqs>=0.4.11,<0.5.0',
 'rank-bm25>=0.2.2,<0.3.0',
 'requests>=2.28.2,<3.0.0',
 'tiktoken>=0.2.0,<0.3.0',
 'tqdm>=4.64.1,<5.0.0']

setup_kwargs = {
    'name': 'berri-ai',
    'version': '0.21.3',
    'description': '',
    'long_description': None,
    'author': 'Team Berri',
    'author_email': 'clerkieai@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<4.0.0',
}


setup(**setup_kwargs)
