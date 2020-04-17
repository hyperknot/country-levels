#!/usr/bin/env bash
set -e; set -o pipefail
cd "${BASH_SOURCE%/*}/" || exit

cd ../..

GEOJSON_COLLECTED=data/geojson/wam/collected
GEOJSON_SIMP=data/geojson/wam/simp

rm -rf $GEOJSON_SIMP
mkdir -p $GEOJSON_SIMP/low $GEOJSON_SIMP/medium $GEOJSON_SIMP/high

echo "mapshaper low"
node --max-old-space-size=40000 node_modules/.bin/mapshaper \
  -i $GEOJSON_COLLECTED/iso1.ndjson $GEOJSON_COLLECTED/iso2.ndjson \
  combine-files \
  snap-interval=1e-6 \
  -simplify interval=10000 keep-shapes \
  -filter-islands min-area=10km2 min-vertices=10 \
  -o $GEOJSON_SIMP/low/ format=geojson extension=geojson \
  precision=0.001 singles geojson-type=FeatureCollection

echo "mapshaper medium"
node --max-old-space-size=40000 node_modules/.bin/mapshaper \
  -i $GEOJSON_COLLECTED/iso1.ndjson $GEOJSON_COLLECTED/iso2.ndjson \
  combine-files \
  snap-interval=1e-6 \
  -simplify interval=1000 keep-shapes \
  -filter-islands min-area=10km2 min-vertices=10 \
  -o $GEOJSON_SIMP/medium/ format=geojson extension=geojson \
  precision=0.001 singles geojson-type=FeatureCollection

echo "mapshaper high"
node --max-old-space-size=40000 node_modules/.bin/mapshaper \
  -i $GEOJSON_COLLECTED/iso1.ndjson $GEOJSON_COLLECTED/iso2.ndjson \
  combine-files \
  snap-interval=1e-6 \
  -simplify interval=100 keep-shapes \
  -o $GEOJSON_SIMP/high/ format=geojson extension=geojson \
  precision=0.001 singles geojson-type=FeatureCollection





