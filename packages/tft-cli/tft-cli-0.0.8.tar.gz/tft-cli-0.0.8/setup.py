# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['tft', 'tft.cli']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.4,<8.1.0',
 'colorama>=0.4.4,<0.5.0',
 'dynaconf>=3.1.7,<4.0.0',
 'requests>=2.27.1,<3.0.0',
 'rich>=13.3.1,<14.0.0',
 'typer>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['testing-farm = tft.cli.tool:app']}

setup_kwargs = {
    'name': 'tft-cli',
    'version': '0.0.8',
    'description': 'Testing Farm CLI tool',
    'long_description': None,
    'author': 'Miroslav Vadkerti',
    'author_email': 'mvadkert@redhat.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
