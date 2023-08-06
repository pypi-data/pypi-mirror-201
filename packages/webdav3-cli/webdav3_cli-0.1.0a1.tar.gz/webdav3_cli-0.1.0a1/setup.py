# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['webdav3_cli', 'webdav3_cli.cli_parsers']

package_data = \
{'': ['*']}

install_requires = \
['tomlkit>=0.11.7,<0.12.0', 'webdavclient3>=3.14.6,<4.0.0']

entry_points = \
{'console_scripts': ['webdav3 = webdav3_cli.cli:main']}

setup_kwargs = {
    'name': 'webdav3-cli',
    'version': '0.1.0a1',
    'description': 'Command line interface for webdav3',
    'long_description': 'None',
    'author': 'Nicholas Johnson',
    'author_email': 'nicholas.m.j@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
