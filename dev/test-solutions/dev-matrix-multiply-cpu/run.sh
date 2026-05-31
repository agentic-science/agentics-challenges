#!/bin/sh
set -eu
input_dir="${AGENTICS_INPUT_DIR:-input}"
output_dir="${AGENTICS_OUTPUT_DIR:-output}"
mkdir -p "$output_dir"
python solution.py < "$input_dir/input.bin" > "$output_dir/output.bin"
