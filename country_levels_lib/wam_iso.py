import itertools
import json

from country_levels_lib.config import geojson_dir
from country_levels_lib.utils import read_json
from country_levels_lib.wam_download import wam_geojson_download_dir
from country_levels_lib.wikidata_iso import get_osm_iso1_map, get_osm_wd_map, get_osm_iso2_map

collected_dir = geojson_dir / 'wam' / 'collected'
iso1_found_path = collected_dir / 'iso1_found.ndjson'
iso2_found_path = collected_dir / 'iso2_found.ndjson'

osm_iso1_map = {}
osm_iso2_map = {}
osm_wd_map = {}


def collect_iso():
    global osm_iso1_map, osm_iso2_map, osm_wd_map

    osm_iso1_map = get_osm_iso1_map()
    osm_iso2_map = get_osm_iso2_map()
    osm_wd_map = get_osm_wd_map()

    geojson_files = (wam_geojson_download_dir / 'FRA').glob(
        '**/*.GeoJson'
    )  # strange capitalization inside zips

    collected_dir.mkdir(parents=True, exist_ok=True)
    iso1_found = open(iso1_found_path, 'w')
    iso2_found = open(iso2_found_path, 'w')

    geojson_files_sorted = sorted(geojson_files, key=lambda p: p.stat().st_size, reverse=True)

    for f in itertools.islice(geojson_files_sorted, None, 10):
        print(f.stem)
        features = read_json(f)['features']
        add_iso(features, iso1_found, iso2_found)

    iso1_found.close()
    iso2_found.close()


def add_iso(features: list, found_iso1_file, found_iso2_file):
    for feature in features:
        prop = feature['properties']
        alltags = prop['alltags']

        name = prop['name']
        osm_id = prop['id']

        iso1_from_wd = osm_iso1_map.get(osm_id)
        iso1_from_osm = alltags.get('ISO3166-1')

        iso2_from_wd = osm_iso2_map.get(osm_id)
        iso2_from_osm = alltags.get('ISO3166-2')

        wd_id_from_wd = osm_wd_map.get(osm_id)
        wd_id_from_osm = prop.get('wikidata')

        if wd_id_from_wd and wd_id_from_osm and wd_id_from_wd != wd_id_from_osm:
            print(
                f'  wd_id mismatch: name: {name} osm_id: {osm_id} wd: {wd_id_from_wd} osm: {wd_id_from_osm}'
            )

        if iso1_from_wd or iso1_from_osm:
            # if any of the sources has ISO1, use that
            # many examples in FRA, including FX which is only found in Wikidata
            iso1 = iso1_from_osm
            if iso1_from_wd != iso1_from_osm:
                if iso1_from_wd and iso1_from_osm:
                    print('iso1 mismatch', iso1_from_wd, iso1_from_osm, name, osm_id, iso1)

                if iso1_from_wd:
                    iso1 = iso1_from_wd

            prop['iso1'] = iso1

            geojson_str = json.dumps(feature, ensure_ascii=False, allow_nan=False)
            found_iso1_file.write(geojson_str + '\n')

        #
        #
        if iso2_from_wd or iso2_from_osm:
            # if any of the sources has ISO2, use that
            # many examples in FRA, including FX which is only found in Wikidata
            iso2 = iso2_from_osm
            if iso2_from_wd != iso2_from_osm:
                if iso2_from_wd and iso2_from_osm:
                    print('iso2 mismatch', iso2_from_wd, iso2_from_osm, name, osm_id, iso2)

                if iso2_from_wd:
                    iso2 = iso2_from_wd

            prop['iso2'] = iso2

            geojson_str = json.dumps(feature, ensure_ascii=False, allow_nan=False)
            found_iso2_file.write(geojson_str + '\n')
