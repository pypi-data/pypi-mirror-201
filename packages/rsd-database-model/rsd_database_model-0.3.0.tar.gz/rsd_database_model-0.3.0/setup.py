# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rsd_database_model',
 'rsd_database_model.alembic',
 'rsd_database_model.alembic.versions',
 'rsd_database_model.tables']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'rsd-database-model',
    'version': '0.3.0',
    'description': 'Database models for RSD catch analyser',
    'long_description': None,
    'author': 'Pintér Tamás',
    'author_email': 'tamas.pinter@pannonszoftver.hu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
