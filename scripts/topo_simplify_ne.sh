#!/usr/bin/env bash
set -e
cd "${BASH_SOURCE%/*}/" || exit

cd ..
DIR=data/geojson

rm -f $DIR/*.json

yarn geo2topo \
    countries=$DIR/countries.geojson \
    units=$DIR/units.geojson \
    subunits=$DIR/subunits.geojson \
    states=$DIR/states.geojson \
    -o $DIR/ne-topo.json

for i in 5 7 8
do
  yarn toposimplify -s 1e-$i -o $DIR/ne-topo-simp-$i.json $DIR/ne-topo.json
  yarn topo2geo -i $DIR/ne-topo-simp-$i.json \
    countries=$DIR/countries-$i.geojson \
    units=$DIR/units-$i.geojson \
    subunits=$DIR/subunits-$i.geojson \
    states=$DIR/states-$i.geojson

  yarn geojson-precision -p 3 $DIR/countries-$i.geojson $DIR/countries-$i.geojson
  yarn geojson-precision -p 3 $DIR/units-$i.geojson $DIR/units-$i.geojson
  yarn geojson-precision -p 3 $DIR/subunits-$i.geojson $DIR/subunits-$i.geojson
  yarn geojson-precision -p 3 $DIR/states-$i.geojson $DIR/states-$i.geojson
done

rm $DIR/*.json

