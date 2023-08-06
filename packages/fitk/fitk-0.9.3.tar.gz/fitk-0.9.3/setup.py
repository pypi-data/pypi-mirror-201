# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fitk', 'fitk.interfaces']

package_data = \
{'': ['*']}

install_requires = \
['sympy']

extras_require = \
{':python_version < "3.11"': ['matplotlib>=3.5,<4.0'],
 ':python_version == "3.7"': ['numpy==1.21.6', 'scipy==1.7.3'],
 ':python_version >= "3.11"': ['matplotlib>=3.6,<4.0'],
 ':python_version >= "3.8"': ['numpy>1.22', 'scipy>1.7.3'],
 'classy': ['classy'],
 'coffe': ['coffe'],
 'interfaces': ['coffe', 'classy']}

setup_kwargs = {
    'name': 'fitk',
    'version': '0.9.3',
    'description': 'The Fisher Information ToolKit',
    'long_description': "## FITK - the Fisher Information ToolKit\n[![codecov](https://codecov.io/gh/JCGoran/fitk/branch/master/graph/badge.svg?token=NX9WRX89SI)](https://codecov.io/gh/JCGoran/fitk)\n[![CircleCI](https://dl.circleci.com/status-badge/img/gh/JCGoran/fitk/tree/master.svg?style=shield&circle-token=5cc8653735b0092318b9790720101eaa4c568c10)](https://dl.circleci.com/status-badge/redirect/gh/JCGoran/fitk/tree/master)\n[![python - versions](https://img.shields.io/pypi/pyversions/fitk)](https://pypi.org/project/fitk/)\n[![CodeFactor](https://www.codefactor.io/repository/github/jcgoran/fitk/badge)](https://www.codefactor.io/repository/github/jcgoran/fitk)\n\nFitk is a Python package for computing, manipulating, and plotting of Fisher information matrices.\n\n### Installation\n\nThe best way to install the stable version is via `pip`:\n\n```plaintext\npip install fitk\n```\n\nNote that on some systems you may have to replace `pip` by `python3 -m pip` or similar for the installation.\nFurthermore, if you only wish to install the package for the current user (or don't have root privileges), you should supply the `--user` flag to the above command.\n\nAlternatively, if you want to install the latest development version:\n\n```plaintext\npip install git+https://github.com/JCGoran/fitk\n```\n\n### Usage\n\nFor various examples on how to use FITK, as well as the latest API, please refer to [the main docs](https://jcgoran.github.io/fitk/).\n\n### Issues\n\nIf you encounter any bugs running the code, or have a suggestion for new functionality, please open up a new issue [on GitHub](https://github.com/JCGoran/fitk/issues/).\n\n### Contributing\n\nSee [CONTRIBUTING.md](CONTRIBUTING.md).\n\n### License\n\nSee [LICENSE](LICENSE) file.\n",
    'author': 'JCGoran',
    'author_email': 'goran.jelic-cizmek@unige.ch',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
