# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pso_load_flow']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.24.2,<2.0.0', 'pandas>=1.5.3,<2.0.0']

setup_kwargs = {
    'name': 'pso-load-flow',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Danilo Nascimento',
    'author_email': 'daconnas.dcn@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10.6,<4.0.0',
}


setup(**setup_kwargs)
