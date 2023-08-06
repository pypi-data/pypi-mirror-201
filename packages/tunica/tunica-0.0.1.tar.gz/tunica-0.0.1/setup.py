# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tunica']

package_data = \
{'': ['*']}

install_requires = \
['isort>=5.12.0,<6.0.0',
 'pre-commit>=3.2.2,<4.0.0',
 'pydantic>=1.10.7,<2.0.0',
 'pytest>=7.2.2,<8.0.0']

setup_kwargs = {
    'name': 'tunica',
    'version': '0.0.1',
    'description': 'Light-weight Python ORM',
    'long_description': '# Tunica\n\nLight-weight Python ORM.\n\n"Wear a Tunica on your low-level code"\n\nBuiltin features:\n* ORM\n  * Use [pydantic](https://github.com/pydantic/pydantic) models\n  * Simple query builder:\n    * `Model.all()`\n    * `Model.filter(TODO).first()`\n  * Simple db configuration. Smart and automatic session management\n  * Hide all low-level sql\n* Migration tool\n  * Fully automatic. Checks changes even if the source db doesn\'t support it (e.g. Enums in GCP Spanner). Compare state of the db with the changes history in all migrations.\n    * Errors/Warnings if there are manual changes\n  * Force to use migrations for data changes:\n    * Move data from one table to another\n    * Modify data in one table\n    * ...\n  * Implement in Rust?\n* SQL Profiling tool (like [silk](https://github.com/jazzband/django-silk) for Django)\n* FastAPI integration\n* Mock for testing (like [alchemy-mock](https://github.com/miki725/alchemy-mock))\n\nAll these features should be architected as independent as possible to be able to move them into another projects\n',
    'author': 'Vladimir Minev',
    'author_email': 'minev.dev@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
