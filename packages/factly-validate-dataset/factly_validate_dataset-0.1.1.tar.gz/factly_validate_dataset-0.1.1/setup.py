# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['factly', 'factly.validate_dataset', 'factly.validate_dataset.assets']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.2.4,<2.0.0',
 'pandera>=0.14.4,<0.15.0',
 'pyyaml>=6.0,<7.0',
 'rich>=13.3.2,<14.0.0',
 'setuptools>=57.0.0,<58.0.0',
 'typer>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['valid = factly.validate_dataset.cli:main']}

setup_kwargs = {
    'name': 'factly-validate-dataset',
    'version': '0.1.1',
    'description': 'Pandera Based data validation library for Dataset Projects',
    'long_description': 'None',
    'author': 'Factly Labs',
    'author_email': 'None',
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
