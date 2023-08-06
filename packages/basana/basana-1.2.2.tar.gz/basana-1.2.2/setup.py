# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['basana',
 'basana.backtesting',
 'basana.core',
 'basana.core.event_sources',
 'basana.external',
 'basana.external.binance',
 'basana.external.binance.csv',
 'basana.external.binance.tools',
 'basana.external.bitstamp',
 'basana.external.bitstamp.csv',
 'basana.external.bitstamp.tools',
 'basana.external.common',
 'basana.external.common.csv',
 'basana.external.yahoo']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp[speedups]>=3.8.4,<4.0.0', 'python-dateutil>=2.8.2,<3.0.0']

setup_kwargs = {
    'name': 'basana',
    'version': '1.2.2',
    'description': 'A Python async and event driven framework for algorithmic trading, with a focus on crypto currencies.',
    'long_description': 'None',
    'author': 'Gabriel Becedillas',
    'author_email': 'gabriel.becedillas@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/gbeced/basana',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<4.0.0',
}


setup(**setup_kwargs)
