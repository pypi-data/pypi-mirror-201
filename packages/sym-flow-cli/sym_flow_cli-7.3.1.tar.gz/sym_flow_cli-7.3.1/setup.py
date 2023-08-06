# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sym',
 'sym.flow',
 'sym.flow.cli',
 'sym.flow.cli.code_generation_templates',
 'sym.flow.cli.code_generation_templates.core',
 'sym.flow.cli.code_generation_templates.core.connectors',
 'sym.flow.cli.code_generation_templates.flows',
 'sym.flow.cli.commands',
 'sym.flow.cli.commands.bots',
 'sym.flow.cli.commands.config',
 'sym.flow.cli.commands.domains',
 'sym.flow.cli.commands.organization',
 'sym.flow.cli.commands.resources',
 'sym.flow.cli.commands.services',
 'sym.flow.cli.commands.services.click',
 'sym.flow.cli.commands.services.hooks',
 'sym.flow.cli.commands.tokens',
 'sym.flow.cli.commands.users',
 'sym.flow.cli.helpers',
 'sym.flow.cli.helpers.code_generation',
 'sym.flow.cli.helpers.config',
 'sym.flow.cli.helpers.login',
 'sym.flow.cli.models']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'auth0-python>=3.23.1,<4.0.0',
 'boto3>=1.16.20,<2.0.0',
 'click>=8.0.0,<9.0.0',
 'cryptography==3.4.8',
 'inflection>=0.5.1,<0.6.0',
 'inquirer>=2.7.0,<3.0.0',
 'pkce>=1.0,<2.0',
 'portalocker>=2.0.0,<3.0.0',
 'pydantic>=1.8.2,<2.0.0',
 'python-hcl2>=4.3.0,<5.0.0',
 'requests>=2.25,<3.0',
 'semver>=2.13.0,<3.0.0',
 'sentry-sdk>=1.0.0,<2.0.0',
 'tabulate>=0.8.7,<0.9.0']

entry_points = \
{'console_scripts': ['symflow = sym.flow.cli.symflow:symflow']}

setup_kwargs = {
    'name': 'sym-flow-cli',
    'version': '7.3.1',
    'description': "Sym's Official CLI for Implementers",
    'long_description': '# sym-flow-cli\n\nThis is the official CLI for [Sym](https://symops.com/) Implementers. Check out the docs [here](https://docs.symops.com/docs/install-sym-flow).\n',
    'author': 'SymOps, Inc.',
    'author_email': 'pypi@symops.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://symops.com/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
