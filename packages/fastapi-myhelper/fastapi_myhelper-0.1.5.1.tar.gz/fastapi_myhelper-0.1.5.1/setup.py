# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_myhelper',
 'fastapi_myhelper.pydantic',
 'fastapi_myhelper.sqlalchemy',
 'fastapi_myhelper.sqlmodel',
 'fastapi_myhelper.strawberry',
 'fastapi_myhelper.strawberry.extentions',
 'fastapi_myhelper.strawberry.schemas',
 'fastapi_myhelper.strawberry.sqlalchemy',
 'fastapi_myhelper.strawberry.sqlmodel',
 'fastapi_myhelper.tests',
 'fastapi_myhelper.tests.strawberry']

package_data = \
{'': ['*']}

extras_require = \
{'all': ['strawberry-graphql>=0.155.3,<0.156.0', 'sqlmodel>=0.0.8,<0.0.9'],
 'pydantic': ['pydantic>=1.10.4,<2.0.0'],
 'sqlalchemy': ['sqlalchemy>=1.4.17,<=1.4.41'],
 'sqlmodel': ['sqlmodel>=0.0.8,<0.0.9',
              'sqlalchemy>=1.4.17,<=1.4.41',
              'pydantic>=1.10.4,<2.0.0'],
 'strawberry': ['strawberry-graphql>=0.155.3,<0.156.0']}

setup_kwargs = {
    'name': 'fastapi-myhelper',
    'version': '0.1.5.1',
    'description': '',
    'long_description': 'None',
    'author': 'MihaTeam1',
    'author_email': 'sarsern2004@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
