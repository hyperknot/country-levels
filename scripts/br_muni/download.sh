#!/usr/bin/env bash
set -e; set -o pipefail
cd "${BASH_SOURCE%/*}/" || exit

cd ../..

DIR=data/geojson/br_muni
rm -rf $DIR
mkdir -p $DIR/orig

wget https://raw.githubusercontent.com/thiagoghisi/br-counties-geodata/master/br-counties-min.geojson -O $DIR/orig/orig.geojson
