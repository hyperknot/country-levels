#!/usr/bin/env bash
set -e
cd "${BASH_SOURCE%/*}/" || exit

cd scripts

./wam_all.sh
./fips_all.sh
