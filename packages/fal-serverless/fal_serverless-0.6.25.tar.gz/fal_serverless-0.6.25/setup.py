# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['fal_serverless',
 'fal_serverless.auth',
 'fal_serverless.console',
 'fal_serverless.exceptions',
 'fal_serverless.logging']

package_data = \
{'': ['*']}

install_requires = \
['auth0-python>=3.24.0,<4.0.0',
 'click>=8.1.3,<9.0.0',
 'colorama>=0.4.6,<0.5.0',
 'datadog-api-client>=2.9.0,<3.0.0',
 'dill==0.3.5.1',
 'grpc-interceptor>=0.15.0,<0.16.0',
 'grpcio>=1.50.0,<2.0.0',
 'isolate-proto==0.0.23',
 'isolate[build]==0.11.1',
 'opentelemetry-api>=1.15.0,<2.0.0',
 'opentelemetry-sdk>=1.15.0,<2.0.0',
 'portalocker>=2.7.0,<3.0.0',
 'requests>=2.28.1,<3.0.0',
 'rich>=13.3.2,<14.0.0',
 'structlog>=22.3.0,<23.0.0',
 'typing-extensions==4.4']

entry_points = \
{'console_scripts': ['fal-serverless = fal_serverless.cli:cli']}

setup_kwargs = {
    'name': 'fal-serverless',
    'version': '0.6.25',
    'description': 'fal Serverless is an easy-to-use Serverless Python Framework',
    'long_description': '',
    'author': 'Features & Labels',
    'author_email': 'hello@fal.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
