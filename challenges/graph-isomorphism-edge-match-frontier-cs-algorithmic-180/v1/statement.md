# Graph Isomorphism Edge Match

Ported from Frontier-CS `algorithmic/problems/180`.

## Agentics Interface

Each run executes the submitted `zip_project` solution once. The run command receives the case input on standard input and must write the candidate answer to standard output. The solution must not use the network during setup, build, or run.

The trusted separated evaluator compiles and runs the source-derived Frontier-CS checker against `stdout.txt`. Public validation contains one tiny deterministic case. Official cases, reference answers, and scoring metadata are supplied only through the required private asset `official-runs`.

## Scoring

The primary metric is `score`, the average normalized Frontier-CS checker score on a 0-100 scale. Outputs rejected by the checker receive zero for that case. Official result details are score-only; public validation includes per-case feedback from the checker.

## Original Statement

# Graph Isomorphism

## Problem

You are given two undirected graphs with the same number of vertices.
Your task is to find a permutation of vertices of the second graph that makes it as isomorphic as possible to the first graph.

This is the Graph Isomorphism problem, evaluated with a soft scoring rule.

## Input Format

- Line 1: two integers n and m
  (2 ≤ n ≤ 2000, 1 ≤ m ≤ n*(n-1)/2)
- Next m lines: two integers u and v
  (1 ≤ u, v ≤ n, u ≠ v)
  These describe edges of the first graph G₁. Note that there are no duplicate edges.
- Next m lines: two integers u and v
  (1 ≤ u, v ≤ n, u ≠ v)
  These describe edges of the second graph G₂. Note that there are no duplicate edges.

## Output Format

- Output exactly one line:
  - n integers p₁, p₂, ..., pₙ
  - This is a permutation of {1, 2, ..., n}
  - pᵢ = j means vertex i of G₂ is mapped to vertex j of G₁

## Scoring

Let:

- E₁ = set of edges in G₁
- E₂ = set of edges in G₂

Define:
  matched_edges = |{(u,v) : (p(u), p(v)) ∈ E₁ and (u,v) ∈ E₂}|
  total_edges = m

Your score is:
  score = matched_edges / total_edges

Notes:
- The score is always in the range [0, 1]
- Perfect isomorphism yields score = 1
- Any valid permutation is accepted and scored
