# Random Subset Sum

Choose a subset whose sum is as close as possible to a target.

## Solution Interface

Submit a `zip_project` solution. The run command is executed once per case, reads the case from standard input, and writes the answer to standard output. The trusted separated evaluator runs the migrated Frontier-CS Testlib checker against the submitted output and the case's evaluator-only answer or scoring metadata.

## Scoring

The leaderboard score is the average checker ratio scaled to `0..100` across official cases. Invalid outputs receive zero for the affected case. The public validation case is intentionally tiny and deterministic; official scoring uses the source-derived Frontier-CS cases packaged as private benchmark data.

## Original Statement

Given (1 <= n <= 1e2) and (B = 1e15), n integers a_1 … a_n (0 <= a_i <= B) drawn from either (normal, uniform, pareto, exponential) distributions, find a subset of a_1..a_n that sums as close as possible to T=x_i*a_i, x_i drawn from Bernoulli (1/2).

Score = 100 * (15 - log(error + 1)) / 15

25% of the test cases will be from U(0, B)
25% of the test cases will be from N(B/2, B/6)
25% of the test cases will be from Exp(B/2)
25% of the test cases will be from TruncatedPareto(m=B/3, alpha=2, max=B)

Input: 
n T
A_1 a_2 a_3 a_4 .. a_n



Output: 
Print a binary string of length n, denoting the subset selection.

Sample input: 
3 4
1 2 3

Sample output:
101

