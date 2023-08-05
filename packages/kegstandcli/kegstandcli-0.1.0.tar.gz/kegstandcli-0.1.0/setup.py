# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['kegstandcli',
 'kegstandcli.cli',
 'kegstandcli.infra',
 'kegstandcli.infra.stacks']

package_data = \
{'': ['*']}

install_requires = \
['aws-cdk-lib>=2.67.0,<3.0.0',
 'aws-solutions-constructs-aws-apigateway-lambda>=2.36.0,<3.0.0',
 'boto3>=1.17.113,<2.0.0',
 'click>=8.0.3,<9.0.0',
 'constructs>=10.0.0,<11.0.0',
 'copier>=6.2.0,<7.0.0',
 'flask>=2.1.0,<3.0.0',
 'pyjwt>=2.1.0,<3.0.0',
 'xxhash>=3.2.0,<4.0.0']

extras_require = \
{':python_version < "3.11"': ['tomli>=2.0.1,<3.0.0']}

entry_points = \
{'console_scripts': ['keg = kegstandcli.cli.__main__:kegstandcli']}

setup_kwargs = {
    'name': 'kegstandcli',
    'version': '0.1.0',
    'description': "The Developer's Toolbelt For Accelerating Mean-Time-To-Party on AWS",
    'long_description': 'None',
    'author': 'JensRoland',
    'author_email': 'mail@jensroland.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://kegstand.dev',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
