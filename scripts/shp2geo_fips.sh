#!/usr/bin/env bash
set -e
cd "${BASH_SOURCE%/*}/" || exit

cd ..

SHP=data/shp/census
GEOJSON=data/geojson/census

rm -rf $GEOJSON
mkdir -p $GEOJSON

yarn

yarn shp2json $SHP/counties_500k/*.shp -o $GEOJSON/counties_500k.geojson --encoding utf8
yarn shp2json $SHP/counties_5m/*.shp -o $GEOJSON/counties_5m.geojson --encoding utf8
yarn shp2json $SHP/counties_20m/*.shp -o $GEOJSON/counties_20m.geojson --encoding utf8

rm -r $SHP
