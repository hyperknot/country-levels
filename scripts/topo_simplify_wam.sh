#!/usr/bin/env bash
set -e
cd "${BASH_SOURCE%/*}/" || exit

cd ..

GEOJSON_COLLECTED=data/geojson/wam/collected
GEOJSON_SIMP=data/geojson/wam/simp
TOPOJSON=data/topojson/wam

# rm -rf $TOPOJSON $GEOJSON_SIMP
mkdir -p $TOPOJSON $GEOJSON_SIMP

for l in 1 2
do
  node --max-old-space-size=40000 node_modules/.bin/geo2topo \
    -n --quantization 1e8 \
    iso$l=$GEOJSON_COLLECTED/iso$l.ndjson \
    -o $TOPOJSON/topo$l.json

  for i in 7
  do
    node --max-old-space-size=40000 node_modules/.bin/toposimplify \
      -s 1e-$i -o $TOPOJSON/simp-$i.json $TOPOJSON/topo$l.json

    node --max-old-space-size=40000 node_modules/.bin/topo2geo \
      -i $TOPOJSON/simp-$i.json \
      iso$l=$GEOJSON_SIMP/iso$l-$i.geojson

    node --max-old-space-size=40000 node_modules/.bin/geojson-precision \
      -p 3 $GEOJSON_SIMP/iso$l-$i.geojson $GEOJSON_SIMP/iso$l-$i.geojson
  done
done

# rm -rf $TOPOJSON


