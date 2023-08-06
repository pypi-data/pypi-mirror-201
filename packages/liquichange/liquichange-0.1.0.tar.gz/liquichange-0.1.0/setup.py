# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['liquichange']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'liquichange',
    'version': '0.1.0',
    'description': 'Build and modify Liquibase changelogs in Python.',
    'long_description': '# liquichange\nBuild and modify Liquibase changelogs in Python.\n\nLIQUIBASE is a registered trademark of Liquibase, INC. Liquibase Open Source is released under the Apache 2.0 license.\n',
    'author': 'Nelson Moore',
    'author_email': 'nelson.moore@essential-soft.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
