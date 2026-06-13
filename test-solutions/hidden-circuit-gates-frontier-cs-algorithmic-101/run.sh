#!/usr/bin/env sh
set -eu
exec timeout --kill-after=1s 50s python3 -u solution.py
