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

for i in 5 6 7 8
do
  yarn toposimplify -s 1e-$i -o $DIR/ne-topo-simp-$i.json $DIR/ne-topo.json
  yarn topoquantize 1e5 -o $DIR/ne-topo-simp-$i-q.json $DIR/ne-topo-simp-$i.json
  yarn topo2geo -i $DIR/ne-topo-simp-$i-q.json \
    countries=$DIR/countries-$i.geojson \
    units=$DIR/units-$i.geojson \
    subunits=$DIR/subunits-$i.geojson \
    states=$DIR/states-$i.geojson
done

rm $DIR/*.json
