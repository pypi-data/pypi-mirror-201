# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['guten', 'guten.backends']

package_data = \
{'': ['*']}

install_requires = \
['feedparser>=6.0.10,<7.0.0',
 'httpx>=0.23.1,<0.24.0',
 'pandas>=1.5.2,<2.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'pytz>=2022.7,<2023.0',
 'toml==0.10.2']

setup_kwargs = {
    'name': 'guten',
    'version': '0.1.10',
    'description': '',
    'long_description': '# guten\n\nCompile RSS/Atom feeds into a combined feed.\n',
    'author': 'Elton',
    'author_email': 'eltonp3103@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
