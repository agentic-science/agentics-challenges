# Big Integer Subset Sum

Ported from Frontier-CS `algorithmic/problems/179`.

## Agentics Interface

Each run executes the submitted `zip_project` solution once. The run command receives the case input on standard input and must write the candidate answer to standard output. The solution must not use the network during setup, build, or run.

The trusted separated evaluator compiles and runs the source-derived Frontier-CS checker against `stdout.txt`. Public validation contains one tiny deterministic case. Official cases, reference answers, and scoring metadata are supplied only through the required private asset `official-runs`.

## Scoring

The primary metric is `score`, the average normalized Frontier-CS checker score on a 0-100 scale. Outputs rejected by the checker receive zero for that case. Official result details are score-only; public validation includes per-case feedback from the checker.

## Original Statement

# Subset Sum

## Problem

You are given a multiset of non-negative integers.
Your task is to choose a subset whose sum is as close as possible to a given target value W.

This is the classic Subset Sum problem, evaluated with a soft scoring rule.

## Input Format

- Line 1: two integers n and W
  (1 ≤ n ≤ 2100)
- Line 2: n integers a₁, a₂, ..., aₙ
  - aᵢ ≥ 0
  - All numbers (including W and aᵢ) can be up to 10^1100.

## Output Format

- Output exactly one line:
  - n integers b₁, b₂, ..., bₙ
  - each bᵢ ∈ {0, 1}
  - bᵢ = 1 means aᵢ is selected into the subset
  - bᵢ = 0 means aᵢ is not selected

## Scoring

Let:

- S = sum of all aᵢ where bᵢ = 1
- M = max(aᵢ) over all i

Your goal is to make S as close to W as possible.

Score is defined as:

  score = max(0, 1 - |W - S| / (W + M))

Notes:
- The score is always in the range [0, 1]
- Achieving S = W yields score = 1
- Any valid output is accepted and scored

## Hint

- Large integer arithmetic may be required
