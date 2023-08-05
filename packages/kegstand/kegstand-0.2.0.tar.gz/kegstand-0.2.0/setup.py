# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['kegstand']

package_data = \
{'': ['*']}

install_requires = \
['aws-lambda-powertools[aws-sdk]>=2.10.0,<3.0.0', 'pyjwt>=2.1.0,<3.0.0']

extras_require = \
{':python_version < "3.11"': ['tomli>=2.0.1,<3.0.0']}

setup_kwargs = {
    'name': 'kegstand',
    'version': '0.2.0',
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
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
