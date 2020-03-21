from SPARQLWrapper import SPARQLWrapper, JSON

from country_levels_lib.config import geojson_dir
from country_levels_lib.utils import read_json


def get_all_ids(
    get_countries: bool = True,
    get_units: bool = True,
    get_subunits: bool = True,
    get_states: bool = True,
):
    if get_countries:
        countries = read_json(geojson_dir / 'countries.geojson')['features']
    else:
        countries = []

    if get_units:
        units = read_json(geojson_dir / 'units.geojson')['features']
    else:
        units = []

    if get_subunits:
        subunits = read_json(geojson_dir / 'subunits.geojson')['features']
    else:
        subunits = []

    if get_states:
        states = read_json(geojson_dir / 'states.geojson')['features']
    else:
        states = []

    all_ids = set()

    for feature in countries + units + subunits + states:
        prop = feature['properties']
        for key in prop:
            prop[key.lower()] = prop.pop(key)

        if not prop.get('wikidataid'):
            continue

        all_ids.add(prop['wikidataid'])

    return sorted(all_ids)


def make_wd_ids_str(qids: list):
    wd_prefixed = {f'wd:{qid}' for qid in qids}
    wd_ids_str = ' '.join(wd_prefixed)
    return wd_ids_str


def get_results(endpoint_url, query):
    user_agent = 'country-levels/0.1 (https://github.com/hyperknot/country-levels)'
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()
