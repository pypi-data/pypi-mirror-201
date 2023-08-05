# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['grafcet']

package_data = \
{'': ['*']}

install_requires = \
['multipledispatch>=0.6.0,<0.7.0']

setup_kwargs = {
    'name': 'grafcet',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'Pierre Lemaitre',
    'author_email': 'oultetman@sfr.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.09,<4.0',
}


setup(**setup_kwargs)
