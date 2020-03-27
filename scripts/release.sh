#!/usr/bin/env bash
set -e
cd "${BASH_SOURCE%/*}/" || exit

cd ..

rm -rf release

for i in 5 7 8
do
  mkdir -p release/q$i/geojson
  cp export/*.json release/q$i
  cp -R export/geojson/q$i/ release/q$i/geojson
  cd release/q$i || exit
  cp ../../data_license.md license.md
  7z a ../export_q$i.zip "*"
  cd ../..
done
