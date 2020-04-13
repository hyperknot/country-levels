#!/usr/bin/env bash
set -e; set -o pipefail
cd "${BASH_SOURCE%/*}/" || exit

cd ../data

rm -rf tmp geojson/cosm
mkdir -p tmp geojson/cosm

wget https://github.com/osm-without-borders/cosmogony/releases/download/v0.7.3/cosmogony-2020-03-02-regions.jsonl.gz -O tmp/cosm.jsonl.gz

gunzip tmp/cosm.jsonl.gz
mv tmp/cosm.jsonl geojson/cosm/cosm.jsonl

rm -r tmp
