#!/usr/bin/env bash
set -e; set -o pipefail
cd "${BASH_SOURCE%/*}/" || exit

# ./download.py

../fips/download_csv.sh
[ -z "$SKIP_COLLECT" ] && python -u collect.py | tee collect.txt
[ -z "$SKIP_COLLECT" ] && ./topo_simplify.sh
python -u export.py | tee export.txt
./docs.py
