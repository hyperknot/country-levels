#!/usr/bin/env bash
set -e
cd "${BASH_SOURCE%/*}/" || exit

cd ..

SHP=data/shp/gadm
GEOJSON=data/geojson/gadm

rm -rf $GEOJSON
mkdir -p $GEOJSON

yarn

yarn shp2json $SHP/gadm36_0.shp -o $GEOJSON/g0.geojson --encoding utf8
yarn shp2json $SHP/gadm36_1.shp -o $GEOJSON/g1.geojson --encoding utf8
yarn shp2json $SHP/gadm36_2.shp -o $GEOJSON/g2.geojson --encoding utf8
yarn shp2json $SHP/gadm36_3.shp -o $GEOJSON/g3.geojson --encoding utf8
yarn shp2json $SHP/gadm36_4.shp -o $GEOJSON/g4.geojson --encoding utf8
yarn shp2json $SHP/gadm36_5.shp -o $GEOJSON/g5.geojson --encoding utf8

rm -r $SHP
