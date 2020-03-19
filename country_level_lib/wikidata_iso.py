import time

from country_level_lib.config import wikidata_dir
from country_level_lib.utils import split_to_chunks, write_json
from country_level_lib.wikidata_utils import get_results, get_all_ids, make_wd_ids_str


def get_iso_id0():
    all_ids = get_all_ids(get_countries=True, get_units=False, get_subunits=False, get_states=False)

    data = dict()

    for i, batch in enumerate(split_to_chunks(all_ids, 100)):
        print(f'Querying wikidata ISO id0 batch: #{i+1}, {len(batch)}')

        batch_data = run_query_id0(batch)
        data = dict(data, **batch_data)

        time.sleep(5)

    wikidata_dir.mkdir(exist_ok=True, parents=True)
    write_json(wikidata_dir / 'iso_id0.json', data, indent=2, sort_keys=True)


def get_iso_id3():
    all_ids = get_all_ids(get_countries=False, get_units=False, get_subunits=False, get_states=True)

    data = dict()

    for i, batch in enumerate(split_to_chunks(all_ids, 100)):
        print(f'Querying wikidata ISO ido3 batch: #{i+1}, {len(batch)}')

        batch_data = run_query_id3(batch)
        data = dict(data, **batch_data)

        time.sleep(5)

    wikidata_dir.mkdir(exist_ok=True, parents=True)
    write_json(wikidata_dir / 'iso_id3.json', data, indent=2, sort_keys=True)


def run_query_id0(qids: list):
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


def run_query_id3(qids: list):
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
