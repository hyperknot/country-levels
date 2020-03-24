#!/usr/bin/env bash
set -e
cd "${BASH_SOURCE%/*}/" || exit

cd ..
rm -rf data/geojson/gadm
mkdir -p data/geojson/gadm

yarn

yarn shp2json data/shp/gadm/gadm36_0.shp -o data/geojson/gadm/g0.geojson --encoding utf8
yarn shp2json data/shp/gadm/gadm36_1.shp -o data/geojson/gadm/g1.geojson --encoding utf8
yarn shp2json data/shp/gadm/gadm36_2.shp -o data/geojson/gadm/g2.geojson --encoding utf8
yarn shp2json data/shp/gadm/gadm36_3.shp -o data/geojson/gadm/g3.geojson --encoding utf8
yarn shp2json data/shp/gadm/gadm36_4.shp -o data/geojson/gadm/g4.geojson --encoding utf8
yarn shp2json data/shp/gadm/gadm36_5.shp -o data/geojson/gadm/g5.geojson --encoding utf8

# rm -r data/shp
