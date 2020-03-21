#!/usr/bin/env bash
set -e
cd "${BASH_SOURCE%/*}/" || exit

cd ../..

rm -rf tmp_recompress

git clone --mirror git@github.com:hyperknot/country-level-id.git tmp_recompress
cd tmp_recompress
bfg -b 4K -D '*.geojson'
git reflog expire --expire=now --all && git gc --prune=now --aggressive
git push

cd ..
rm -r tmp_recompress
