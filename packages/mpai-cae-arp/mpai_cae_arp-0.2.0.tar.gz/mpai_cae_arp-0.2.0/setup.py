# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mpai_cae_arp', 'mpai_cae_arp.audio', 'mpai_cae_arp.types']

package_data = \
{'': ['*']}

install_requires = \
['librosa>=0.10.0.post2,<0.11.0',
 'llvmlite>=0.39.1,<0.40.0',
 'numpy==1.23.3',
 'pydantic>=1.10.7,<2.0.0',
 'pyyaml>=6.0,<7.0']

setup_kwargs = {
    'name': 'mpai-cae-arp',
    'version': '0.2.0',
    'description': 'The MPAI CAE-ARP software API',
    'long_description': '# MPAI CAE-ARP API\n\n[![LICENSE](https://img.shields.io/badge/license-GPLv3-blue.svg)](https://img.shields.io/badge/license-GPLv3-blue.svg)\n\n## Description\n\nThis package provides a set of tools for common task in MPAI CAE-ARP standard. It is usend in the official implementation of the standard and can be used as well to develop your own.\n\n## License\n\nThis software is licensed under the GPLv3 license. See the [official site](http://www.gnu.org/licenses/gpl-3.0.html) for more information.\n',
    'author': 'Matteo Spanio',
    'author_email': 'dev2@audioinnova.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
