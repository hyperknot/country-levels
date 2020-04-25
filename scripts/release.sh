#!/usr/bin/env bash
set -e; set -o pipefail
cd "${BASH_SOURCE%/*}/" || exit

cd ../../country-levels-export

echo '{"name": "country-levels","version": "1.0.0"}' > package.json

rm -rf release

for simp in low medium high json
do
  mkdir -p release/$simp
  cp *.json release/$simp
  cp *.md release/$simp
  [ $simp != "json" ] && cp -R geojson/$simp/. release/$simp/geojson
  cd release/$simp || exit
  tar -czvf ../export_$simp.tgz .
  cd ../..
  rm -rf release/$simp
done

