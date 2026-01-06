"""
golden_section_search.py

Golden-section search for one-dimensional optimization with a small
command-line interface (CLI).

This script finds the minimum or maximum of a unimodal function over a
closed interval [a, b] using the golden-section search algorithm.
The function may be supplied either as:
  1) A built-in example function, or
  2) A user-defined mathematical expression in the variable `x`

The golden-section search is a derivative-free optimization method that:
- Requires only function evaluations
- Assumes the function is unimodal on [a, b]
- Shrinks the search interval by a fixed ratio each iteration

-----------------------------------------------------------------------
USAGE
-----------------------------------------------------------------------
Minimize a user-supplied expression:
  python golden_section_search.py \
      --expr "(x-2)**2 + math.sin(x)" \
      --a -5 --b 5

Maximize a built-in example:
  python golden_section_search.py \
      --example quadratic \
      --a -10 --b 10 \
      --maximize

Adjust convergence tolerance:
  python golden_section_search.py \
      --example wavy \
      --a -2 --b 3 \
      --tol 1e-6

-----------------------------------------------------------------------
FUNCTION EXPRESSIONS
-----------------------------------------------------------------------
When using --expr, the expression is evaluated with restricted globals
for safety. The following names are available:

  - x            : independent variable
  - math         : math module
  - sin, cos
  - exp, log
  - sqrt

Example valid expressions:
  "(x - 2)**2"
  "math.sin(x) + 0.1*x"
  "(x - 1)**2 + math.exp(-x)"

WARNING:
Expressions are evaluated using eval(). Although builtins are disabled,
this should only be used with trusted input.

-----------------------------------------------------------------------
ASSUMPTIONS & LIMITATIONS
-----------------------------------------------------------------------
- The function must be unimodal on [a, b]
- The interval endpoints a < b are required
- The reported result is approximate, controlled by --tol
- The original interval [a, b] is not modified outside the algorithm

-----------------------------------------------------------------------
DEPENDENCIES
-----------------------------------------------------------------------
Python standard library only:
  - math
  - argparse
  - typing

-----------------------------------------------------------------------
AUTHOR / INTENT
-----------------------------------------------------------------------
Educational and demonstration code for numerical optimization and
Python CLI design.
"""
