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
    'version': '0.0.6',
    'description': '',
    'long_description': '# OsmRx\n\nA geographic Python library to extract Open Street Map roads (and POIs) from a location or a bounding box, in order to create a graph thanks to [Rustworkx](https://github.com/Qiskit/rustworkx). OsmRx is able to clean a network based on Linestring geometries and connect Point geometries. The graph built is able to process graph-analysis (shortest-path, isochrones...)\n\nCapabilities:\n* load data from a location name or a bounding box (roads and pois)\n* graph creation (and topology processing and cleaning)\n* shortest path\n* isochrone builder\n\n[![CI](https://github.com/amauryval/osmrx/actions/workflows/main.yml/badge.svg?branch=master)](https://github.com/amauryval/osmrx/actions/workflows/main.yml)\n[![codecov](https://codecov.io/gh/amauryval/osmrx/branch/master/graph/badge.svg)](https://codecov.io/gh/amauryval/osmrx)\n\n[![PyPI version](https://badge.fury.io/py/osmrx.svg)](https://badge.fury.io/py/osmrx)\n\nCheck the demo [here](https://amauryval.github.io/gdf2bokeh/)\n\n\n## How to install it ?\n\n### with pip\n\n```bash\npip install osmrx\n```\n\n## How to use it ?\n\nCheck the jupyter notebook [here](https://amauryval.github.io/OsmRx/)\n\nCheck the wiki: TODO\n\n### Get POIs\n\nFind the Points of interest from a location (Point(s)) or a bounding box: \n* OSM attributes are returned\n* features ready to be used with shapely, GeoPandas (...):\n\n\n```python\nfrom osmrx.main.pois import Pois\n\nlocation_name = "lyon"  \n\n# Initialize the Pois class\npois_object = Pois()\n# call .from_location(location: str) or .from_bbox(bounds: Tuple[float, float, float, float]) to get data from your location\npois_object.from_location(location_name)  # nominatim api is used to get Lyon coordinates\n\n# It returns a list of dictionnaries [{"geometry": Point(...), "attribute": "...", ...}\n# Free for you to use it with GeoPandas or something else (epsg=4326)\npois_data_found = pois_object.data\n```\n\n### Get Roads\n\nFind the vehicle or pedestrian network (LineString(s)) from a location or a bounding box:\n* OSM attributes available\n* OSM features ready to be used with shapely, GeoPandas (...):\n* data cleaned regarding classical topology rules\n\n```python\nfrom osmrx.main.roads import Roads\n\n# Choose the vehicle or the pedestrian network\nroads_object = Roads("vehicle")\n\n# from_location(location: str) is available\nroads_object.from_bbox({6.019674, 4.023742, 46.072575, 4.122018})\n\n# It returns a list of dictionnaries [{"geometry": Point(...), "attribute": "...", ...}\n# Free for you to use it with GeoPandas or something else (epsg=4326)\nroads_data_found = roads_object.data\n\n# return the rustworkx graph (directed for vehicle / undirected for pedestrian)\ngraph = roads_object.graph\n# Free for you to compute graph analysis\n```\n\n\n### Compute a shortest path\n\nCompute the shortest path from an ordered list of Point(s) (at least 2)\n\n```python\nfrom shapely import Point\n\nfrom osmrx.main.roads import GraphAnalysis\n\n# use the GraphAnalysis class and set:\n# the network type (pedestrian or vehicle) and an ordered list of 2 Shapely Points defining the source and the target\n# of your shortest path)\nanalysis_object = GraphAnalysis("pedestrian",\n                              [Point(4.0793058, 46.0350304), Point(4.0725246, 46.0397676)])  # (epsg=4326)\npaths_built = analysis_object.get_shortest_path()\nfor path_object in paths_built:\n    print(path_object.path)  # LineString shortest path (epsg=4326)\n    print(path_object.features())  # List of LineString (with osm attributes) composing the path found\n```\n\n\n### Compute an Isochrone\n\nBuild an isochrone (Polygon(s)) from a Point\n\n```python\nfrom shapely import Point\n\nfrom osmrx.main.roads import GraphAnalysis\n\n# use the GraphAnalysis class and set:\n# the network type (pedestrian or vehicle) and a list of one Shapely Point (epsg=4326) to build the isochone\nanalysis_object = GraphAnalysis("vehicle", [Point(4.0793058, 46.0350304)])\n\n# Set the distance intervals to compute the isochone with a list of integer or float\nisochrones_built = analysis_object.isochrones_from_distance([0, 250, 500, 1000, 1500])\n\n# List of Polygons with a distance attributes based on the intervals defined\nprint(isochrones_built.data)\n```\n',
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
