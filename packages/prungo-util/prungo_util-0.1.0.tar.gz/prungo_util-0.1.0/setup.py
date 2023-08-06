# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['prungo_util']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'prungo-util',
    'version': '0.1.0',
    'description': 'A package for basic utility functions/classes',
    'long_description': '# prungo-util\nutility package for importing into projects\n',
    'author': 'c-prungo',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/c-prungo/prungo-util',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
