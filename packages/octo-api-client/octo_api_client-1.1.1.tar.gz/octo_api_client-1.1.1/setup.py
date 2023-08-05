# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['octo_client']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.20.0,<3', 'tonalite>=1.7.1,<2']

setup_kwargs = {
    'name': 'octo-api-client',
    'version': '1.1.1',
    'description': 'HTTP client for OCTo (Open Connection for Tourism) APIs.',
    'long_description': "# OCTO API client\n\nPython HTTP client for OCTO (Open Connection for Tourism) APIs.\n\nMore info at [octospec.com](https://octospec.com/)\n\nAPI Specification: https://docs.octo.travel/docs/octo/r6gduoa5ah5ne-octo-api\n\n## Installation\n\n    pip install octo-api-client\n\n## Requirements\n\n* Python v3.7+\n\n## Development\n\n### Getting started\n\n    $ pip install poetry\n    $ poetry install\n\n### Running tests and linters\n\nTo run linters:\n\n    $ poetry run ruff octo_client\n    $ poetry run mypy octo_client\n\nTo run tests:\n\n    $ poetry run pytest\n\n\n## Usage\n\n```\nfrom octo_client import OctoClient\n\nclient = OctoClient('https://octo-api.mysupplier.com', 'MY-SECRET_TOKEN')\nclient.get_suppliers()\n```\n",
    'author': 'Tiqets',
    'author_email': 'connections@tiqets.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
