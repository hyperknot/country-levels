#!/usr/bin/env bash
set -e
cd "${BASH_SOURCE%/*}/" || exit

# rm -rf data export
# mkdir data

cd scripts

./download.sh
./shp2geo.sh

# ./wikidata_iso.py
# ./wikidata_population.py

./create_ids.py
./export_geojsons.py
./generate_docs.py
