#!/usr/bin/env bash
set -e
cd "${BASH_SOURCE%/*}/" || exit

cd ..
GEOJSON=data/geojson/gadm
TOPOJSON=data/topojson/gadm

rm -rf $TOPOJSON
mkdir -p $TOPOJSON

node --max-old-space-size=12000 node_modules/.bin/geo2topo \
    --quantization 1e6 \
    g0=$GEOJSON/g0.geojson \
    g1=$GEOJSON/g1.geojson \
    g2=$GEOJSON/g2.geojson \
    g3=$GEOJSON/g3.geojson \
    g4=$GEOJSON/g4.geojson \
    g5=$GEOJSON/g5.geojson \
    -o $TOPOJSON/topo.json


# for i in 5 7 8
# do
#   node --max-old-space-size=6000 node_modules/.bin/toposimplify -s 1e-$i -o $TOPOJSON/topo$i.json $TOPOJSON/topo.json
#   node --max-old-space-size=6000 node_modules/.bin/topo2geo -i $TOPOJSON/topo$i.json 0=$GEOJSON/simp-$i.geojson

#   # yarn geojson-precision -p 6 $$GEOJSON/0-$i.geojson $GEOJSON/0-$i.geojson
#   # yarn geojson-precision -p 3 $DIR/units-$i.geojson $DIR/units-$i.geojson
#   # yarn geojson-precision -p 3 $DIR/subunits-$i.geojson $DIR/subunits-$i.geojson
#   # yarn geojson-precision -p 3 $DIR/states-$i.geojson $DIR/states-$i.geojson
# done

# rm $DIR/*.json

