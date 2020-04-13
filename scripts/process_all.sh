#!/usr/bin/env bash
set -e; set -o pipefail
cd "${BASH_SOURCE%/*}/" || exit

rm -rf ../data/{fips,shp,topojson}
rm -rf ../data/geojson/{br_muni,fips}

[ -z "$SKIP_COLLECT" ] && rm -rf ../data/wam
[ -z "$SKIP_COLLECT" ] && rm -rf ../data/geojson/wam/{collected,simp}

rm -rf ../../country-levels-export

./wam/all.sh
./fips/all.sh
./br_muni/all.sh

./push.sh
./release.sh
