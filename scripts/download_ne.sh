#!/usr/bin/env bash
set -e
cd "${BASH_SOURCE%/*}/" || exit

cd ../data
rm -rf tmp shp
mkdir tmp shp

wget https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/10m/cultural/ne_10m_admin_0_countries.zip -O tmp/countries.zip
wget https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/10m/cultural/ne_10m_admin_0_map_units.zip -O tmp/units.zip
wget https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/10m/cultural/ne_10m_admin_0_map_subunits.zip -O tmp/subunits.zip
wget https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/10m/cultural/ne_10m_admin_1_states_provinces_lakes.zip -O tmp/states.zip

unzip tmp/countries.zip -d shp/countries
unzip tmp/units.zip -d shp/units
unzip tmp/subunits.zip -d shp/subunits
unzip tmp/states.zip -d shp/states

rm -r tmp
