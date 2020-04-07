#!/usr/bin/env bash
set -e
cd "${BASH_SOURCE%/*}/" || exit

../fips/download_csv.sh
./download.py
./collect.py
./topo_simplify.sh
./export.py
./docs.py
