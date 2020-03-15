#!/usr/bin/env bash

rm -rf geojson
mkdir geojson

yarn

yarn shp2json shp/countries/*.shp -o geojson/countries.geojson --encoding utf8
yarn shp2json shp/units/*.shp -o geojson/units.geojson --encoding utf8
yarn shp2json shp/subunits/*.shp -o geojson/subunits.geojson --encoding utf8
yarn shp2json shp/states/*.shp -o geojson/states.geojson --encoding utf8
