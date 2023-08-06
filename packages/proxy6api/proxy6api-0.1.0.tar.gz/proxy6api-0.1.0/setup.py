# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['proxy6api', 'proxy6api.settings']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.2,<3.0.0']

setup_kwargs = {
    'name': 'proxy6api',
    'version': '0.1.0',
    'description': 'This is unofficial software for using api with proxy 6.net',
    'long_description': '# Proxy6API\nThis is unofficial software for using api with proxy 6.net\n',
    'author': 'Konstantin Raikhert',
    'author_email': 'raikhert13@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
