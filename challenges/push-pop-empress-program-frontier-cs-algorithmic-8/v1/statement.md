# The Empress

Write a compact Push-Pop program that halts after exactly the requested odd number of steps.

## Solution Interface

Submit a `zip_project` solution. The run command is executed once per case, reads the case from standard input, and writes the answer to standard output. The trusted separated evaluator runs the migrated Frontier-CS Testlib checker against the submitted output and the case's evaluator-only answer or scoring metadata.

## Scoring

The leaderboard score is the average checker ratio scaled to `0..100` across official cases. Invalid outputs receive zero for the affected case. The public validation case is intentionally tiny and deterministic; official scoring uses the source-derived Frontier-CS cases packaged as private benchmark data.

## Original Statement

The Empress

Capoo invented an interesting language named Push-Pop. This language is an interpreted language. The interpreter starts with an empty stack with infinite capacity and reads the first instruction of the custom program. There are only two kinds of instructions in this language:

POP a GOTO x PUSH b GOTO y

If the top element of the stack is a, then pop the stack once and transfer the control flow to the x-th instruction (which means the next instruction will be the x-th).

Otherwise, push an element b into the stack and transfer the control flow to the y-th instruction.

HALT PUSH b GOTO y

If the stack is empty, halt the whole program after executing this instruction. Otherwise, push an element b into the stack and transfer the control flow to the y-th instruction. Capoo wants to construct a Push-Pop program that halts after executing exactly k instructions. A program can contain at most 512 instructions. Then, let n be the number of instructions, your score will be (512 - n) / 512.

Input

The only line contains a single integer k (1 <= k <= 2^31 − 1, k is odd).

Output

The first line contains an integer n (1 <= n <= 512) denoting the number of instructions, and then follows n lines denoting the Push-Pop program. For each instruction, 1 <= a, b ≤ 1024, 1 <= x, y <= n should hold. It is guaranteed that a solution exists for given input.

Example Input 1:

1

Example Output 1:

1
HALT PUSH 1 GOTO 1

Example Input 2:

5

Example Output 2:

5
POP 1 GOTO 2 PUSH 1 GOTO 2
HALT PUSH 1 GOTO 3
POP 1 GOTO 4 PUSH 2 GOTO 4
POP 1 GOTO 2 PUSH 2 GOTO 4
HALT PUSH 99 GOTO 4

