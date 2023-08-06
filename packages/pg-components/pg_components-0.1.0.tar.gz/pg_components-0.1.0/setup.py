# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pg_components']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pg-components',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Dan',
    'author_email': 'kelleherjdan@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
