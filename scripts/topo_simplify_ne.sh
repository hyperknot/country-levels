#!/usr/bin/env bash
set -e
cd "${BASH_SOURCE%/*}/" || exit

cd ..

GEOJSON=data/geojson/ne
TOPOJSON=data/topojson/ne

rm -rf $TOPOJSON
mkdir -p $TOPOJSON

yarn geo2topo \
  --quantization 1e8 \
  countries=$GEOJSON/countries.geojson \
  units=$GEOJSON/units.geojson \
  subunits=$GEOJSON/subunits.geojson \
  states=$GEOJSON/states.geojson \
  -o $TOPOJSON/topo.json

for i in 5 7 8
do
  yarn toposimplify -s 1e-$i -o $TOPOJSON/simp-$i.json $TOPOJSON/topo.json
  yarn topo2geo -i $TOPOJSON/simp-$i.json \
    countries=$GEOJSON/countries-$i.geojson \
    units=$GEOJSON/units-$i.geojson \
    subunits=$GEOJSON/subunits-$i.geojson \
    states=$GEOJSON/states-$i.geojson

  yarn geojson-precision -p 3 $GEOJSON/countries-$i.geojson $GEOJSON/countries-$i.geojson
  yarn geojson-precision -p 3 $GEOJSON/units-$i.geojson $GEOJSON/units-$i.geojson
  yarn geojson-precision -p 3 $GEOJSON/subunits-$i.geojson $GEOJSON/subunits-$i.geojson
  yarn geojson-precision -p 3 $GEOJSON/states-$i.geojson $GEOJSON/states-$i.geojson
done

rm $GEOJSON/countries.geojson
rm $GEOJSON/units.geojson
rm $GEOJSON/subunits.geojson
rm $GEOJSON/states.geojson

rm -rf $TOPOJSON


