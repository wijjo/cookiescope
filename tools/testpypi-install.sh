#!/usr/bin/env bash
set -e
if [[ ! -d venv ]]; then
    read -p "Okay to create virtual environment 'venv' here (y/n)? " okay
   [[ $okay == y ]] || exit 1
    python3 -m venv venv
    venv/bin/python3 -m pip install --upgrade pip
fi
read -p "Okay to install cookiescope in 'venv' (y/n)? " okay
[[ $okay == y ]] || exit 1
venv/bin/python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps cookiescope
