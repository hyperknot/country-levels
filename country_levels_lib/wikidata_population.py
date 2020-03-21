import time

from country_levels_lib.config import wikidata_dir
from country_levels_lib.utils import split_to_chunks, write_json
from country_levels_lib.wikidata_utils import get_all_ids, make_wd_ids_str, get_results


def get_population():
    all_ids = get_all_ids()

    simple_data = dict()
    latest_data = dict()

    for i, batch in enumerate(split_to_chunks(all_ids, 100)):
        print(f'Querying wikidata population batch: #{i+1}, {len(batch)}')

        # fill with simple data
        simple_batch = run_query_simple(batch)
        simple_data = dict(simple_data, **simple_batch)

        # overwrite with latest data
        latest_batch = run_query_latest(batch)
        latest_data = dict(latest_data, **latest_batch)

        time.sleep(5)

    mix_data = dict(simple_data, **latest_data)

    wikidata_dir.mkdir(exist_ok=True, parents=True)
    write_json(wikidata_dir / 'population.json', mix_data, indent=2, sort_keys=True)


def run_query_simple(qids: list):
    wd_ids_str = make_wd_ids_str(qids)

    endpoint_url = "https://query.wikidata.org/sparql"

    query = """SELECT ?item ?population WHERE {
        VALUES ?item { WD_ID_STR_TEMPLATE }
        ?item wdt:P1082 ?population.
    }""".replace(
        'WD_ID_STR_TEMPLATE', wd_ids_str
    )

    results = get_results(endpoint_url, query)

    data = {}

    for result in results["results"]["bindings"]:
        qid = result['item']['value'].split('/')[-1]
        population = int(float(result['population']['value']))
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

    results = get_results(endpoint_url, query)

    data = {}

    for result in results["results"]["bindings"]:
        qid = result['item']['value'].split('/')[-1]
        population = int(float(result['population']['value']))
        data[qid] = population

    return data
