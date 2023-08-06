# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nerpii']

package_data = \
{'': ['*']}

install_requires = \
['faker>=17.3.0,<18.0.0',
 'gender-guesser>=0.4.0,<0.5.0',
 'pandas>=1.5.3,<2.0.0',
 'presidio-analyzer>=2.2.32,<3.0.0',
 'simple-colors>=0.1.5,<0.2.0',
 'spacy>=3.5.0,<4.0.0',
 'torch>=1.13.1,<2.0.0',
 'transformers>=4.26.1,<5.0.0']

setup_kwargs = {
    'name': 'nerpii',
    'version': '0.1.4',
    'description': 'A python library to perform NER on structured data and generate PII with Faker',
    'long_description': "# Nerpii \nNerpii is a Python library developed to perform Named Entity Recognition (NER) on structured datasets and synthesize Personal Identifiable Information (PII).\n\nNER is performed with [Presidio](https://github.com/microsoft/presidio) and with a [NLP model](https://huggingface.co/dslim/bert-base-NER) available on HuggingFace, while the PII generation is based on [Faker](https://faker.readthedocs.io/en/master/).\n\n## Installation\nYou can install Nerpii by using pip: \n\n```python\npip install nerpii\n```\n## Quickstart\n### Named Entity Recognition\nYou can import the NamedEntityRecognizer using\n```python\nfrom nerpii.named_entity_recognizer import NamedEntityRecognizer\n```\nYou can create a recognizer passing as parameter a path to a csv file or a Pandas Dataframe\n\n```python\nrecognizer = NamedEntityRecognizer('./csv_path.csv')\n```\nPlease note that if there are columns in the dataset containing names of people consisting of first and last names (e.g. John Smith), before creating a recognizer, it is necessary to split the name into two different columns called <strong>first_name</strong> and <strong>last_name</strong> using the function `split_name()`.\n\n```python\nfrom nerpii.named_entity_recognizer import split_name\n\ndf = split_name('./csv_path.csv', name_of_column_to_split)\n```\nThe NamedEntityRecognizer class contains three methods to perform NER on a dataset:\n\n```python\nrecognizer.assign_entities_with_presidio()\n```\nwhich assigns Presidio entities, listed [here](https://microsoft.github.io/presidio/supported_entities/)\n\n```python\nrecognizer.assign_entities_manually()\n```\nwhich assigns manually ZIPCODE and CREDIT_CARD_NUMBER entities \n\n```python\nrecognizer.assign_organization_entity_with_model()\n```\nwhich assigns ORGANIZATION entity using a [NLP model](https://huggingface.co/dslim/bert-base-NER) available on HuggingFace.\n\nTo perform NER, you have to run these three methods sequentially, as reported below:\n\n```python\nrecognizer.assign_entities_with_presidio()\nrecognizer.assign_entities_manually()\nrecognizer.assign_organization_entity_with_model()\n```\n\nThe final output is a dictionary in which column names are given as keys and assigned entities and a confidence score as values.\n\nThis dictionary can be accessed using\n\n```python\nrecognizer.dict_global_entities\n```\n\n### PII generation \n\nAfter performing NER on a dataset, you can generate new PII using Faker. \n\nYou can import the FakerGenerator using \n\n```python\nfrom nerpii.faker_generator import FakerGenerator\n```\n\nYou can create a generator using\n\n```python\ngenerator = FakerGenerator(dataset, recognizer.dict_global_entities)\n```\nTo generate new PII you can run\n\n```python\ngenerator.get_faker_generation()\n```\nThe method above can generate the following PII:\n* address\n* phone number\n* email naddress\n* first name\n* last name\n* city\n* state\n* url\n* zipcode\n* credit card\n* ssn\n* country\n\n## Examples\n\nYou can find a notebook example in the [notebook](https://github.com/Clearbox-AI/nerpii/tree/main/notebooks) folder. \n\n\n",
    'author': 'Clearbox AI',
    'author_email': 'info@clearbox.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Clearbox-AI/nerpii',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
