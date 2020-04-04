#!/usr/bin/env bash
set -e
cd "${BASH_SOURCE%/*}/" || exit

cd ../../data

rm -rf tmp shp/fips
mkdir -p tmp shp/fips

wget https://www2.census.gov/geo/tiger/GENZ2018/shp/cb_2018_us_county_500k.zip -O tmp/counties_500k.zip
wget https://www2.census.gov/geo/tiger/GENZ2018/shp/cb_2018_us_county_5m.zip -O tmp/counties_5m.zip
wget https://www2.census.gov/geo/tiger/GENZ2018/shp/cb_2018_us_county_20m.zip -O tmp/counties_20m.zip

unzip -j tmp/counties_500k.zip -d shp/fips/counties_500k
unzip -j tmp/counties_5m.zip -d shp/fips/counties_5m
unzip -j tmp/counties_20m.zip -d shp/fips/counties_20m

rm -r tmp
