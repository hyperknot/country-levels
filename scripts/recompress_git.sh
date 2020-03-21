#!/usr/bin/env bash
set -e
cd "${BASH_SOURCE%/*}/" || exit

cd ..
DIR=$(pwd)

cd ..
rm -rf tmp_clean tmp_recompress*

git clone --mirror git@github.com:hyperknot/country-level-id.git tmp_recompress
cd tmp_recompress || exit
bfg -b 4K -D '*.geojson'
git reflog expire --expire=now --all && git gc --prune=now --aggressive
git push
cd .. || exit

git clone git@github.com:hyperknot/country-level-id.git tmp_clean
rm -rf "$DIR/.git"
mv tmp_clean/.git "$DIR"

rm -rf tmp_clean tmp_recompress*
