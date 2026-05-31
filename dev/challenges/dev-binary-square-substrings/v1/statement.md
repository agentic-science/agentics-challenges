# Binary Square-Count Substrings

This is an Agentics migration of Frontier-CS algorithmic problem 228.

Your submitted `zip_project` run command is executed once per case. It receives exactly one case on stdin and must write the candidate answer to stdout. Do not read or write challenge-owned files. Network access is unavailable during setup, build, and run.

The trusted separated evaluator uses the original Frontier-CS Testlib checker. Public validation is intentionally small and only checks the interface. Official scoring uses the private Frontier-CS-derived run manifest.

## Original Statement

You are given a 01-string (a string consisting only of characters '0' and '1').

You need to find the number of substrings such that the number of '0's in the substring is equal to the square of the number of '1's.

### Input
A single line containing a 01-string.
The length of the string is at most $2 \times 10^6$.

### Output
Output a single line containing the answer.

### Scoring
- Assume the ground truth answer is $ans$, and your answer is $cnt$.
- Your score is $max(0, 1 - \log_2(abs(cnt - ans) + 1) / 10)$.
