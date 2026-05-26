#!/usr/bin/env bash
set -euo pipefail
mkdir -p build
g++ solution.cpp -O2 -std=gnu++17 -o build/solution
