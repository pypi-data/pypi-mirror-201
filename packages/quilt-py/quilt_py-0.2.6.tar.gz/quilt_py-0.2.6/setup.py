# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['quilt',
 'quilt.context_base',
 'quilt.extensions',
 'quilt.gql_utils',
 'quilt.gql_utils.resolvers',
 'quilt.middlewares',
 'quilt.models',
 'quilt.models.location',
 'quilt.plugins.StrawberryFilters',
 'quilt.scalars',
 'quilt.services.auth',
 'quilt.vendors',
 'quilt.vendors.Cloudinary',
 'quilt.vendors.Firebase',
 'quilt.vendors.GooglePlaces',
 'quilt.vendors.GooglePlaces.tests',
 'quilt.vendors.IPInfo',
 'quilt.vendors.Sentry']

package_data = \
{'': ['*']}

install_requires = \
['devtools',
 'firebase-admin',
 'httpx',
 'phonenumbers',
 'pydantic[email]',
 'sentry-sdk[httpx,pure-eval]>=1.15,<2.0',
 'strawberry-graphql']

setup_kwargs = {
    'name': 'quilt-py',
    'version': '0.2.6',
    'description': '',
    'long_description': 'hello!',
    'author': 'Jeremy Berman',
    'author_email': 'jerber@sas.upenn.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
