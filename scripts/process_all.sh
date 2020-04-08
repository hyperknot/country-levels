#!/usr/bin/env bash
set -e
cd "${BASH_SOURCE%/*}/" || exit

rm -rf ../export

./wam/all.sh
./fips/all.sh
./br_muni/all.sh
./release.sh

cd ..

git add .
git commit -m 'regenerated'

