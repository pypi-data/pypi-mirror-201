# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['selic_api']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.10.0,<5.0.0',
 'certifi==2022.12.07',
 'python-dateutil>=2.8.2,<3.0.0',
 'requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'selic-api',
    'version': '0.0.6',
    'description': 'API para obtenção dos dados da SELIC.',
    'long_description': "# selic_api\n API para obter a taxa SELIC acumulada para fins de cálculo da atualização monetária para os tributos da Prefeitura de Belo Horizonte.\n\n## Publishing a new version on PyPI\n\nTo publish a new version of a Poetry package to PyPI, follow these steps:\n\n1. Update the version number of your package in your project's pyproject.toml file. This should be done according to the Semantic Versioning guidelines.\n2. Build the distribution files for the new version of your package by running the following command in your project's root directory:\n\n`poetry build`\n\nThis will create a dist directory with the distribution files for your package.\n\n3. Check that the generated distribution files are correct by running the following command:\n\n`poetry check`\n\nThis will perform several checks on the generated distribution files and report any issues.\n\n4. Publish the new version of your package to PyPI by running the following command:\n\n`poetry publish`\n\nThis will upload the distribution files to PyPI and make the new version of your package available for installation.\n\nNote that you will need to have a PyPI account and be logged in to it for this step to work.\n\nAlso, if this is the first time you are publishing your package to PyPI, you will need to create a new release on GitHub (or other version control system you use) and tag it with the new version number before running the poetry publish command. This is because PyPI requires that the source code for each release be available online.\n",
    'author': 'João Marcelo',
    'author_email': 'joaomarceloav@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/marceloid/selic_api',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
