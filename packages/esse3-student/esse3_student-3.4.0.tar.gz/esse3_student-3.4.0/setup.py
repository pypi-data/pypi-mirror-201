# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['esse3_student', 'esse3_student.tui', 'esse3_student.utils']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.3,<4.0.0',
 'asyncselenium>=0.0.2,<0.0.3',
 'dataclass-type-validator>=0.1.2,<0.2.0',
 'dateutils>=0.6.12,<0.7.0',
 'export>=0.2.0,<0.3.0',
 'httpx>=0.23.3,<0.24.0',
 'pytest-localserver>=0.7.0,<0.8.0',
 'python-dotenv>=0.21.1,<0.22.0',
 'rich>=12.5.1,<13.0.0',
 'screeninfo>=0.8.1,<0.9.0',
 'selenium>=4.4.3,<5.0.0',
 'self>=2020.12.3,<2021.0.0',
 'termcolor>=2.2.0,<3.0.0',
 'textual>=0.6.0,<0.7.0',
 'typeguard>=2.13.3,<3.0.0',
 'typer>=0.6.1,<0.7.0',
 'valid8>=5.1.2,<6.0.0',
 'webdriver-manager>=3.8.3,<4.0.0']

extras_require = \
{':python_version >= "3.10" and python_version < "4.0"': ['xdotool>=0.4.0,<0.5.0']}

setup_kwargs = {
    'name': 'esse3-student',
    'version': '3.4.0',
    'description': 'Esse3 command line utility',
    'long_description': 'None',
    'author': 'Antonio Pallaria',
    'author_email': 'pallaria98@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
