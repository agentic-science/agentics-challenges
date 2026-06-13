#!/usr/bin/env sh
set -eu
exec timeout --kill-after=1s 25s python3 solution.py
