#!/usr/bin/env bash
set -e; set -o pipefail
cd "${BASH_SOURCE%/*}/" || exit

cd ..

GEOJSON=data/geojson/gadm
TOPOJSON=data/topojson/gadm

rm -rf $TOPOJSON
mkdir -p $TOPOJSON

for i in 0 1 2 3 4 5
do
  node --max-old-space-size=20000 node_modules/.bin/geo2topo \
    --quantization 1e8 \
    g=$GEOJSON/g$i.geojson \
    -o $TOPOJSON/topo$i.json
done


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

