# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lakefuse']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'lakefuse',
    'version': '0.0.0',
    'description': '',
    'long_description': '',
    'author': 'anthonyp',
    'author_email': 'anthony.potappel@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
