#!/usr/bin/env python3

import itertools
import json
from pprint import pprint

from country_levels_lib.config import geojson_dir


def main():
    ndjson = (geojson_dir / 'cosm').glob('*.ndjson')
    for f in ndjson:
        f.unlink()

    jsonl_path = geojson_dir / 'cosm' / 'cosm.jsonl'
    infile = open(jsonl_path)

    outfiles = {}
    for t in ['country', 'country_region', 'state', 'state_district']:
        outfiles[t] = open(geojson_dir / 'cosm' / f'{t}.ndjson', 'w')

    for i, line in enumerate(itertools.islice(infile, None, None)):
        print(f'Processing line #{i}')
        feature, zone_type = get_feature(line)
        line_geojson = json.dumps(feature, ensure_ascii=False)
        outfiles[zone_type].write(line_geojson + '\n')

    infile.close()
    # jsonl_path.unlink()


def get_feature(line):
    prop = json.loads(line)
    geom = prop.pop('geometry')

    feature = {"type": "Feature", "geometry": geom, "properties": prop}

    admin_level = prop['admin_level']
    zone_type = prop['zone_type']

    # too slow
    # feature = geojson.Feature(geometry={}, properties={})
    # assert feature.is_valid

    return feature, zone_type


if __name__ == "__main__":
    main()
