# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['neofuzz']

package_data = \
{'': ['*']}

install_requires = \
['pynndescent>=0.5.0,<0.6.0', 'scikit-learn>=1.1.0,<1.3.0']

setup_kwargs = {
    'name': 'neofuzz',
    'version': '0.1.2',
    'description': 'Blazing fast fuzzy text search for Python.',
    'long_description': '# neofuzz\n\nBlazing fast fuzzy text search for Python.\n\n## Introduction\n\nneofuzz is a fuzzy search library based on vectorization and approximate nearest neighbour\nsearch techniques.\n\nWhat neofuzz is good at:\n  - Hella Fast.\n  - Repeated searches in the same space of options.\n  - Compatibility with already existing TheFuzz code.\n  - Incredible flexibility in the vectorization process.\n  - Complete control over the nearest neighbour algorithm\'s speed and accuracy.\n\nIf you\'re looking for a scalable solution for searching the same, large dataset\nwith lower quality of results but incredible speed, neofuzz is the thing you\'re looking for.\n\nWhat neofuzz is not good at:\n  - Exact and certainly correct results.\n  - Searching different databases in succession.\n  - Not the best fuzzy search algorithm.\n\nIf you\'re looking for a library that\'s great for fuzzy searching small amount of data with a\ngood fuzzy algorithm like levenshtein or hamming distance, neofuzz is probably not\nthe thing for you.\n\n## Usage\n\nYou can install neofuzz from PyPI:\n\n```bash\npip install neofuzz\n```\n\nThe base abstraction of neofuzz is the `Process`, which is a class aimed at replicating TheFuzz\'s API.\n\nA `Process` takes a vectorizer, that turns strings into vectorized form, and different parameters\nfor fine-tuning the indexing process.\n\nIf you want a plug-and play experience you can create a generally good quick and dirty\nprocess with the `char_ngram_process()` process.\n\n```python\nfrom neofuzz import char_ngram_process\n\n# We create a process that takes character 1 to 5-grams as features for\n# vectorization and uses a tf-idf weighting scheme.\n# We will use cosine distance for the nearest neighbour search.\nprocess = char_ngram_process(ngram_range=(1,5), metrics="cosine", tf_idf=True)\n\n# We index the options that we are going to search in\nprocess.index(options)\n\n# Then we can extract the ten most similar items the same way as in\n# thefuzz\nprocess.extract("fuzz", limit=10)\n---------------------------------\n[(\'fuzzer\', 67),\n (\'Januzzi\', 30),\n (\'Figliuzzi\', 25),\n (\'Fun\', 20),\n (\'Erika_Petruzzi\', 20),\n (\'zu\', 20),\n (\'Zo\', 18),\n (\'blog_BuzzMachine\', 18),\n (\'LW_Todd_Bertuzzi\', 18),\n (\'OFU\', 17)]\n```\n\nIf you want to use a custom vectorization process with dimentionality reduction for example,\nyou are more than free to do so by creating your own custom `Process`\n\n```python\nfrom neofuzz import Process\n\nfrom sklearn.decomposition import NMF\nfrom sklearn.feature_extraction.text import TfidfVectorizer\nfrom sklearn.pipeline import make_pipeline\n\n# Let\'s say we have a list of sentences instead of words,\n# Then we can use token ngrams as features\ntf_idf = TfidfVectorizer(analyzer="word", stop_words="english", ngram_range=(1,3))\n# We use NMF for reducing the dimensionality of the vectors to 20\n# This could improve speed but takes more time to set up the index\nnmf = NMF(n_components=20)\n\n# Our vectorizer is going to be a pipeline\nvectorizer = make_pipeline(tf_idf, nmf)\n\n# We create a process and index it with our corpus.\nprocess = Process(vectorizer, metric="cosine")\nprocess.index(sentences)\n\n# Then you can extract results\nprocess.extract("she ate the cat", limit=3)\n-------------------------------------------\n[(\'She ate the Apple.\', 65),\n (\'The dog at the cat.\', 42),\n (\'She loves that cat\', 30)]\n```\n\n## Documentation\nTODO\n',
    'author': 'Márton Kardos',
    'author_email': 'power.up1163@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
