# Permutation Reconstruction

Recover a hidden permutation through a trusted Agentics interactive-evaluator. The submitted ZIP project communicates only through stdin/stdout.

The interactive-evaluator first prints `n`. A query line starts with `0` followed by `n` integers in `[1, n]`; the interactive-evaluator replies with the number of exact-position matches against the hidden permutation. A final answer starts with `1` followed by a valid permutation.

## Provenance

This challenge is migrated from Frontier-CS:

- `algorithmic/problems/2`
- Original title: Permutation
- Original shape: C++ `testlib` interactive-evaluator with hidden `.ans` permutations and query-count scoring.

The Agentics version uses `piped_stdio`: the trusted interactive-evaluator owns private session data, communicates with one participant run container, and writes the evaluator result JSON.

## Files

- `v1/spec.json` declares the challenge bundle.
- `v1/statement.md` is the submitter-facing statement.
- `v1/public/session.json` contains the small public validation session.
- `v1/interactive-evaluator/run.py` implements the trusted protocol and scoring.

Official hidden permutations are uploaded as a private asset overlay and are not committed.
