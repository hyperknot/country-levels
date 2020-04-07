#!/usr/bin/env bash
set -e
cd "${BASH_SOURCE%/*}/" || exit

./fips_download_csv.sh
./fips_download_shp.sh
./fips_shp2geo.sh
./fips_export.py
