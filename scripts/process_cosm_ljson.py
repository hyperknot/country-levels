#!/usr/bin/env python3

import itertools
import json

from country_levels_lib.config import geojson_dir


def main():
    jsonl_path = geojson_dir / 'cosm' / 'cosm.jsonl'
    infile = open(jsonl_path)
    outfile = open(geojson_dir / 'cosm' / 'cosm.ndjson', 'w')

    for i, line in enumerate(itertools.islice(infile, None, None)):
        print(f'Processing line #{i}')
        feature = get_feature(line)
        line_geojson = json.dumps(feature, ensure_ascii=False)
        outfile.write(line_geojson + '\n')

    infile.close()
    outfile.close()
    # jsonl_path.unlink()


def get_feature(line):
    prop = json.loads(line)
    geom = prop.pop('geometry')

    feature = {"type": "Feature", "geometry": geom, "properties": prop}

    # too slow
    # feature = geojson.Feature(geometry={}, properties={})
    # assert feature.is_valid

    return feature


if __name__ == "__main__":
    main()
