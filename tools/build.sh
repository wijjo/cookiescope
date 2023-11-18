#!/usr/bin/env bash
set -e
cd $( dirname $( dirname "${BASH_SOURCE}[0]" ) )
venv/bin/python3 -m pip install '.[build]'
venv/bin/python3 -m build
