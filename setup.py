from setuptools import setup

requirements = [
    'black',
    'geojson',
    'requests',
    'shapely',
    'sparqlwrapper',
    'timezonefinder',
    'xlsx2csv',
]

setup(name='country_levels_lib', python_requires='>=3.7', install_requires=requirements)
