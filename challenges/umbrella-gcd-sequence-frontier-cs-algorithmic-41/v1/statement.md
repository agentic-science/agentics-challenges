# Umbrella GCD Sequence

Construct a high-value increasing sequence with strictly increasing adjacent gcds.

## Solution Interface

Submit a `zip_project` solution. The run command is executed once per case, reads the case from standard input, and writes the answer to standard output. The trusted separated evaluator runs the migrated Frontier-CS Testlib checker against the submitted output and the case's evaluator-only answer or scoring metadata.

## Scoring

The leaderboard score is the average checker ratio scaled to `0..100` across official cases. Invalid outputs receive zero for the affected case. The public validation case is intentionally tiny and deterministic; official scoring uses the source-derived Frontier-CS cases packaged as private benchmark data.

## Original Statement

# Problem

Anton owns \(n\) umbrellas, each labeled with a distinct integer from \(1\) to \(n\). He wants to arrange some of them in a line to form a brilliant sequence of umbrellas (BSU).

A sequence of \(k\) umbrellas with numbers \(a_1, a_2, \ldots, a_k\) is a BSU if:

- \(a_i > a_{i-1}\) for all \(2 \le i \le k\);
- \(\gcd(a_i, a_{i-1}) > \gcd(a_{i-1}, a_{i-2})\) for all \(3 \le i \le k\).

Here, \(\gcd(x, y)\) denotes the greatest common divisor of integers \(x\) and \(y\).

## Input
A single line containing an integer \(n\) — the number of umbrellas \((1 \le n \le 10^{12})\).

## Output
Print two lines:

- The first line should contain an integer \(k\), the length of your BSU \((1 \le k \le 10^6)\).
- The second line should contain \(k\) integers \(a_1, a_2, \ldots, a_k\) \((1 \le a_i \le n)\), forming a valid BSU.

## Goal
Maximize the objective:
\[
V \;=\; \text{length}(\text{BSU}) \times \sum_{i=1}^{k} a_i \;=\; k \times \Big(\sum_{i=1}^{k} a_i\Big).
\]

## Scoring
We compare your objective value \(V_{\text{you}}\) with a fixed baseline heuristic’s value \(V_{\text{base}}\) on the same test. There is **no** best/optimal reference in scoring.

Your score for a test is:
\[
\text{score} \;=\; 100 \times \min\!\left(\frac{V_{\text{you}}}{1.05 \times V_{\text{base}}},\, 1\right).
\]

Thus, reaching \(1.05 \times V_{\text{base}}\) yields a score of 100. Your final score is the average over all tests. Invalid outputs (violating constraints) receive 0 for that test.

## Time limit
1 second

## Memory limit
512 MB

## Sample
**Input**
22
**Output**
5
1 2 4 8 16

(The sample only illustrates format and validity; it is not necessarily optimal for the new objective.)

