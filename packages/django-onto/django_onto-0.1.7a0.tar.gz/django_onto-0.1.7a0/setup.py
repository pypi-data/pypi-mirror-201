# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['authz',
 'authz.migrations',
 'onto',
 'onto.authz',
 'onto.authz.migrations',
 'onto.crud',
 'onto.crud.migrations',
 'onto.jobs',
 'onto.jobs.migrations',
 'onto.migrations']

package_data = \
{'': ['*'],
 'onto.crud': ['static/onto/crud/*',
               'static/onto/crud/vendor/*',
               'templates/onto/crud/*']}

install_requires = \
['django>=4.1.6,<5.0.0']

setup_kwargs = {
    'name': 'django-onto',
    'version': '0.1.7a0',
    'description': "Onto (as in 'ontology') is a lightweight extension to Django centered around the concept of an Entity graph, which can be used to simplify the implementation of complex business logic. Onto includes a number of subpackages that leverage the Entity graph, including the powerful `onto.authz` authorization plugin.",
    'long_description': 'Placeholder - Onto source is being migrated to this new destination.\n',
    'author': 'Paul Fischer',
    'author_email': 'pphysch@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
