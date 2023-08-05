# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiofauna', 'aiofauna.app']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'aiohttp-sse>=2.1.0,<3.0.0',
 'aiohttp>=3.8.4,<4.0.0',
 'iso8601>=1.1.0,<2.0.0',
 'pydantic[email,dotenv]>=1.10.7,<2.0.0']

setup_kwargs = {
    'name': 'aiofauna',
    'version': '0.0.4',
    'description': 'A developer friendly yet versatile asynchronous Object-Document Mapper for FaunaDB',
    'long_description': None,
    'author': 'Oscar Bahamonde',
    'author_email': 'oscar.bahamonde.dev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
