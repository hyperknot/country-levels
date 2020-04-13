#!/usr/bin/env bash
set -e; set -o pipefail
cd "${BASH_SOURCE%/*}/" || exit

cd ../..

GEOJSON_ORIG=data/geojson/br_muni/orig
GEOJSON_SIMP=data/geojson/br_muni/simp
TOPOJSON=data/topojson/br_muni

rm -rf $TOPOJSON $GEOJSON_SIMP
mkdir -p $TOPOJSON $GEOJSON_SIMP

node --max-old-space-size=40000 node_modules/.bin/geo2topo \
  --quantization 1e8 \
  g=$GEOJSON_ORIG/orig.geojson \
  -o $TOPOJSON/topo.json

for i in 5 7 8
do
  node --max-old-space-size=40000 node_modules/.bin/toposimplify \
    -s 1e-$i -o $TOPOJSON/simp-$i.json $TOPOJSON/topo.json

  node --max-old-space-size=40000 node_modules/.bin/topo2geo \
    -i $TOPOJSON/simp-$i.json \
    g=$GEOJSON_SIMP/simp-$i.geojson

  node --max-old-space-size=40000 node_modules/.bin/geojson-precision \
    -p 3 $GEOJSON_SIMP/simp-$i.geojson $GEOJSON_SIMP/simp-$i.geojson
done

rm -rf $TOPOJSON $GEOJSON_ORIG


