# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['abml_cli', 'abml_cli.dataclasses', 'abml_cli.subroutines.dload']

package_data = \
{'': ['*'], 'abml_cli': ['examples/*', 'subroutines/dload/templates/*']}

install_requires = \
['abqpy>=2023.4.3,<2024.0.0',
 'click>=8.1.3,<9.0.0',
 'invoke>=2.0.0,<3.0.0',
 'jinja2>=3.1.2,<4.0.0',
 'numpy>=1.24.2,<2.0.0',
 'pandas>=1.5.3,<2.0.0',
 'pydantic>=1.10.5,<2.0.0',
 'pyyaml>=6.0,<7.0',
 'rich>=13.3.2,<14.0.0']

entry_points = \
{'console_scripts': ['abml = abml_cli.abml_exec:run',
                     'abml_grid = abml_cli.abml_exec:run_grid',
                     'jnl = abml_cli.helpers:extract_data_from_jnl']}

setup_kwargs = {
    'name': 'abml-cli',
    'version': '0.1.3',
    'description': '',
    'long_description': '',
    'author': 'DavidNaizheZhou',
    'author_email': '70525024+DavidNaizheZhou@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>3.8',
}


setup(**setup_kwargs)
