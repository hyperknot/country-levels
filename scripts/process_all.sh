#!/usr/bin/env bash
set -e
cd "${BASH_SOURCE%/*}/" || exit

./wam/all.sh
./fips/all.sh
./release.sh

cd ..

git add .
git commit 'regenerated'

