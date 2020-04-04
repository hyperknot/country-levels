#!/usr/bin/env bash
set -e
cd "${BASH_SOURCE%/*}/" || exit

cd ../..

rm -rf data/geojson/br_muni
mkdir -p data/geojson/br_muni

wget https://raw.githubusercontent.com/thiagoghisi/br-counties-geodata/master/br-counties-min.geojson -O data/geojson/br_muni/original.geojson
