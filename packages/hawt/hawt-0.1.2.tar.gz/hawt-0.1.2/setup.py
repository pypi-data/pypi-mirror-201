# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hawt']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0',
 'boto3-stubs-lite[essential,identitystore,sso,sso-oidc]>=1.26.105,<2.0.0',
 'boto3>=1.26.105,<2.0.0',
 'mypy>=1.1.1,<2.0.0',
 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['hawt = hawt.main:typer_main']}

setup_kwargs = {
    'name': 'hawt',
    'version': '0.1.2',
    'description': 'Highspot Amazon Web Services Tools; convenicance functions that automate certain security tasks.',
    'long_description': '# Highspot Amazon Web Services Tools (HAWT)\nA collection of utilities for working with Amazon Web Services (AWS) from the command line.\nOften adds the missing "all in one" API call that AWS should have provided.\n\n## Installation\npipx install hawt\n\n## Usage\n```\n Usage: hawt [OPTIONS] COMMAND [ARGS]...\n\n╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────╮\n│ --install-completion          Install completion for the current shell.                                              │\n│ --show-completion             Show completion for the current shell, to copy it or customize the installation.       │\n│ --help                        Show this message and exit.                                                            │\n╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯\n╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────────╮\n│ hello                                                                                                                │\n│ identitycenter                                                                                                       │\n╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯\n```\n\nGet help on a specific command:\n\n```\nhawt identitycenter list-group-memberships-enriched --help\n                                                                                                                                                      \n Usage: hawt identitycenter list-group-memberships-enriched                                                                                           \n            [OPTIONS] [SSO_ADMIN_ROLE_NAME] [SSO_ADMIN_ACCOUNT_ID]                                                                                    \n            [SSO_ADMIN_REGION] [ID_STORE_ID]                                                                                                          \n                                                                                                                                                      \n╭─ Arguments ─────────────────────────────────────────────────────────────────────────────────────────────────────╮\n│   sso_admin_role_name       [SSO_ADMIN_ROLE_NAME]   SSO Role with read access to Identity Center [default: ...] │\n│   sso_admin_account_id      [SSO_ADMIN_ACCOUNT_ID]  AWS Account id, like 123456789012 [default: ...]            │\n│   sso_admin_region          [SSO_ADMIN_REGION]      region, like us-east-1 [default: ...]                       │\n│   id_store_id               [ID_STORE_ID]           Go to identity center Dashboard in the AWS web console,     │\n│                                                     click on the id store, and copy the id                      │\n│                                                     from the url                                                │\n│                                                     [default: ...]                                              │\n╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯\n╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────╮\n│ --outputpath        PATH  [default: sso_group_memberships.csv]                                                  │\n│ --help                    Show this message and exit.                                                           │\n╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯\n```\n',
    'author': 'Anthony Lozano',
    'author_email': 'tony.lozano@highspot.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
