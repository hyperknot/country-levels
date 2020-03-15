#!/usr/bin/env bash

venv/bin/black \
    --line-length 100 \
    --target-version=py37 \
    --skip-string-normalization \
    --exclude '(\.git/|venv/|node_modules/)'\
    .
