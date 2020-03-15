#!/usr/bin/env bash
set -e

rm -rf data/tmp
mkdir data/tmp

wget https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/10m/cultural/ne_10m_admin_0_countries.zip -O data/tmp/countries.zip
wget https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/10m/cultural/ne_10m_admin_0_map_units.zip -O data/tmp/units.zip
wget https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/10m/cultural/ne_10m_admin_0_map_subunits.zip -O data/tmp/subunits.zip
wget https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/10m/cultural/ne_10m_admin_1_states_provinces_lakes.zip -O data/tmp/states.zip

unzip data/tmp/countries.zip -d data/shp/countries
unzip data/tmp/units.zip -d data/shp/units
unzip data/tmp/subunits.zip -d data/shp/subunits
unzip data/tmp/states.zip -d data/shp/states

rm -rf data/tmp
