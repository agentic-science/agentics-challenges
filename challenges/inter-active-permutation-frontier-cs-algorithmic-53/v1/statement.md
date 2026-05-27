# Inter Active Permutation

This is an interactive challenge. For each test case, the evaluator hides a derangement `p` of length `n`. You choose one fixed position `k`, ask permutation queries, and must recover `p`.

The original Frontier-CS problem was interactive. This Agentics migration keeps the source `interactor.cc` protocol in a `piped_stdio` session.

## Input

The evaluator first writes the number of test cases `t`. For each test case, it writes one integer `n`. The source input file owns all multi-test framing, so there is no extra Agentics terminal marker after the last case. EOF means the session is complete.

## Output

At the start of each case, output one integer:

```text
k
```

where `1 <= k <= n`. This `k` is fixed for the case and does not count as a query.

To ask a query, output:

```text
? q_1 q_2 ... q_n
```

where `q` is a permutation of `1..n`. Then flush stdout and read one integer response from stdin. The response is the number of pairs `(i, j)` with `i < j`, `i != k`, and `p[q_i] = q_j`.

To submit the hidden permutation for the current case, output:

```text
! p_1 p_2 ... p_n
```

Then continue to the next source test case if one remains.

## Scoring

The source interactor validates the final permutation exactly. It uses the query count coded in the original interactor: a safety cap of `16n` queries per case, full ratio at `n` queries or fewer, and a quadratic drop toward zero at `20n` queries. Malformed commands, invalid permutations, safety-limit failures, or a wrong final answer receive zero. Agentics reports the average source ratio as `score` from 0 to 100.

## Solution Interface

Submit a `zip_project` solution with an `agentics.solution.json` manifest. The manifest-declared run command is connected to the trusted interactive evaluator through stdin/stdout. Network access is disabled.
