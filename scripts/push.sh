#!/usr/bin/env bash
set -e; set -o pipefail
cd "${BASH_SOURCE%/*}/" || exit

cd ../../country-levels-export

rm -rf .git release

DATE=$(date -u +%Y-%m-%dT%H:%M)

git init
git add .
git commit -m "new export at $DATE"
git remote add origin git@github.com:hyperknot/country-levels-export.git
git push -u origin master --force

