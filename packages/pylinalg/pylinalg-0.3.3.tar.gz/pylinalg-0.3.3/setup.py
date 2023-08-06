# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pylinalg', 'pylinalg.func', 'pylinalg.obj']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.20.0']

setup_kwargs = {
    'name': 'pylinalg',
    'version': '0.3.3',
    'description': 'Linear algebra utilities for Python',
    'long_description': '[![PyPI version](https://badge.fury.io/py/pylinalg.svg)](https://badge.fury.io/py/pylinalg)\n\n# pylinalg\n\nLinear algebra utilities for Python.\n',
    'author': 'Korijn van Golen',
    'author_email': 'korijn@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/pygfx/pylinalg',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
