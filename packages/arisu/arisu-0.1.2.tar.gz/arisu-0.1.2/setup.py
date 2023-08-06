# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['arisu', 'arisu.extensions', 'arisu.loaders']

package_data = \
{'': ['*']}

install_requires = \
['Flask>=2.2.3,<3.0.0',
 'jinja2>=3.1.2,<4.0.0',
 'mistune>=2.0.5,<3.0.0',
 'multiprocess>=0.70.14,<0.71.0',
 'pydantic>=1.10.7,<2.0.0',
 'python-benedict>=0.30.0,<0.31.0',
 'rich>=13.3.3,<14.0.0',
 'tomli>=2.0.1,<3.0.0',
 'watchdog>=3.0.0,<4.0.0',
 'websockets>=11.0,<12.0']

entry_points = \
{'console_scripts': ['aris = aris.__main__:main']}

setup_kwargs = {
    'name': 'arisu',
    'version': '0.1.2',
    'description': '',
    'long_description': '<!-- @format -->\n\ngi# sitegen\n',
    'author': 'Alex Zhang',
    'author_email': 'zhangchi0104@live.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
