#!/usr/bin/env bash
set -e; set -o pipefail
cd "${BASH_SOURCE%/*}/" || exit

cd ../..

GEOJSON_COLLECTED=data/geojson/wam/collected
GEOJSON_SIMP=data/geojson/wam/simp_mapshaper
TOPOJSON=data/topojson/wam_mapshaper

rm -rf $TOPOJSON $GEOJSON_SIMP
mkdir -p $TOPOJSON $GEOJSON_SIMP

echo "convert to topojson"
node --max-old-space-size=40000 node_modules/.bin/mapshaper \
  -i $GEOJSON_COLLECTED/iso1.ndjson $GEOJSON_COLLECTED/iso2.ndjson \
  combine-files \
  snap-interval=1e-4 \
  -o $TOPOJSON/topo.topojson

for q in 10 100 1000
do
  echo "topo_simplify q$q"

  node --max-old-space-size=40000 node_modules/.bin/mapshaper \
    -i $TOPOJSON/topo.topojson \
    -simplify \
    interval=$q \
    -o $TOPOJSON/simp-$q.topojson
done


#rm -rf $TOPOJSON


