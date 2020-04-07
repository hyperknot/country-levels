#!/usr/bin/env bash
set -e
cd "${BASH_SOURCE%/*}/" || exit

cd ../..

GEOJSON_COLLECTED=data/geojson/wam/collected
GEOJSON_SIMP=data/geojson/wam/simp
TOPOJSON=data/topojson/wam

rm -rf $TOPOJSON $GEOJSON_SIMP
mkdir -p $TOPOJSON $GEOJSON_SIMP

for i in 1 2
do
  echo "geo2topo iso$i"
  node --max-old-space-size=40000 node_modules/.bin/geo2topo \
    -n --quantization 1e8 \
    iso$i=$GEOJSON_COLLECTED/iso$i.ndjson \
    -o $TOPOJSON/topo$i.json

  for q in 5 7 8
  do
    echo "topo_simplify iso$i q$q"

    node --max-old-space-size=40000 node_modules/.bin/toposimplify \
      -s 1e-$q -o $TOPOJSON/simp-$q.json $TOPOJSON/topo$i.json

    node --max-old-space-size=40000 node_modules/.bin/topo2geo \
      -i $TOPOJSON/simp-$q.json \
      iso$i=$GEOJSON_SIMP/iso$i-$q.geojson

    node --max-old-space-size=40000 node_modules/.bin/geojson-precision \
      -p 3 $GEOJSON_SIMP/iso$i-$q.geojson $GEOJSON_SIMP/iso$i-$q.geojson
  done
done

rm -rf $TOPOJSON


