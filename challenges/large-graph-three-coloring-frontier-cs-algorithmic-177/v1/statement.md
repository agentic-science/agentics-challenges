# Large Graph 3-Coloring

Ported from Frontier-CS `algorithmic/problems/177`.

## Agentics Interface

Each run executes the submitted `zip_project` solution once. The run command receives the case input on standard input and must write the candidate answer to standard output. The solution must not use the network during setup, build, or run.

The trusted separated evaluator compiles and runs the source-derived Frontier-CS checker against `stdout.txt`. Public validation contains one tiny deterministic case. Official cases, reference answers, and scoring metadata are supplied only through the required private asset `official-runs`.

## Scoring

The primary metric is `score`, the average normalized Frontier-CS checker score on a 0-100 scale. Outputs rejected by the checker receive zero for that case. Official result details are score-only; public validation includes per-case feedback from the checker.

## Original Statement

# Graph 3-Coloring

## Problem

You are given an undirected graph with n vertices and m edges.
Your task is to assign each vertex one of three colors.

The objective is to minimize the number of conflicting edges.
An edge is conflicting if its two endpoints have the same color.

## Input Format

- Line 1: two integers n and m (1 ≤ n ≤ 60000, 0 ≤ m ≤ 200000)
- Next m lines: two integers u v (1 ≤ u, v ≤ n, u ≠ v)
The graph may be disconnected.
There are no multiple edges or self-loops.

## Output Format

- Output exactly one line:
  - n integers c₁ c₂ … cₙ
  - each cᵢ ∈ {1, 2, 3}

## Scoring

Let:
- m be the number of edges
- b be the number of conflicting edges

Score is defined as:
- If m > 0:  score = 1 − b / m
- If m = 0:  score = 1

The score is clamped to [0, 1].
