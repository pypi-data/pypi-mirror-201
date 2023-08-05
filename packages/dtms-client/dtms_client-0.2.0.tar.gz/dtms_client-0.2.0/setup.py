# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dtms_client']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=22.2.0,<23.0.0',
 'cattrs>=22.2.0,<23.0.0',
 'requests>=2.28.2,<3.0.0',
 'yarl>=1.8.2,<2.0.0']

setup_kwargs = {
    'name': 'dtms-client',
    'version': '0.2.0',
    'description': 'Client library for DTMS api',
    'long_description': '# dtms-client\ndtms client for use in other applications\n',
    'author': 'Shahriyar Shawon',
    'author_email': 'ShahriyarShawon321@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
