# Three-Hop Shortcut DAG

This is an Agentics migration of Frontier-CS algorithmic problem 239.

Your submitted `zip_project` run command is executed once per case. It receives exactly one case on stdin and must write the candidate answer to stdout. Do not read or write challenge-owned files. Network access is unavailable during setup, build, and run.

The trusted separated evaluator uses the original Frontier-CS Testlib checker. Public validation is intentionally small and only checks the interface. Official scoring uses the private Frontier-CS-derived run manifest.

## Original Statement

Problem Description:
You are given a directed graph G on vertices numbered $0$ to $n$. Initially, G contains exactly n edges of the
form $v → v + 1$. Your task is to add some edges to this graph in such a way that for every two vertices
$v, u (v < u)$ there exists a directed path from v to u consisting of at most three edges. You can add an edge $a → c$ if and only if there exists such $b$ that edges $a → b$ and $b → c$ are already
present in $G$.

find the minimum edges you need to add such that  for every two vertices
$v, u (v < u)$ there exists a directed path from v to u consisting of at most three edges

Input 
Input a single line contains a single integer $n(0\leq n \leq 2^{12})$

Output
First line contains a single integer $m$

Following $m$ lines, each line contains a three integer $u, c, v$, representing there is an edge from $u$ to $c$, and an edge from $c$ to v, you add an edge from $u$ to $v$

Example 1:
Input:
5

Output:
2
2 3 4
1 2 4

Scoring:
Your score is calculated based on the number of edges $m$, and $m_0$(edges by std):
if $m \leq m_0$, you receive full score (1.0).
if $m>3 * m_0$, you receive 0 score.
otherwise Score = $(3 * m_0 - m) / (2 * m_0)$, linearly decreasing from 1.0 to 0.0.

Time limit:
2 seconds

Memory limit:
512 MB
