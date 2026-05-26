# Almost Monochromatic Cycle

Find a permutation whose cycle colors change at most once in a symmetric binary matrix.

## Solution Interface

Submit a `zip_project` solution. The run command is executed once per case, reads the case from standard input, and writes the answer to standard output. The trusted separated evaluator runs the migrated Frontier-CS Testlib checker against the submitted output and the case's evaluator-only answer or scoring metadata.

## Scoring

The leaderboard score is the average checker ratio scaled to `0..100` across official cases. Invalid outputs receive zero for the affected case. The public validation case is intentionally tiny and deterministic; official scoring uses the source-derived Frontier-CS cases packaged as private benchmark data.

## Original Statement

Time limit: 1 seconds
Memory limit: 512 megabytes
Bobo has an n×n symmetric matrix C consisting of zeros and ones. For a permutation p_1, ..., p_n of 1, ..., n, let c_i=(C_{p_i, p_{i+1}} for 1 ≤ i < n, C_{p_n, p_1} for i = n).
The permutation p is almost monochromatic if and only if the number of indices i (1 ≤ i < n) where c_i ̸= c_{i+1} is at most one.
Find an almost monochromatic permutation p_1, ... p_n for the given matrix C.

Input
The input consists of several test cases terminated by end-of-file. For each test case,
The first line contains an integer n.
For the following n lines, the i-th line contains n integers C_{i,1}, ..., C_{i,n}.
 •3≤n≤2000
 •C_{i,j} ∈ {0,1} for each1 ≤ i,j ≤ n
 •C_{i,j} = C_{j,i} for each1 ≤ i,j ≤ n
 •C_{i,i} = 0 for each 1 ≤ i ≤ n
 •In each input, the sum of n does not exceed 2000.

Output
For each test case, if there exists an almost monochromatic permutation, out put n integers p_1, ..., p_n which denote the permutation. Otherwise, output -1.
If there are multiple almost monochromatic permutations, you need to minimize the lexicographical order. Basically, set S = n * p_1 + (n - 1) * p_2 + ... + 1 * p_n, your score is inversely linear related to S.

SampleInput
3
001
000
100
4
0000
0000
0000
0000
SampleOutput
3 1 2
2 4 3 1

Note
For the first test case, c1 = C_{3,1} = 1, c2 = C_{1,2} = 0, c3 = C_{2,3} = 0. Only when i=1, c_i ̸= c_{i+1}.Therefore, the permutation 3,1,2 is an almost monochromatic permutation

