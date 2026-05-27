# Bracket Sequence Recovery

This is an interactive challenge. A hidden bracket sequence `s` of length `n` contains at least one `(` and at least one `)`. You can query subsequences by index and must recover the whole string.

The original Frontier-CS problem was interactive. This Agentics migration keeps the source `interactor.cpp` protocol in a `piped_stdio` session.

## Input

For each source case, the evaluator writes one integer `n`. Public validation uses a tiny smoke case; official evaluation uses private Frontier-CS cases.

An Agentics session may contain more than one original Frontier-CS case. After you answer one case, keep reading stdin. If another positive `n` arrives, solve that case with the same protocol. When the evaluator writes `0`, the session is complete and your program should exit. EOF before the terminal marker should also be treated as the end of interaction.

## Output

To ask a query, output:

```text
0 k i_1 i_2 ... i_k
```

Then flush stdout and read one integer response from stdin. The response is `f(t)`, the number of non-empty regular bracket substrings in `t = s[i_1]s[i_2]...s[i_k]`. Indices may repeat. Each query must satisfy `1 <= k <= 1000` and `1 <= i_j <= n`.

To guess the current hidden sequence, output:

```text
1 s
```

The guess does not count as a query. For a multi-case Agentics session, continue reading after each guess until the evaluator sends terminal `n = 0`.

## Scoring

The source interactor allows at most `200` queries per case. If the final string is correct, the source ratio is `(200 - q) / 200`, where `q` is the number of queries. Protocol errors, too many queries, invalid indices, or a wrong final string receive zero for the affected case. Agentics reports the average source ratio as `score` from 0 to 100.

## Solution Interface

Submit a `zip_project` solution with an `agentics.solution.json` manifest. The manifest-declared run command is connected to the trusted interactive evaluator through stdin/stdout. Network access is disabled.
