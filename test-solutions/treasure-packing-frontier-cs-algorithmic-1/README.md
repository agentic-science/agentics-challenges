# Treasure Packing Baseline Solution

Valid greedy baseline solution for `treasure-packing-frontier-cs-algorithmic-1`.

The runner reads the JSON item catalog from stdin and writes a JSON object with one count per category. It greedily packs items by value per normalized resource cost while respecting mass, volume, and quantity limits.
