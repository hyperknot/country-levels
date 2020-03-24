#!/usr/bin/env python3
import itertools
import json
from pprint import pprint

import geojson

from country_levels_lib.config import geojson_dir


def main():
    infile = open(geojson_dir / 'cosm' / 'cosm.jsonl')
    outfile = open(geojson_dir / 'cosm' / 'cosm.ndjson', 'w')

    for i, line in enumerate(itertools.islice(infile, None, 5)):
        print(f'Processing line #{i}')
        feature = get_feature(line)
        line_geojson = geojson.dumps(feature, ensure_ascii=False)
        outfile.write(line_geojson + '\n')


def get_feature(line):
    prop = json.loads(line)
    geom = prop.pop('geometry')

    feature = geojson.Feature(geometry=geom, properties=prop)
    assert feature.is_valid

    return feature


if __name__ == "__main__":
    main()
