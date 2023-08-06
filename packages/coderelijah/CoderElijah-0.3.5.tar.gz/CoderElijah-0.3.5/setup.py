# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['CoderElijah']

package_data = \
{'': ['*']}

install_requires = \
['Flask>=2.2.0,<3.0.0',
 'numpy>=1.22.2,<2.0.0',
 'replit>=3.2.4,<4.0.0',
 'urllib3>=1.26.12,<2.0.0']

setup_kwargs = {
    'name': 'coderelijah',
    'version': '0.3.5',
    'description': 'This is the custom Python library of @CoderElijah on https://replit.com/.',
    'long_description': None,
    'author': 'CoderElijah',
    'author_email': 'CoderElijah@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
