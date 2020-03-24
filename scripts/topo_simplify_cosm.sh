#!/usr/bin/env bash
set -e
cd "${BASH_SOURCE%/*}/" || exit

cd ..

GEOJSON=data/geojson/cosm
TOPOJSON=data/topojson/cosm

rm -rf $TOPOJSON
mkdir -p $TOPOJSON

rm $GEOJSON/*.geojson

yarn geo2topo -n \
  --quantization 1e8 \
  cosm=$GEOJSON/cosm.ndjson \
  -o $TOPOJSON/topo.json

for i in 5 7 8
do
  yarn toposimplify -s 1e-$i -o $TOPOJSON/simp-$i.json $TOPOJSON/topo.json
  yarn topo2geo -i $TOPOJSON/simp-$i.json \
    cosm=$GEOJSON/cosm-$i.geojson \

  yarn geojson-precision -p 3 $GEOJSON/cosm-$i.geojson $GEOJSON/cosm-$i.geojson
  yarn geojson-precision -p 4 $GEOJSON/cosm-$i.geojson $GEOJSON/cosm-$i.geojson
done


rm -rf $TOPOJSON


