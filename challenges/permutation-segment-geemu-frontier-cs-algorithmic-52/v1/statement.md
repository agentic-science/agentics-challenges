# Permutation Segment Geemu

This is an interactive challenge. The evaluator hides a permutation `p` of length `n`. You may query how many value-contiguous segments appear in a current interval and may swap positions in the current hidden state. Your final report must match the current permutation or the source-accepted reverse-value equivalent.

The original Frontier-CS problem was interactive. This Agentics migration keeps the source `interactor.cc` protocol in a `piped_stdio` session.

## Input

For each source case, the evaluator writes:

```text
n l1 l2
```

where `l1` is the maximum number of ask operations and `l2` is the maximum number of swap operations. Public validation uses a tiny smoke case; official evaluation uses private Frontier-CS cases.

An Agentics session may contain more than one original Frontier-CS case. After you report one permutation, keep reading stdin. If another positive `n l1 l2` arrives, solve that case with the same protocol. When the evaluator writes `0 0 0`, the session is complete and your program should exit. EOF before the terminal marker should also be treated as the end of interaction.

## Output

To query the number of value-contiguous segments in the current interval `[l, r]`, output:

```text
1 l r
```

Then flush stdout and read one integer response from stdin.

To swap positions `i` and `j` in the current hidden permutation, output:

```text
2 i j
```

Then flush stdout and read confirmation `1`.

To submit the current permutation, output:

```text
3 p_1 p_2 ... p_n
```

The report must be a valid permutation. The source interactor accepts either the current permutation or the value-reversed permutation `n - p_i + 1`.

## Scoring

Let `s1` be the number of ask operations and `s2` be the number of swap operations. The source interactor returns zero if `s1 > l1`, `s2 > l2`, the command is malformed, or the reported permutation is invalid or wrong. Otherwise the source ratio is `min((r1 + r2 + 1) / (s1 + s2 + 1), 1)`, where `r1` and `r2` are the private reference costs from the source answer file. Agentics reports the average source ratio as `score` from 0 to 100.

## Solution Interface

Submit a `zip_project` solution with an `agentics.solution.json` manifest. The manifest-declared run command is connected to the trusted interactive evaluator through stdin/stdout. Network access is disabled.
