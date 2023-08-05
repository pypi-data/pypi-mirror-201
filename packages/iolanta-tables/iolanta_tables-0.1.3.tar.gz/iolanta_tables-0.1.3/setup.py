# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['iolanta_tables',
 'iolanta_tables.facets',
 'iolanta_tables.facets.cli',
 'iolanta_tables.facets.csv',
 'iolanta_tables.facets.html',
 'iolanta_tables.facets.json',
 'iolanta_tables.facets.tex']

package_data = \
{'': ['*'],
 'iolanta_tables': ['data/*'],
 'iolanta_tables.facets.html': ['sparql/*']}

install_requires = \
['dominate>=2.7.0,<3.0.0', 'iolanta>=1.0.11,<2.0.0']

entry_points = \
{'iolanta.plugins': ['tables = iolanta_tables:IolantaTables']}

setup_kwargs = {
    'name': 'iolanta-tables',
    'version': '0.1.3',
    'description': 'Linked Data as tables',
    'long_description': '# iolanta-tables\n\n',
    'author': 'Anatoly Scherbakov',
    'author_email': 'altaisoft@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
