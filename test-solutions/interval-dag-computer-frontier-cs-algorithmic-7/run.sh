#!/usr/bin/env bash
set -euo pipefail
if [ ! -x build/solution ]; then
  mkdir -p build
  g++ solution.cpp -O2 -std=gnu++17 -o build/solution
fi
exec ./build/solution
