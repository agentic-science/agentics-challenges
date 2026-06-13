#!/usr/bin/env sh
set -eu
"${CXX:-g++}" -O2 -std=c++17 solution.cpp -o solution
