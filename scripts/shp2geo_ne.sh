#!/usr/bin/env bash
set -e
cd "${BASH_SOURCE%/*}/" || exit

cd ..

SHP=data/shp/ne
GEOJSON=data/geojson/ne

rm -rf $GEOJSON
mkdir -p $GEOJSON

yarn

yarn shp2json $SHP/countries/*.shp -o $GEOJSON/countries.geojson --encoding utf8
yarn shp2json $SHP/units/*.shp -o $GEOJSON/units.geojson --encoding utf8
yarn shp2json $SHP/subunits/*.shp -o $GEOJSON/subunits.geojson --encoding utf8
yarn shp2json $SHP/states/*.shp -o $GEOJSON/states.geojson --encoding utf8

rm -r $SHP
