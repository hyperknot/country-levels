#!/usr/bin/env bash
set -e
cd "${BASH_SOURCE%/*}/" || exit

cd scripts

./download.sh
./shp2geo.sh
./create_ids.py
./export_geojsons.py
./generate_docs.py
