#!/usr/bin/env bash
set -e
cd "${BASH_SOURCE%/*}/" || exit

cd ../data
rm -rf tmp data/geojson/cosm
mkdir -p tmp data/geojson/cosm

wget https://github.com/osm-without-borders/cosmogony/releases/download/v0.7.3/cosmogony-2020-03-02-regions.jsonl.gz -O tmp/cosm.jsonl.gz

gunzip tmp/cosm.jsonl.gz
mv tmp/cosm.jsonl data/geojson/cosm/cosm.jsonl

rm -r tmp
