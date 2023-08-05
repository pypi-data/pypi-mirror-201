# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['cmk', 'cmk.objects', 'cmk.objects.interface']

package_data = \
{'': ['*']}

install_requires = \
['furl>=2.1,<3.0', 'incremental>=22,<23', 'requests>=2.28,<3.0']

setup_kwargs = {
    'name': 'python-cmk',
    'version': '23.4.0',
    'description': 'API for CheckMK',
    'long_description': '# python-cmk\n\n[![GitHub](https://img.shields.io/github/license/NimVek/python-cmk)](https://github.com/NimVek/python-cmk/blob/main/LICENSE)\n[![PyPI](https://img.shields.io/pypi/v/python-cmk)](https://pypi.org/project/python-cmk)\n[![GitHub last commit](https://img.shields.io/github/last-commit/NimVek/python-cmk)](https://github.com/NimVek/python-cmk/commits/main)\n[![Build Status](https://img.shields.io/github/actions/workflow/status/NimVek/python-cmk/ci.yml)](https://github.com/NimVek/python-cmk/actions/workflows/ci.yml)\n[![Coverage Status](https://img.shields.io/codecov/c/github/NimVek/python-cmk)](https://codecov.io/gh/NimVek/python-cmk/)\n[![Documentation](https://img.shields.io/badge/docs-passing-brightgreen)](https://nimvek.github.io/python-cmk/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black)\n\nAPI for CheckMK\n',
    'author': 'NimVek',
    'author_email': 'NimVek@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/NimVek/python-cmk',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
