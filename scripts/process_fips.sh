#!/usr/bin/env bash
set -e
cd "${BASH_SOURCE%/*}/" || exit

./download_fips_csv.sh
./download_fips_shp.sh
./shp2geo_fips.sh
./process_geojson_fips.py
