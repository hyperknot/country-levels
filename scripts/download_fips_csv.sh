#!/usr/bin/env bash
set -e
cd "${BASH_SOURCE%/*}/" || exit

cd ../data
mkdir -p fips

wget https://www2.census.gov/programs-surveys/popest/geographies/2018/all-geocodes-v2018.xlsx -O fips/fips.xlsx
wget https://www2.census.gov/programs-surveys/popest/datasets/2010-2019/counties/totals/co-est2019-alldata.csv -O fips/population.csv

xlsx2csv fips/fips.xlsx | tail -n +5 > fips/fips.csv
rm fips/fips.xlsx


