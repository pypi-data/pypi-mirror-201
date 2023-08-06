# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bootloader',
 'bootloader.ue',
 'bootloader.ue.cli',
 'bootloader.ue.constant',
 'bootloader.ue.model',
 'bootloader.ue.utils']

package_data = \
{'': ['*']}

install_requires = \
['perseus-core-library>=1.19.2,<2.0.0']

entry_points = \
{'console_scripts': ['ueprjver = bootloader.ue.cli.uassetdump:run']}

setup_kwargs = {
    'name': 'uasset-dump',
    'version': '0.0.3',
    'description': 'Command-line Interface (CLI) responsible for returning the list of the assets of an Unreal Engine project into a JSON structure',
    'long_description': '# Unreal Engine Assets Dump\n\nCommand-line Interface (CLI) responsible for returning the list of the assets of an Unreal Engine project into a JSON structure.\n\n## Development\n\n### Poetry\n\nUnreal Engine Assets Dump used Poetry to declare all its dependencies.  [Poetry](https://python-poetry.org/) is a python dependency management tool to manage dependencies, packages, and libraries in your python project.\n\nWe need to install Poetry with Unreal Engine Python:\n\n```shell\ncurl -sSL https://install.python-poetry.org | python3 -\n```\n\nThen, we need to create the Python virtual environment using Poetry:\n\n```shell\npoetry env use /Users/Shared/Epic\\ Games/UE_5.1/Engine/Binaries/ThirdParty/Python3/Mac/bin/python3\n```\n\nWe can enter this virtual environment and install all the required dependencies:\n\n```shell\npoetry shell\npoetry update\n```\n\n\n## Installation\n\n```shell\n/Users/Shared/Epic\\ Games/UE_5.1/Engine/Binaries/ThirdParty/Python3/Mac/bin/python3 -m pip install --upgrade uasset-dump\n```',
    'author': 'Daniel CAUNE',
    'author_email': 'daniel@bootloader.studio',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/bootloader-studio/cli-uasset-dump',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
