# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['stated']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.4,<4.0.0', 'cryptography>=39.0.1,<40.0.0']

entry_points = \
{'console_scripts': ['stated = stated.terminal:entrypoint']}

setup_kwargs = {
    'name': 'stated',
    'version': '0.1.1a5',
    'description': 'Distributed State in memory',
    'long_description': '# stated\n\nStated aims to provide distributed state in memory(and persistant) purely in python, example usecases can be syncronising state among pods in a set of kubernets pods.\n',
    'author': 'Abbas Jafari',
    'author_email': 'abbas.jafari@powercoders.org',
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
