# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['edge_orm',
 'edge_orm.external',
 'edge_orm.node',
 'edge_orm.resolver',
 'edge_orm.types_generator']

package_data = \
{'': ['*']}

install_requires = \
['black',
 'devtools',
 'edgedb>=1.2.0,<2.0.0',
 'orjson>=3.8.0,<4.0.0',
 'pydantic[email]>=1.10,<2.0']

extras_require = \
{'docs': ['mkdocs-material>=8.5.7,<9.0.0']}

setup_kwargs = {
    'name': 'edge-orm',
    'version': '0.5.2',
    'description': '',
    'long_description': '# edge orm',
    'author': 'Jeremy Berman',
    'author_email': 'jerber@sas.upenn.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
