# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['osmrx',
 'osmrx.apis_handler',
 'osmrx.data_processing',
 'osmrx.globals',
 'osmrx.graph_manager',
 'osmrx.helpers',
 'osmrx.main',
 'osmrx.topology']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.7.1,<4.0.0',
 'more-itertools>=9.1.0,<10.0.0',
 'requests-futures>=1.0.0,<2.0.0',
 'rtree>=1.0.1,<2.0.0',
 'rustworkx[mpl]>=0.12.1,<0.13.0',
 'scipy>=1.10.1,<2.0.0',
 'setuptools>=67.6.1,<68.0.0',
 'shapely>=2.0.1,<3.0.0']

setup_kwargs = {
    'name': 'osmrx',
    'version': '0.0.5',
    'description': '',
    'long_description': '# OsmRx\n\nA geographic Python library to extract Open Street Map roads (and POIs) from a location or a bounding box, in order to create a graph thanks to Rustworkx. OsmRx is able to clean a network based on Linestring geometries and connect Point geometries. The graph built is able to process graph-analysis (shortest-path, isochrones...)\n\nCapabilities:\n* load data from a location name or a bounding box (roads and pois)\n* graph creation (and topology processing and cleaning)\n* shortest path\n* isochrone builder\n\n[![CI](https://github.com/amauryval/osmrx/actions/workflows/main.yml/badge.svg?branch=master)](https://github.com/amauryval/osmrx/actions/workflows/main.yml)\n[![codecov](https://codecov.io/gh/amauryval/osmrx/branch/master/graph/badge.svg)](https://codecov.io/gh/amauryval/osmrx)\n\n[![PyPI version](https://badge.fury.io/py/osmrx.svg)](https://badge.fury.io/py/osmrx)\n\nCheck the demo [here](https://amauryval.github.io/gdf2bokeh/)\n\n\n## How to install it ?\n\n### with pip\n\n```bash\npip install osmrx\n```\n\n## How to use it ?\n\nCheck the jupyter notebook here : TODO\nCheck the wiki: TODO\n\n### Get POIs\n\nTODO\n\n```python\n\n```\n\n### Get Roads\n\nTODO\n\n```python\n\n```\n\n\n### Compute a shortest path\n\nTODO\n\n```python\n\n```\n\n\n### Compute an Isochrone\n\nTODO\n\n```python\n\n```\n',
    'author': 'amauryval',
    'author_email': 'amauryval@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '==3.11.0',
}


setup(**setup_kwargs)
