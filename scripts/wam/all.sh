#!/usr/bin/env bash
set -e
cd "${BASH_SOURCE%/*}/" || exit

# ./download.py

../fips/download_csv.sh
./collect.py
./topo_simplify.sh
./export.py
./docs.py
