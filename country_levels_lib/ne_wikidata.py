import time

from country_levels_lib.config import geojson_dir, wikidata_dir
from country_levels_lib.utils import read_json, split_to_chunks, write_json
from country_levels_lib.wikidata_utils import make_wd_ids_str, get_results


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


def get_iso_ne0():
    all_ids = get_all_ids(get_countries=True, get_units=False, get_subunits=False, get_states=False)

    data = dict()

    for i, batch in enumerate(split_to_chunks(all_ids, 100)):
        print(f'Querying wikidata ISO ne0 batch: #{i+1}, {len(batch)}')

        batch_data = run_query_ne0(batch)
        data = dict(data, **batch_data)

        time.sleep(5)

    wikidata_dir.mkdir(exist_ok=True, parents=True)
    write_json(wikidata_dir / 'iso_ne0.json', data, indent=2, sort_keys=True)


def get_iso_ne3():
    all_ids = get_all_ids(get_countries=False, get_units=False, get_subunits=False, get_states=True)

    data = dict()

    for i, batch in enumerate(split_to_chunks(all_ids, 100)):
        print(f'Querying wikidata ISO ne3 batch: #{i+1}, {len(batch)}')

        batch_data = run_query_ne3(batch)
        data = dict(data, **batch_data)

        time.sleep(5)

    wikidata_dir.mkdir(exist_ok=True, parents=True)
    write_json(wikidata_dir / 'iso_ne3.json', data, indent=2, sort_keys=True)


def run_query_ne0(qids: list):
    wd_ids_str = make_wd_ids_str(qids)

    endpoint_url = "https://query.wikidata.org/sparql"

    query = """SELECT ?item ?iso WHERE {
        VALUES ?item { WD_ID_STR_TEMPLATE }
        ?item wdt:P297 ?iso.
    }""".replace(
        'WD_ID_STR_TEMPLATE', wd_ids_str
    )

    results = get_results(endpoint_url, query)

    data = {}

    for result in results["results"]["bindings"]:
        qid = result['item']['value'].split('/')[-1]
        iso = result['iso']['value']
        data[qid] = iso

    return data


def run_query_ne3(qids: list):
    wd_ids_str = make_wd_ids_str(qids)

    endpoint_url = "https://query.wikidata.org/sparql"

    query = """SELECT ?item ?iso WHERE {
        VALUES ?item { WD_ID_STR_TEMPLATE }
        ?item wdt:P300 ?iso.
    }""".replace(
        'WD_ID_STR_TEMPLATE', wd_ids_str
    )

    results = get_results(endpoint_url, query)

    data = {}

    for result in results["results"]["bindings"]:
        qid = result['item']['value'].split('/')[-1]
        iso = result['iso']['value']
        data[qid] = iso

    return data
