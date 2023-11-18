#!/usr/bin/env bash
set -e
cd $( dirname $( dirname "${BASH_SOURCE}[0]" ) )
tools/build.sh
venv/bin/python3 -m pip install --upgrade twine
echo ""
echo ">>> Use __token__ for username and API key for password below. <<<"
echo ""
venv/bin/python3 -m twine upload --repository testpypi dist/*
