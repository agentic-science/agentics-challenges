# Magic Word Spells

This is an interactive `zip_project` challenge. The trusted evaluator starts a case by printing:

```text
n q
```

Print `n` distinct magic words, one per line. Each word must contain only `X` and `O`, and each length must be between `1` and `30n`, inclusive. Flush after printing the words.

For each of the `q` students, the evaluator prints one integer `p`: the number of distinct non-empty substrings in the concatenation of an evaluator-owned ordered pair of your words. You must reply with the exact ordered pair:

```text
u v
```

Indices are 1-based, and order matters. Flush after each pair. In Agentics official evaluation, a session may contain multiple source cases; after the last answer for one case, the next case starts immediately with another `n q` line. Exit on EOF.

Malformed words, duplicate words, length violations, invalid pair indices, wrong ordered pairs, and EOF are handled by the source interactor. The source score for a case is `(30n^2 - total_length) / (30n^2 - optimal_total_length)`, clamped by the original interactor, and Agentics reports that ratio scaled to `score` from 0 to 100. The trusted evaluator writes `result.json`.
