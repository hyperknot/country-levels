#!/usr/bin/env bash
set -e; set -o pipefail
cd "${BASH_SOURCE%/*}/" || exit

cd ../data

rm -rf tmp shp/gadm
mkdir -p tmp shp/gadm

wget https://biogeo.ucdavis.edu/data/gadm3.6/gadm36_levels_shp.zip -O tmp/gadm.zip

unzip tmp/gadm.zip -d shp/gadm

rm -r tmp
