#!/usr/bin/env sh
set -eu
exec timeout --kill-after=1s 8s ./solution
