# Rectangle-Free Points

You are given an `n` by `m` grid. Select as many cells as you can while avoiding every axis-aligned rectangle: there must not be two distinct rows `r1`, `r2` and two distinct columns `c1`, `c2` such that all four cells `(r1, c1)`, `(r1, c2)`, `(r2, c1)`, and `(r2, c2)` are selected.

## Input

Each run receives one grid size on stdin:

```text
n m
```

`n` and `m` are positive integers. Official cases satisfy `n * m <= 100000`.

## Output

Write:

```text
k
r_1 c_1
...
r_k c_k
```

`k` is the number of selected cells. Each coordinate must satisfy `1 <= r_i <= n` and `1 <= c_i <= m`. All listed cells must be distinct. Extra output tokens are rejected.

## Scoring

Let:

```text
U(n, m) = floor(min(n * sqrt(m) + m, m * sqrt(n) + n, n * m))
```

Each valid case scores:

```text
100 * min(k / (1.5 * U(n, m)), 1)
```

Higher is better. Invalid cases contribute `0` to the official average.

## Public Validation

Public validation uses tiny deterministic grids. Official scoring uses hidden Frontier-CS grid sizes uploaded as private benchmark data.
