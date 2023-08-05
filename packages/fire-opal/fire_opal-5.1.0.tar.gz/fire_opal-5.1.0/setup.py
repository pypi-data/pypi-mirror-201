# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fireopal', 'fireopal.functions']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.0,<9.0.0',
 'qctrl-client>=5.0.0,<6.0.0',
 'qctrl-commons>=18.0.0,<19.0.0']

setup_kwargs = {
    'name': 'fire-opal',
    'version': '5.1.0',
    'description': 'Fire Opal Client',
    'long_description': "# Fire Opal Client\n\nThe Fire Opal Client package is a Python client for Q-CTRL's Fire Opal product.\n",
    'author': 'Q-CTRL',
    'author_email': 'support@q-ctrl.com',
    'maintainer': 'Q-CTRL',
    'maintainer_email': 'support@q-ctrl.com',
    'url': 'https://q-ctrl.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
