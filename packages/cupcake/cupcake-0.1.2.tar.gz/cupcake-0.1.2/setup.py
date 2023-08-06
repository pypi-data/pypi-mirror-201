# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['cupcake', 'cupcake.data.new']

package_data = \
{'': ['*'],
 'cupcake': ['data/query/*'],
 'cupcake.data.new': ['include/{{name}}/*', 'src/*', 'tests/*']}

install_requires = \
['click-option-group>=0.5.3,<0.6.0',
 'click>=8.0.4,<9.0.0',
 'jinja2>=3.1.1,<4.0.0',
 'libcst>=0.4.9,<0.5.0',
 'semver>=2.13.0,<3.0.0',
 'tomlkit>=0.10.1,<0.11.0']

entry_points = \
{'console_scripts': ['cupcake = cupcake.main:main']}

setup_kwargs = {
    'name': 'cupcake',
    'version': '0.1.2',
    'description': 'Make C++ a piece of cake.',
    'long_description': None,
    'author': 'John Freeman',
    'author_email': 'jfreeman08@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
