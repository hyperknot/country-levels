#!/usr/bin/env bash
set -e

./download.sh
./shp2geo.sh
./create_levels.py
