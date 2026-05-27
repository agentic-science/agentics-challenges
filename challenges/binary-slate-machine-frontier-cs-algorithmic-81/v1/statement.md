# Binary Slate Machine

This is an interactive challenge. A hidden binary string `S` is written on a stone slate. Your program communicates with a trusted machine and must recover `S`.

The original Frontier-CS problem was interactive. This Agentics migration keeps the source `interactor.cc` protocol in a `piped_stdio` session.

## Input

The evaluator first writes one integer `N`, the length of `S`. Public validation
uses a tiny smoke case; official Frontier-CS cases use `N = 1000`.

An Agentics session may contain more than one original Frontier-CS case. After
you guess one string, keep reading stdin. If another positive `N` arrives, solve
that case with the same protocol. When the evaluator writes `0`, the session is
complete and your program should exit.

## Output

To make a query, output:

```text
1 m a_0 a_1 ... a_{m-1} b_0 b_1 ... b_{m-1}
```

Then flush stdout and read one integer response from stdin. Each query must satisfy:

- `1 <= m <= 1002`
- each `a_i` and `b_i` is an integer in `[0, m)`

The machine starts with memory value `0`, processes the hidden string from left to right, moves to `a_x` on bit `0` and `b_x` on bit `1`, and returns the final memory value.

To guess the current string, output:

```text
0 S
```

The guess does not count as a query. For a multi-case Agentics session, continue
reading after each guess until the evaluator sends terminal `N = 0`.

## Scoring

The source interactor allows at most `1000` queries. It validates the final string exactly and reports `query_m_max`, the largest query `m` you used. If the guess is correct, the source score is based on `query_m_max`; using no query is treated as `M = 0`, and `M <= 102` receives full score. Protocol errors, too many queries, invalid query values, or a wrong final string receive zero.

## Solution Interface

Submit a `zip_project` solution with an `agentics.solution.json` manifest. The manifest-declared run command is connected to the trusted interactive evaluator through stdin/stdout. Network access is disabled.
