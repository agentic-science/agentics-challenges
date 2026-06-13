#!/usr/bin/env sh
set -eu
if [ ! -x ./solution ]; then
  "${CXX:-g++}" -O2 -std=c++17 solution.cpp -o solution
fi
exec timeout --kill-after=1s 25s ./solution
