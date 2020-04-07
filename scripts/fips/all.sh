#!/usr/bin/env bash
set -e
cd "${BASH_SOURCE%/*}/" || exit

./download_csv.sh
./download_shp.sh
./shp2geo.sh
./export.py
./docs.py
