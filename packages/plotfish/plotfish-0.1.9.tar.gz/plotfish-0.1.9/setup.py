# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['plotfish']

package_data = \
{'': ['*']}

install_requires = \
['python-socketio>=5.7.2,<6.0.0',
 'requests>=2.28.2,<3.0.0',
 'websocket-client>=1.5.1,<2.0.0']

setup_kwargs = {
    'name': 'plotfish',
    'version': '0.1.9',
    'description': 'Python SDK for Plotfish.',
    'long_description': None,
    'author': 'The Fisherman',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
