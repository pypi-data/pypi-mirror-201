# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['torncoder', 'torncoder.cli', 'torncoder.file_util']

package_data = \
{'': ['*']}

install_requires = \
['aiofile[aio]>=3.8.1,<4.0.0',
 'aiofiles[threaded]>=22.1.0,<23.0.0',
 'tornado>=6.0,<7.0']

entry_points = \
{'console_scripts': ['file-cache-server = '
                     'torncoder.cli.file_cache_server:start']}

setup_kwargs = {
    'name': 'torncoder',
    'version': '0.3.0',
    'description': 'Basic tornado-based python utilities.',
    'long_description': '# Torncoder\n\nTornado Utility Library for various features.\n\nThis library contains a few common classes and helpers that:\n - Make file serving easier.\n - Make file uploads easier.\n\n## File Server CLI\n\nThis also implements a simple tool: `file-cache-server`.\nThis CLI tool implements a super simple File server API (with caching headers and so forth).\nSimple usage is:\n```sh\nfile-cache-server -p 7070 -d mydirectory --readonly\n```\nto serve the files at `mydirectory` on port 7070.\nNote that without the `--readonly` flag, this supports PUT and DELETE operations on these files which will create, modify and delete them.\n\n# TBD\n\nAdd an interface that is more S3-compatible.\n',
    'author': 'Aaron Gibson',
    'author_email': 'eulersidcrisis@yahoo.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/eulersIDcrisis/torncoder',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
