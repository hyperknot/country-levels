#!/usr/bin/env bash
set -e
cd "${BASH_SOURCE%/*}/" || exit

cd ../data
mkdir -p fips

wget https://www2.census.gov/programs-surveys/popest/geographies/2018/all-geocodes-v2018.xlsx -O fips/census.xlsx

xlsx2csv fips/census.xlsx | tail -n +5 > fips/census.csv
rm fips/census.xlsx


