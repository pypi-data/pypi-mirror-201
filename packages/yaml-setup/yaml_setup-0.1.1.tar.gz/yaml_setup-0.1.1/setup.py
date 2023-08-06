# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yamlup']

package_data = \
{'': ['*']}

install_requires = \
['pyyaml>=6.0,<7.0', 'schema>=0.7.5,<0.8.0', 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['yaml-setup = yamlup.cli:app',
                     'yamlup = yamlup.cli:app',
                     'ymlsetup = yamlup.cli:app']}

setup_kwargs = {
    'name': 'yaml-setup',
    'version': '0.1.1',
    'description': '',
    'long_description': "# YAML based Windows setup files with schema validation\n\nAs as example, consider this [README for a windows scoop-based setup](out.md).\n\nThis was produced entirely using this module's CLI from the [YAML setup file](tests/setup.yml).\n\nThe command you need is\n\n```shell\n\nyamlup render /path/to/setup.yml -o /path/to/README.md\n```\n\nThis module doesn't have any other aims besides setup schema validation and formatting its contents.",
    'author': 'arnos-stuff',
    'author_email': 'bcda0276@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
