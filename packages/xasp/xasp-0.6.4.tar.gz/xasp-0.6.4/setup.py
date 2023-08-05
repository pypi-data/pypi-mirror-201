# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xasp']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.3.0,<10.0.0',
 'cairocffi>=1.4.0,<2.0.0',
 'dateutils>=0.6.12,<0.7.0',
 'dumbo-asp==0.0.21',
 'igraph>=0.10.4,<0.11.0']

setup_kwargs = {
    'name': 'xasp',
    'version': '0.6.4',
    'description': 'API for eXplainable Answer Set Programming',
    'long_description': 'None',
    'author': 'Mario Alviano',
    'author_email': 'mario.alviano@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
