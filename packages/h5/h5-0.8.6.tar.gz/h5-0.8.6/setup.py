# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['h5']

package_data = \
{'': ['*']}

install_requires = \
['h5py>=3.7.0', 'numpy>=1.24.2,<2.0.0', 'typing-extensions>=4.5.0,<5.0.0']

extras_require = \
{'cli': ['click>=8.1.3,<9.0.0',
         'rich>=13.3.3,<14.0.0',
         'globsters>=0.0.2,<0.0.3']}

entry_points = \
{'console_scripts': ['h5 = h5.cli:main']}

setup_kwargs = {
    'name': 'h5',
    'version': '0.8.6',
    'description': 'H5py utils',
    'long_description': '<a href="https://github.com/dynamic-graphics-inc/dgpy-libs">\n<img align="right" src="https://github.com/dynamic-graphics-inc/dgpy-libs/blob/main/docs/images/dgpy_banner.svg?raw=true" alt="drawing" height="120" width="300"/>\n</a>\n\n# h5\n\n[![Wheel](https://img.shields.io/pypi/wheel/h5.svg)](https://img.shields.io/pypi/wheel/h5.svg)\n[![Version](https://img.shields.io/pypi/v/h5.svg)](https://img.shields.io/pypi/v/h5.svg)\n[![py_versions](https://img.shields.io/pypi/pyversions/h5.svg)](https://img.shields.io/pypi/pyversions/h5.svg)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n**Install:** `pip install h5`\n\n---\n\nUtil functions for h5py and home of recursive generators!\n',
    'author': 'jesse',
    'author_email': 'jesse@dgi.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/dynamic-graphics-inc/dgpy-libs/tree/main/libs/h5',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8.0',
}


setup(**setup_kwargs)
