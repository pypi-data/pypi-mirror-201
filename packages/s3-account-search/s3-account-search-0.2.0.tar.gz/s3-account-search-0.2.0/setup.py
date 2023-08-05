# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['s3_account_search']

package_data = \
{'': ['*']}

install_requires = \
['aws-assume-role-lib>=1.3.0,<2.0.0', 'boto3>=1.16.49,<2.0.0']

entry_points = \
{'console_scripts': ['s3-account-finder = s3_account_search.cli:run',
                     's3-account-search = s3_account_search.cli:run']}

setup_kwargs = {
    'name': 's3-account-search',
    'version': '0.2.0',
    'description': 'Search for the AWS Account that contains an S3 bucket or object',
    'long_description': None,
    'author': 'Ben Bridts',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
