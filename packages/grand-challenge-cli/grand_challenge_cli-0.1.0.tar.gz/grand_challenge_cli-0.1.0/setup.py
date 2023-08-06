# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['grand_challenge_cli']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'grand-challenge-cli',
    'version': '0.1.0',
    'description': 'Command Line Interface for Grand Challenge',
    'long_description': '# rse-grand-challenge-cli\nCommand Line Interface for Grand Challenge\n',
    'author': 'James Meakin',
    'author_email': '12661555+jmsmkn@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
