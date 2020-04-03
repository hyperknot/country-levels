from setuptools import setup

requirements = ['sparqlwrapper', 'geojson', 'requests', 'xlsx2csv', 'shapely', 'black']

setup(name='country_levels_lib', python_requires='>=3.7', install_requires=requirements)
