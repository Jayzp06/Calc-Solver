import os
import re
from typing import List, Tuple

import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr


# Directory to save generated plots
PLOT_DIR = os.path.join('static', 'plots')
os.makedirs(PLOT_DIR, exist_ok=True)


def detect_problem(text: str) -> str:
    """Detect problem type based on keywords."""
    lower = text.lower()
    if 'int' in lower or '∫' in text:
        return 'integral'
    if 'limit' in lower or 'lim' in lower:
        return 'limit'
    if 'd/d' in lower or 'derivative' in lower or 'diff' in lower:
        return 'derivative'
    return 'expression'


def _plot(expr, result_expr, var: sp.Symbol, filename: str, label_result: str):
    xs = np.linspace(-5, 5, 400)
    f1 = sp.lambdify(var, expr, modules=['numpy'])
    f2 = sp.lambdify(var, result_expr, modules=['numpy'])
    fig, ax = plt.subplots()
    ax.plot(xs, f1(xs), label='f(x)')
    ax.plot(xs, f2(xs), label=label_result)
    ax.legend()
    ax.grid(True)
    path = os.path.join(PLOT_DIR, filename)
    fig.savefig(path)
    plt.close(fig)
    return path


def solve(text: str) -> Tuple[str, List[str], str]:
    """Solve calculus problem from text.

    Returns tuple of problem type, steps list, plot path.
    """
    problem = detect_problem(text)
    steps: List[str] = [f"Detected problem type: {problem}"]
    x = sp.symbols('x')

    try:
        if problem == 'derivative':
            expr_str = re.split(r'd/dx', text, flags=re.IGNORECASE)[-1]
            expr = parse_expr(expr_str)
            steps.append(f"Expression: {sp.pretty(expr)}")
            result = sp.diff(expr, x)
            steps.append(f"Derivative: {sp.pretty(result)}")
            plot_path = _plot(expr, result, x, 'derivative.png', 'f\'(x)')
        elif problem == 'integral':
            expr_match = re.split(r'int|∫', text, flags=re.IGNORECASE)[-1]
            expr_match = re.split(r'dx', expr_match, flags=re.IGNORECASE)[0]
            expr = parse_expr(expr_match)
            steps.append(f"Integrand: {sp.pretty(expr)}")
            result = sp.integrate(expr, x)
            steps.append(f"Integral: {sp.pretty(result)} + C")
            plot_path = _plot(expr, result, x, 'integral.png', '∫f(x)dx')
        elif problem == 'limit':
            # very simple pattern limit as x->a of expr
            m = re.search(r'(?:limit|lim).*?x->([0-9+-]+)', text, re.IGNORECASE)
            limit_point = 0
            if m:
                limit_point = float(m.group(1))
            expr_str = text.split(' of ')[-1]
            expr = parse_expr(expr_str)
            steps.append(f"Expression: {sp.pretty(expr)}")
            result = sp.limit(expr, x, limit_point)
            steps.append(f"Limit as x-> {limit_point}: {sp.pretty(result)}")
            plot_path = _plot(expr, expr, x, 'limit.png', 'f(x)')
        else:
            expr = parse_expr(text)
            steps.append(f"Expression: {sp.pretty(expr)}")
            result = sp.simplify(expr)
            steps.append(f"Simplified: {sp.pretty(result)}")
            plot_path = _plot(expr, result, x, 'expression.png', 'f(x)')
    except Exception as exc:
        raise ValueError(f"Could not parse expression: {exc}")

    steps.append(f"Result: {result}")
    return problem, steps, plot_path

