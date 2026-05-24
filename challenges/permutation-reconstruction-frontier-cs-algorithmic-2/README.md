# Permutation Reconstruction

Recover a hidden permutation through a trusted interactive Agentics interactor. The submitted ZIP project communicates only through stdin/stdout.

The interactor first prints `n`. A query line starts with `0` followed by `n` integers in `[1, n]`; the interactor replies with the number of exact-position matches against the hidden permutation. A final answer starts with `1` followed by a valid permutation.

## Provenance

This challenge is migrated from Frontier-CS:

- `algorithmic/problems/2`
- Original title: Permutation
- Original shape: C++ `testlib` interactor with hidden `.ans` permutations and query-count scoring.

The Agentics version uses `piped_stdio`: the trusted interactor owns private session data, communicates with one participant run container, and writes the evaluator result JSON.

## Files

- `v1/spec.json` declares the challenge bundle.
- `v1/statement.md` is the submitter-facing statement.
- `v1/public/session.json` contains the small public validation session.
- `v1/interactor/run.py` implements the trusted protocol and scoring.

Official hidden permutations are uploaded as a private asset overlay and are not committed.
