#!/usr/bin/env bash
set -e
cd "${BASH_SOURCE%/*}/" || exit

# ./download.py

../fips/download_csv.sh
# python -u collect.py | tee collect.txt
# ./topo_simplify.sh
python -u export.py | tee export.txt
./docs.py
