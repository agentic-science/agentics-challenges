# Black and White Components

Draw a bounded grid with the requested black and white component counts at low weighted area.

## Solution Interface

Submit a `zip_project` solution. The run command is executed once per case, reads the case from standard input, and writes the answer to standard output. The trusted separated evaluator runs the migrated Frontier-CS Testlib checker against the submitted output and the case's evaluator-only answer or scoring metadata.

## Scoring

The leaderboard score is the average checker ratio scaled to `0..100` across official cases. Invalid outputs receive zero for the affected case. The public validation case is intentionally tiny and deterministic; official scoring uses the source-derived Frontier-CS cases packaged as private benchmark data.

## Original Statement

Black and White

Time limit: 2 seconds
Memory limit: 256 megabytes

------------------------------------------------------------
The jury has a great artistic idea — to create a rectangular
panel out of a huge pile of black and white squares of the
same size. The panel should have exactly b 4-connected areas
made of black tiles, and w 4-connected areas made of white tiles.

A 4-connected area of some color is a maximal set of the
panel tiles such that:
• any two tiles of the area share the same color;
• for any two tiles of the area there is a tile sequence
  connecting them, such that any two consecutive tiles of
  the sequence share a common side.

You will also be given two integers x, y. Try to minimize x * (the number of black tiles in your grid) + y * (the number of white tiles in your grid).

------------------------------------------------------------
Input
------------------------------------------------------------
The only line of the input file contains four integers b, w —
number of black and white areas (1 ≤ b, w ≤ 1000) and x, y - grading coefficients (1 ≤ x, y ≤ 1000).

------------------------------------------------------------
Output
------------------------------------------------------------
The first line of the output file should contain the picture sizes
r and c — the number of rows and columns (1 ≤ r, c ≤ 100 000).
This line should be followed by r lines of c symbols each.
Each symbol should be either '@' (for black tile) or '.' (for
white one). There should be no more than 100 000 tiles in
the panel.

------------------------------------------------------------
Example
------------------------------------------------------------
Input:
2 3 5 6

Output:
6 7
@@@@@@@
@.@@@@@
@@...@@
@@@@@@@
.......
@@@@@@@

