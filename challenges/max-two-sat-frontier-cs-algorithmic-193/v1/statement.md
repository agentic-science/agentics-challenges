# Max 2-SAT

Ported from Frontier-CS `algorithmic/problems/193`.

## Agentics Interface

Each run executes the submitted `zip_project` solution once. The run command receives the case input on standard input and must write the candidate answer to standard output. The solution must not use the network during setup, build, or run.

The trusted separated evaluator compiles and runs the source-derived Frontier-CS checker against `stdout.txt`. Public validation contains one tiny deterministic case. Official cases, reference answers, and scoring metadata are supplied only through the required private asset `official-runs`.

## Scoring

The primary metric is `score`, the average normalized Frontier-CS checker score on a 0-100 scale. Outputs rejected by the checker receive zero for that case. Official result details are score-only; public validation includes per-case feedback from the checker.

## Original Statement

# Max-2-SAT

## Problem

You are given a Boolean formula in CNF form, where each clause contains exactly two literals.
Your task is to assign truth values to variables to satisfy as many clauses as possible.

## Input Format

- Line 1: two integers n and m
  (1 ≤ n ≤ 1000, 0 ≤ m ≤ 40000)
- Next m lines: two integers a b
  - Each integer is in [-n, n], non-zero
  - Positive x means variable x
  - Negative -x means ¬x

Each clause is (a ∨ b).

## Output Format

- Output exactly one line:
  - n integers x₁ x₂ … xₙ
  - each xᵢ ∈ {0, 1}
  - 1 means TRUE, 0 means FALSE

## Scoring

Let:
- m be the total number of clauses
- s be the number of satisfied clauses

Score is defined as:
- If m > 0:  score = s / m
- If m = 0:  score = 1

## Notes

- Any assignment is accepted and scored
- Satisfying all clauses yields score 1.0
