#!/usr/bin/env bash
set -e
cd "${BASH_SOURCE%/*}/" || exit

cd ../../country-levels-export

cp ../country-levels/docs/export_readme.md README.md

rm -rf .git

git init
git add .
git commit -m "re-exported"
git remote add origin git@github.com:hyperknot/country-levels-export.git
git push -u origin master --force

