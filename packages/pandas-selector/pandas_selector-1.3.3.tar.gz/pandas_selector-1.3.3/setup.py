# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pandas_selector']

package_data = \
{'': ['*']}

install_requires = \
['pandas_paddles==1.3.3']

setup_kwargs = {
    'name': 'pandas-selector',
    'version': '1.3.3',
    'description': 'Stub package to install the matching pandas_paddles',
    'long_description': None,
    'author': 'Eike von Seggern',
    'author_email': 'eikevons@mailbox.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/eikevons/pandas-paddles.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
