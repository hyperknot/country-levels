from country_levels_lib.config import wikidata_dir
from country_levels_lib.utils import write_json, read_json
from country_levels_lib.wikidata.wikidata_utils import get_results


def get_osm_iso1_map():
    endpoint_url = "https://query.wikidata.org/sparql"

    query = """SELECT ?region ?iso1 ?iso2 ?osm WHERE {
      ?region wdt:P297 ?iso1;
        wdt:P402 ?osm.
    }"""

    results = get_results(endpoint_url, query)

    osm_iso1_map = {}

    for result in results["results"]["bindings"]:
        iso1 = result['iso1']['value']
        osm = int(result['osm']['value'])

        osm_iso1_map[osm] = iso1

    return osm_iso1_map


def get_osm_iso2_map():
    endpoint_url = "https://query.wikidata.org/sparql"

    query = """SELECT ?region ?iso1 ?iso2 ?osm WHERE {
      ?region wdt:P300 ?iso2;
        wdt:P402 ?osm.
    }"""

    results = get_results(endpoint_url, query)

    osm_iso2_map = {}

    for result in results["results"]["bindings"]:
        iso2 = result['iso2']['value']
        osm = int(result['osm']['value'])

        osm_iso2_map[osm] = iso2

    return osm_iso2_map


def get_osm_wd_map():
    endpoint_url = "https://query.wikidata.org/sparql"

    query = """SELECT ?region ?osm WHERE {
          ?region wdt:P297 ?iso1;
            wdt:P402 ?osm.
        }"""

    iso1_results = get_results(endpoint_url, query)

    query = """SELECT ?region ?osm WHERE {
              ?region wdt:P300 ?iso2;
                wdt:P402 ?osm.
            }"""

    iso2_results = get_results(endpoint_url, query)

    osm_wd_map = {}

    for result in iso1_results["results"]["bindings"] + iso2_results["results"]["bindings"]:
        osm = int(result['osm']['value'])
        wd_id = result['region']['value'].split('/')[-1]

        osm_wd_map[osm] = wd_id

    return osm_wd_map
