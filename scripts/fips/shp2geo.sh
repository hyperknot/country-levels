#!/usr/bin/env bash
set -e; set -o pipefail
cd "${BASH_SOURCE%/*}/" || exit

cd ../..

SHP=data/shp/fips
GEOJSON=data/geojson/fips

rm -rf $GEOJSON
mkdir -p $GEOJSON

yarn

yarn shp2json $SHP/counties_500k/*.shp -o $GEOJSON/counties_500k.geojson --encoding utf8
yarn shp2json $SHP/counties_5m/*.shp -o $GEOJSON/counties_5m.geojson --encoding utf8
yarn shp2json $SHP/counties_20m/*.shp -o $GEOJSON/counties_20m.geojson --encoding utf8

yarn geojson-precision -p 3 $GEOJSON/counties_500k.geojson $GEOJSON/counties_500k.geojson
yarn geojson-precision -p 3 $GEOJSON/counties_5m.geojson $GEOJSON/counties_5m.geojson
yarn geojson-precision -p 3 $GEOJSON/counties_20m.geojson $GEOJSON/counties_20m.geojson

rm -r $SHP
