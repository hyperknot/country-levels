#!/usr/bin/env bash
set -e
cd "${BASH_SOURCE%/*}/" || exit

rm -rf ../../country-levels-export

./wam/all.sh
./fips/all.sh
./br_muni/all.sh

./push.sh
./release.sh
