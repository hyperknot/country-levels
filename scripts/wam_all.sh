#!/usr/bin/env bash
set -e
cd "${BASH_SOURCE%/*}/" || exit

./fips_download_csv.sh
./wam_download.py
./wam_collect.py
./wam_topo_simplify.sh
./wam_export.py
./wam_docs.py
