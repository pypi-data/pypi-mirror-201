# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['secreta']

package_data = \
{'': ['*']}

install_requires = \
['cryptography>=40.0.1,<41.0.0', 'typer>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['secreta = secreta.commands:app']}

setup_kwargs = {
    'name': 'secreta',
    'version': '0.0.1',
    'description': '',
    'long_description': '# secreta\n\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n\nModern CLI Password Manager\n\n\n## Installation\n\n```python\npip install secreta\n```\n\n## Usage\n\n```python\nsecreta set # set your secreta access password\nsecreta new # add new credentials for a serivce\nsecreta get # get credentials for a given service\nsecreta ls # list all credentials added\n```\n\n## Stack\n\n```python\nTyper\n```\n',
    'author': 'caiopeternela',
    'author_email': 'caiopeternela.dev@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
