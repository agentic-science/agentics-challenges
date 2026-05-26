# Binary Quadratic Assignment

Ported from Frontier-CS `algorithmic/problems/181`.

## Agentics Interface

Each run executes the submitted `zip_project` solution once. The run command receives the case input on standard input and must write the candidate answer to standard output. The solution must not use the network during setup, build, or run.

The trusted separated evaluator compiles and runs the source-derived Frontier-CS checker against `stdout.txt`. Public validation contains one tiny deterministic case. Official cases, reference answers, and scoring metadata are supplied only through the required private asset `official-runs`.

## Scoring

The primary metric is `score`, the average normalized Frontier-CS checker score on a 0-100 scale. Outputs rejected by the checker receive zero for that case. Official result details are score-only; public validation includes per-case feedback from the checker.

## Original Statement

# Binary Quadratic Assignment Problem

## Problem

You are given two n×n binary matrices: a distance matrix D and a flow matrix F (both containing only 0s and 1s).
Your task is to assign n facilities to n locations (a permutation) to minimize the total cost.

This is a binary version of the Quadratic Assignment Problem.

## Input Format

- Line 1: one integer n (2 ≤ n ≤ 2000)
- Next n lines: each line contains n integers (0 or 1), representing one row of the distance matrix D
- Next n lines: each line contains n integers (0 or 1), representing one row of the flow matrix F

## Output Format

- Output exactly one line: n integers p₁, p₂, ..., pₙ
- This is a permutation of {1, 2, ..., n}
- pᵢ = j means facility i is assigned to location j

## Scoring

Let:

- Cost = Σᵢ Σⱼ D[p(i), p(j)] * F[i, j]
- TotalFlow = Σᵢ Σⱼ F[i, j]  (sum of all elements in F)

Your score is:
  score = 1 - Cost / TotalFlow
