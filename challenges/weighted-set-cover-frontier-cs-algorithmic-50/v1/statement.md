# Weighted Set Cover

Choose sets covering every element while minimizing total cost.

## Solution Interface

Submit a `zip_project` solution. The run command is executed once per case, reads the case from standard input, and writes the answer to standard output. The trusted separated evaluator runs the migrated Frontier-CS Testlib checker against the submitted output and the case's evaluator-only answer or scoring metadata.

## Scoring

The leaderboard score is the average checker ratio scaled to `0..100` across official cases. Invalid outputs receive zero for the affected case. The public validation case is intentionally tiny and deterministic; official scoring uses the source-derived Frontier-CS cases packaged as private benchmark data.

## Original Statement

Time Limit: 10s
Memory Limit: 1024M

Firstly, you are given two integers n (1 <= n <= 400) and m (1 <= m <= 4000), which means that you have n elements and m sets.

After that, there are m integers, the i-th integer is the cost of choosing the i-th set.

After that, for the i-th element, firstly input an integer k_i, which means the number of sets that contain the element. After that, there

are k_i integers, the j-th integer a_j means that the set with id a_j contains the element i.

Find some sets so that each element belongs to at least one of these sets. You need to minimize the total cost of these sets. This value will determine your final score.

Output: 

Firstly output an integer |S|, which means the number of sets you choose. After that, output |S| ids of the sets you choose in another line.

