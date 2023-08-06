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
    'version': '0.1.0',
    'description': '',
    'long_description': '',
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
