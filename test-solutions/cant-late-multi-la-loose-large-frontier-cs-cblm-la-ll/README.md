# Deadline-aware multi-region spot baseline for cant-late-multi-la-loose-large-frontier-cs-cblm-la-ll

This baseline reads the evaluator-provided deadline and restart overhead, uses spot instances when any currently available region can provide them, and falls back to on-demand when the remaining deadline slack becomes too tight for another restart.
