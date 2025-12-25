"""
golden_section_search.py

Simple implementation of the golden-section search for 1D optimization
(with a small CLI). Supports minimizing or maximizing a user-supplied
expression (evaluated safely with math functions) or choosing a built-in
example function.

Usage examples:
  python golden_section_search.py --expr " (x-2)**2 + math.sin(x) " --a -5 --b 5
  python golden_section_search.py --example quadratic --a -10 --b 10 --tol 1e-6

Warning: when using --expr the expression is evaluated with restricted
globals. You can use `math` (e.g. math.sin, math.exp) and the name `x`.
"""

from __future__ import annotations
import math
import argparse
from typing import Callable, Tuple


def golden_section_search(
    f: Callable[[float], float],
    a: float,
    b: float,
    tol: float = 1e-5,
    max_iter: int = 1000,
    minimize: bool = True,
) -> Tuple[float, float, int]:
    """
    Golden-section search for a unimodal function on [a, b].

    Returns (x_opt, f_opt, iterations).

    If minimize is False the algorithm searches for a maximum.
    """
    if a >= b:
        raise ValueError("Require a < b for the search interval")

    # golden ratio constant
    gr = (math.sqrt(5) - 1) / 2  # ~0.618...
    c = b - gr * (b - a)
    d = a + gr * (b - a)
    fc = f(c)
    fd = f(d)
    it = 0

    while (b - a) > tol and it < max_iter:
        # For minimization: if fc < fd -> minimum in [a, d] -> move b = d
        # For maximization, reverse the comparisons.
        if minimize:
            if fc < fd:
                b, d, fd = d, c, fc
                c = b - gr * (b - a)
                fc = f(c)
            else:
                a, c, fc = c, d, fd
                d = a + gr * (b - a)
                fd = f(d)
        else:
            if fc > fd:
                b, d, fd = d, c, fc
                c = b - gr * (b - a)
                fc = f(c)
            else:
                a, c, fc = c, d, fd
                d = a + gr * (b - a)
                fd = f(d)
        it += 1

    # Pick the better of c and d
    if (fc < fd) == minimize:
        x_opt, f_opt = c, fc
    else:
        x_opt, f_opt = d, fd

    return x_opt, f_opt, it


# Small library of example functions
def example_quadratic(x: float) -> float:
    return (x - 2.0) ** 2 + 1.0


def example_wavy(x: float) -> float:
    return (x - 0.5) ** 2 + math.sin(3 * x)


def make_function_from_expr(expr: str) -> Callable[[float], float]:
    """
    Create a function f(x) by evaluating the expression string.

    Allowed symbols in the expression:
      - math (module)
      - math functions: sin, cos, exp, log, sqrt (available via math too)
      - the variable x

    Example: " (x-2)**2 + math.sin(x) "
    """
    allowed_globals = {"math": math, "sin": math.sin, "cos": math.cos, "exp": math.exp, "log": math.log, "sqrt": math.sqrt}
    # Use an empty __builtins__ to reduce risk
    def f(x: float) -> float:
        local_vars = {"x": x}
        return eval(expr, {"__builtins__": {}}, {**allowed_globals, **local_vars})
    return f


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Golden-section search (1D optimization)")
    p.add_argument("--a", type=float, required=True, help="Left endpoint of interval")
    p.add_argument("--b", type=float, required=True, help="Right endpoint of interval")
    p.add_argument("--tol", type=float, default=1e-5, help="Tolerance for interval length")
    p.add_argument("--max-iter", type=int, default=1000, help="Maximum iterations")
    p.add_argument("--maximize", action="store_true", help="Search for maximum instead of minimum")
    p.add_argument("--example", choices=["quadratic", "wavy"], help="Use a built-in example function")
    p.add_argument("--expr", type=str, help="Python expression in x to evaluate, e.g. \"(x-2)**2 + math.sin(x)\"")
    return p.parse_args()


def main() -> None:
    args = parse_args()

    if args.example and args.expr:
        raise SystemExit("Choose either --example or --expr, not both.")

    if args.example:
        if args.example == "quadratic":
            f = example_quadratic
        elif args.example == "wavy":
            f = example_wavy
        else:
            raise SystemExit("Unknown example")
    elif args.expr:
        f = make_function_from_expr(args.expr)
    else:
        raise SystemExit("Please provide --example or --expr")

    x_opt, f_opt, it = golden_section_search(
        f, args.a, args.b, tol=args.tol, max_iter=args.max_iter, minimize=not args.maximize
    )

    print("Result:")
    print(f"  x_opt = {x_opt:.12g}")
    print(f"  f(x_opt) = {f_opt:.12g}")
    print(f"  iterations = {it}")
    print(f"  final interval length = {abs(args.b - args.a):.12g}  (note: original endpoints unchanged in output)")


if __name__ == "__main__":
    main()
