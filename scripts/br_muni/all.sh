#!/usr/bin/env bash
set -e; set -o pipefail
cd "${BASH_SOURCE%/*}/" || exit

./download.sh
./topo_simplify.sh
./export.py
./docs.py
