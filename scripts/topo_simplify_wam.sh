#!/usr/bin/env bash
set -e
cd "${BASH_SOURCE%/*}/" || exit

cd ..

GEOJSON=data/geojson/wam/collected
TOPOJSON=data/topojson/wam

rm -rf $TOPOJSON
mkdir -p $TOPOJSON

rm -f $GEOJSON/*.geojson

node --max-old-space-size=20000 node_modules/.bin/geo2topo \
  -n --quantization 1e8 \
  iso1=$GEOJSON/iso1.ndjson \
  -o $TOPOJSON/topo.json

# for i in 7
# do
#   node --max-old-space-size=20000 node_modules/.bin/toposimplify \
#     -s 1e-$i -o $TOPOJSON/simp-$i.json $TOPOJSON/topo.json

#   node --max-old-space-size=20000 node_modules/.bin/topo2geo \
#     -i $TOPOJSON/simp-$i.json cosm=$GEOJSON/$zone_type-$i.geojson

#   node --max-old-space-size=20000 node_modules/.bin/geojson-precision \
#     -p 3 $GEOJSON/$zone_type-$i.geojson $GEOJSON/$zone_type-$i.geojson
# done

# rm -rf $TOPOJSON


