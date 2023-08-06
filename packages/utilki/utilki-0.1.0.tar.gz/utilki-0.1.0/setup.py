# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['utilki']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0']

entry_points = \
{'console_scripts': ['utilki = utilki.cli:cli']}

setup_kwargs = {
    'name': 'utilki',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Khaidar Bikmaev',
    'author_email': 'khaidar@bikmaev.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.1',
}


setup(**setup_kwargs)
