import time

from SPARQLWrapper import SPARQLWrapper, JSON

from country_level_lib.config import geojson_dir, population_dir
from country_level_lib.utils import read_json, split_to_chunks, write_json


def get_population():
    all_ids = get_all_ids()

    simple_data = dict()
    latest_data = dict()

    for i, batch in enumerate(split_to_chunks(all_ids, 100)):
        print(f'Querying wikidata for batch: #{i+1}, {len(batch)}')

        # fill with simple data
        simple_batch = run_query_simple(batch)
        simple_data = dict(simple_data, **simple_batch)

        # overwrite with latest data
        latest_batch = run_query_latest(batch)
        latest_data = dict(latest_data, **latest_batch)

        time.sleep(5)

    mix_data = dict(simple_data, **latest_data)

    population_dir.mkdir(exist_ok=True, parents=True)
    write_json(population_dir / 'simple.json', simple_data, indent=2, sort_keys=True)
    write_json(population_dir / 'latest.json', latest_data, indent=2, sort_keys=True)
    write_json(population_dir / 'mix.json', mix_data, indent=2, sort_keys=True)


def get_all_ids():
    countries = read_json(geojson_dir / 'countries.geojson')['features']
    units = read_json(geojson_dir / 'units.geojson')['features']
    subunits = read_json(geojson_dir / 'subunits.geojson')['features']
    states = read_json(geojson_dir / 'states.geojson')['features']

    all_ids = set()

    for feature in countries + units + subunits + states:
        prop = feature['properties']
        for key in prop:
            prop[key.lower()] = prop.pop(key)

        if not prop.get('wikidataid'):
            continue

        all_ids.add(prop['wikidataid'])

    return sorted(all_ids)


def run_query_simple(qids: list):
    wd_ids_str = make_wd_ids_str(qids)

    endpoint_url = "https://query.wikidata.org/sparql"

    query = """SELECT ?item ?population WHERE {
        VALUES ?item { WD_ID_STR_TEMPLATE }
        ?item wdt:P1082 ?population.
    }""".replace(
        'WD_ID_STR_TEMPLATE', wd_ids_str
    )

    def get_results(endpoint_url, query):
        user_agent = 'country-level-id/0.1 (https://github.com/hyperknot/country-level-id)'
        sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        return sparql.query().convert()

    results = get_results(endpoint_url, query)

    data = {}

    for result in results["results"]["bindings"]:
        qid = result['item']['value'].split('/')[-1]
        population = int(result['population']['value'])
        data[qid] = population

    return data


def run_query_latest(qids: list):
    wd_ids_str = make_wd_ids_str(qids)

    endpoint_url = "https://query.wikidata.org/sparql"

    query = """SELECT ?item ?population ?atTime WHERE {
      VALUES ?item { WD_ID_STR_TEMPLATE }
      ?item p:P1082 ?populationStmt .
      ?populationStmt pq:P585 ?atTime .
      ?populationStmt ps:P1082 ?population .
      {
        SELECT ?item (MAX(?time) as ?atTime) WHERE {
          ?item p:P1082 ?populationStmt .
          ?populationStmt pq:P585 ?time . 
        } GROUP BY ?item
      }
    }""".replace(
        'WD_ID_STR_TEMPLATE', wd_ids_str
    )

    def get_results(endpoint_url, query):
        user_agent = 'country-level-id/0.1 (https://github.com/hyperknot/country-level-id)'
        sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        return sparql.query().convert()

    results = get_results(endpoint_url, query)

    data = {}

    for result in results["results"]["bindings"]:
        qid = result['item']['value'].split('/')[-1]
        population = int(result['population']['value'])
        data[qid] = population

    return data


def make_wd_ids_str(qids: list):
    wd_prefixed = {f'wd:{qid}' for qid in qids}
    wd_ids_str = ' '.join(wd_prefixed)
    return wd_ids_str
