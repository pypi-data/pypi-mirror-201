# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['avsec',
 'avsec.analyze',
 'avsec.attack',
 'avsec.attack.image',
 'avsec.attack.lidar',
 'avsec.defend',
 'avsec.defend.lidar']

package_data = \
{'': ['*'], 'avsec.attack.lidar': ['configs/*']}

install_requires = \
['numpy>=1.19,<2.0']

setup_kwargs = {
    'name': 'lib-avsec',
    'version': '0.1.0a1',
    'description': 'Security analysis routines for autonomous vehicles',
    'long_description': '# Perception Attack Utilities\n\n## Installation\nInstall from a directory above as\n\n```\npip install -e ./lib-percep_attacks\n```\n\n## Dependencies\nDepends on the `avutils` library\n',
    'author': 'Spencer Hallyburton',
    'author_email': 'spencer.hallyburton@duke.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://cpsl.pratt.duke.edu/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.9',
}


setup(**setup_kwargs)
