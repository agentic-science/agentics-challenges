#!/usr/bin/env sh
set -eu
mkdir -p build
g++ -std=c++17 -O2 -pipe solution.cpp -o build/solution
