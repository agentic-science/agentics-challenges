# Symbolic Regression Sincos

Ported from Frontier-CS `research/problems/symbolic_regression/sincos`.

## Agentics Interface

Submit a ZIP project containing the source interface described below. The trusted evaluator imports or compiles participant code from `/workspace`, so this challenge uses `coexecuted_benchmark` with `acknowledge_danger: true`.

## Public And Official Data

Public validation uses a small deterministic configuration committed under `v1/public`. Official scoring uses the private `official-runs` overlay under `private-benchmark/`.

## Original Statement

Symbolic Regression Benchmark - SinCos Dataset
===============================================

Problem Setting
---------------
Learn a closed-form symbolic expression `f(x1, x2)` that predicts the target `y`.

This dataset features a function built from basic trigonometric operations. The target exhibits periodic behavior in both input dimensions, representing a straightforward but fundamental pattern for symbolic regression.

Input Format
------------
- Your `Solution.solve` receives:
  - `X`: numpy.ndarray of shape `(n, 2)` containing feature values
  - `y`: numpy.ndarray of shape `(n,)` containing target values
- Dataset columns: `x1, x2, y`

Output Specification
--------------------
Implement a `Solution` class in `solution.py`:

```python
import numpy as np

class Solution:
    def __init__(self, **kwargs):
        pass

    def solve(self, X: np.ndarray, y: np.ndarray) -> dict:
        """
        Args:
            X: Feature matrix of shape (n, 2)
            y: Target values of shape (n,)

        Returns:
            dict with keys:
              - "expression": str, a Python-evaluable expression using x1, x2
              - "predictions": list/array of length n (optional)
              - "details": dict with optional "complexity" int
        """
        # Example: fit a symbolic expression to the data
        expression = "x1 + x2"  # placeholder
        return {
            "expression": expression,
            "predictions": None,  # will be computed from expression if omitted
            "details": {}
        }
```

Expression Requirements:
- Must be a valid Python expression string
- Use variable names: `x1`, `x2`
- Allowed operators: `+`, `-`, `*`, `/`, `**`
- Allowed functions: `sin`, `cos`, `exp`, `log`
- Numeric constants are allowed

Agentics Runtime
----------------
The Agentics evaluator runtime provides `numpy`, `pandas`, and `sympy`. PySR
and Julia are not installed by the evaluator setup phase, so submitted
solutions must not rely on evaluator-provided PySR unless they vendor their own
compatible runtime inside the ZIP project.

Minimal Working Examples
------------------------

**Manual expression (simple baseline)**
```python
import numpy as np

class Solution:
    def __init__(self, **kwargs):
        pass

    def solve(self, X: np.ndarray, y: np.ndarray) -> dict:
        # Simple linear combination as baseline
        x1, x2 = X[:, 0], X[:, 1]

        # Fit coefficients via least squares
        A = np.column_stack([x1, x2, np.ones_like(x1)])
        coeffs, _, _, _ = np.linalg.lstsq(A, y, rcond=None)
        a, b, c = coeffs

        expression = f"{a:.6f}*x1 + {b:.6f}*x2 + {c:.6f}"
        predictions = a * x1 + b * x2 + c

        return {
            "expression": expression,
            "predictions": predictions.tolist(),
            "details": {}
        }
```

Expression Format Requirements
------------------------------
- Must be a valid Python expression string
- Use variable names: `x1`, `x2`
- Allowed operators: `+`, `-`, `*`, `/`, `**`
- Allowed functions: `sin`, `cos`, `exp`, `log` (NO `np.` prefix)
- Numeric constants are allowed
- The evaluator uses `sympy.sympify()` to parse your expression

Scoring
-------
```
MSE = (1/n) Σ (y_i - ŷ_i)²
Score = 100 × clamp((m_base - MSE) / (m_base - m_ref), 0, 1) × 0.99^max(C - C_ref, 0)
```

- `m_base`: linear regression baseline MSE
- `m_ref`, `C_ref`: reference solution MSE and complexity
- `C = 2 × (#binary ops) + (#unary ops)`
- Lower MSE and lower complexity yield higher scores

Environment
-----------
The evaluator setup phase creates the Agentics runtime described above with uv.
