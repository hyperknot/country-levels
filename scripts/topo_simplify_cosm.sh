#!/usr/bin/env bash
set -e
cd "${BASH_SOURCE%/*}/" || exit

cd ..

GEOJSON=data/geojson/cosm
TOPOJSON=data/topojson/cosm

rm -rf $TOPOJSON
mkdir -p $TOPOJSON

rm -f $GEOJSON/*.geojson

node --max-old-space-size=20000 node_modules/.bin/geo2topo \
  -n --quantization 1e8 \
  cosm=$GEOJSON/cosm.ndjson \
  -o $TOPOJSON/topo.json

for i in 5 7 8
do
  node --max-old-space-size=20000 node_modules/.bin/toposimplify \
    -s 1e-$i -o $TOPOJSON/simp-$i.json $TOPOJSON/topo.json

  node --max-old-space-size=20000 node_modules/.bin/topo2geo \
    -i $TOPOJSON/simp-$i.json cosm=$GEOJSON/cosm-$i.geojson

  node --max-old-space-size=20000 node_modules/.bin/geojson-precision \
    -p 3 $GEOJSON/cosm-$i.geojson $GEOJSON/cosm-$i.geojson
done


rm -rf $TOPOJSON


