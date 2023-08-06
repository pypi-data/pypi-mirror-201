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
    'version': '1.0.0',
    'description': 'Command line interface for webdav3',
    'long_description': '# webdav3-cli\n\nSimple command-line interface for interacting with a WebDAV server.\n\nThis was tested and developed against the WebDAV interface for a [Redmine](https://www.redmine.org/) server.\n\n## Usage\n\n### Configuring\n\nYou can configure a set of default values for the optional arguments using the `config` command \n\n#### Examples:\n`webdav3 config set hostname="http://client.openjaus.net/dmsf/webdav/openjaus4-sdk-cpp"`\n\n`webdav3 config set user={username}`\n\n`webdav3 config set pass={password}`\n\n\n### Uploading files\n\nFiles can be uploaded to the WebDAV server using the `upload` command\n\n#### Examples:\n`webdav3 upload {local_path} {remote_path} --hostname {server address} --root "/dmsf/webdav" --user {username} --pass {password}`\n\n`webdav3 upload {local_path} {remote_path}`\n',
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
