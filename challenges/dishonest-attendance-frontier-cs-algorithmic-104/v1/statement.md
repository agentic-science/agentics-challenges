# Dishonest Attendance

This is an interactive challenge. The evaluator first prints `t`, then for each independent test case prints `n`. Exactly one student is absent, but the evaluator may adaptively keep several possibilities as long as all previous answers remain consistent with the Frontier-CS dishonesty constraints.

To ask an interval attendance query, print one line:

```text
? l r
```

`1 <= l <= r <= n`. The evaluator replies with either `r-l` or `r-l+1`, representing the number of students who raised their hands. Across any three consecutive interval queries for the true absent student, the answers are never all honest and never all dishonest. Each test case has the original source query limit from its hidden answer file.

To guess an absent student, print one line:

```text
! a
```

The evaluator replies `1` if `a` is now forced as the absent student, otherwise `0` and removes that candidate. You may make at most two guesses per test case. After a successful guess, print:

```text
#
```

Then continue to the next test case. After all source cases in the Agentics session are complete, exit on EOF.

The trusted evaluator owns the adaptive candidate state, validates query and guess limits, enforces the final `#`, and writes `result.json`. The source score is based on the worst per-test-case ratio `(query_limit - queries) / (query_limit - 1)`, clamped to 0..1 and scaled to `score` from 0 to 100.
