#!/usr/bin/env bash
set -e
cd "${BASH_SOURCE%/*}/" || exit

cd ../data
rm -rf fips
mkdir -p fips

wget https://www2.census.gov/programs-surveys/popest/geographies/2018/all-geocodes-v2018.xlsx -O fips/all-geocodes.xlsx
wget https://www2.census.gov/programs-surveys/popest/datasets/2010-2019/counties/totals/co-est2019-alldata.csv -O fips/population.csv
wget https://www2.census.gov/geo/docs/reference/state.txt -O fips/state_postal_codes.csv

xlsx2csv fips/all-geocodes.xlsx | tail -n +5 > fips/all-geocodes.csv
rm fips/all-geocodes.xlsx


