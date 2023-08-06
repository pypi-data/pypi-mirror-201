# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['resolver']

package_data = \
{'': ['*']}

install_requires = \
['jsonschema>=3.2.0,<4.0.0',
 'requests>=2.28.2,<3.0.0',
 'validator-collection>=1.5.0,<2.0.0']

entry_points = \
{'sceptre.resolvers': ['request = resolver.request:Request']}

setup_kwargs = {
    'name': 'sceptre-request-resolver',
    'version': '0.4.0',
    'description': 'A Sceptre resolver to make requests from REST API endpoints',
    'long_description': "# sceptre-request-resolver\n\nA Sceptre resolver to make requests from REST API endpoints.\n\n## Motivation\n\nThere are some pretty useful REST API endpoints on the internet.  The endpoints\ncan return lots of different types of data, typically in JSON format.\nThis simple resolver can retrieve that data and pass it to Sceptre parameters\nor scepter_user_data parameters.\n\n## Installation\n\nTo install directly from PyPI\n```shell\npip install sceptre-request-resolver\n```\n\nTo install from this git repo\n```shell\npip install git+https://github.com/Sceptre/sceptre-request-resolver.git\n```\n\n## Usage/Examples\n\n```yaml\nparameters|sceptre_user_data:\n  <name>: !request <API ENDPOINT>\n```\n\n```yaml\nparameters|sceptre_user_data:\n  <name>: !request\n    url: <API ENDPOINT>\n    auth: <authentication type>\n    user: <auth user name>\n    password: <auth password>\n```\n\n__Note__:\n* This resolver always returns a string.\n* Supported authentication types: `basic`\n\n## Example\n\nSimple request:\n\n```yaml\nparameters:\n  wisdom: !request 'https://ron-swanson-quotes.herokuapp.com/v2/quotes'\n```\n\nRequest with basic authentication:\n```yaml\nparameters:\n  wisdom: !request\n    url: https://private.endpoint.com/\n    auth: basic\n    user: MyUsername\n    password: MyUserPwd\n```\n",
    'author': 'Khai Do',
    'author_email': 'zaro0508@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Sceptre/sceptre-request-resolver',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
