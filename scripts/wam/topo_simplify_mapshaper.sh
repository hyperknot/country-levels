#!/usr/bin/env bash
set -e; set -o pipefail
cd "${BASH_SOURCE%/*}/" || exit

cd ../..

GEOJSON_COLLECTED=data/geojson/wam/collected
GEOJSON_SIMP=data/geojson/wam/simp
TOPOJSON=data/topojson/wam

rm -rf $TOPOJSON $GEOJSON_SIMP
mkdir -p $TOPOJSON $GEOJSON_SIMP

echo "convert to topojson"
node --max-old-space-size=40000 node_modules/.bin/mapshaper \
  -i $GEOJSON_COLLECTED/iso1.ndjson $GEOJSON_COLLECTED/iso2.ndjson \
  combine-files \
  snap-interval=1e-4 \
  -o $TOPOJSON/topo.topojson
#
#for q in 5 7 8
#do
#  echo "topo_simplify iso$i q$q"
#
#  node --max-old-space-size=40000 node_modules/.bin/toposimplify \
#    -s 1e-$q -o $TOPOJSON/simp-$q.json $TOPOJSON/topo$i.json
#
#  node --max-old-space-size=40000 node_modules/.bin/topo2geo \
#    -i $TOPOJSON/simp-$q.json \
#    iso$i=$GEOJSON_SIMP/iso$i-$q.geojson
#
#  node --max-old-space-size=40000 node_modules/.bin/geojson-precision \
#    -p 3 $GEOJSON_SIMP/iso$i-$q.geojson $GEOJSON_SIMP/iso$i-$q.geojson
#done


#rm -rf $TOPOJSON


