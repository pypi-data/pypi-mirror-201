# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['behave_to_cucumber']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.5.3,<0.6.0']

entry_points = \
{'console_scripts': ['btc = behave_to_cucumber.__main__:main']}

setup_kwargs = {
    'name': 'behave-to-cucumber',
    'version': '0.1.9',
    'description': '该项目主要用于将behave框架生成的behave.json转换为cucumber.json',
    'long_description': None,
    'author': 'chineseluo',
    'author_email': '848257135@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/chineseluo/behave_to_cucumber',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
