"""Business logic for pow, fibonacci, factorial with simple caching."""
from __future__ import annotations

from functools import lru_cache
from typing import Tuple

from .models import FactRequest, FibRequest, MathResponse, PowRequest


# ---------- Core math implementations ---------- #
@lru_cache(maxsize=256)
def pow_int(base: int, exponent: int) -> int:
    """Fast integer power (non-negative exponent)."""
    return pow(base, exponent)


@lru_cache(maxsize=512)
def fib(n: int) -> int:
    """n-th Fibonacci using fast doubling (O(log n))."""

    def _pair(k: int) -> Tuple[int, int]:
        # returns (F(k), F(k+1))
        if k == 0:
            return (0, 1)
        a, b = _pair(k // 2)
        c = a * ((b << 1) - a)         # F(2k)   = F(k) * (2*F(k+1) − F(k))
        d = a * a + b * b              # F(2k+1) = F(k)^2 + F(k+1)^2
        if k % 2 == 0:
            return (c, d)
        return (d, c + d)

    return _pair(n)[0]


@lru_cache(maxsize=256)
def factorial(n: int) -> int:
    """n! using iterative product (avoids recursion depth issues)."""
    if n < 2:
        return 1
    prod = 1
    for i in range(2, n + 1):
        prod *= i
    return prod


# ---------- Facade functions that accept Pydantic requests ---------- #
def compute_pow(req: PowRequest) -> MathResponse:
    res = pow_int(req.base, req.exponent)
    return MathResponse(result=res, details=f"pow({req.base},{req.exponent})={res}")


def compute_fib(req: FibRequest) -> MathResponse:
    res = fib(req.n)
    return MathResponse(result=res, details=f"fib({req.n})={res}")


def compute_fact(req: FactRequest) -> MathResponse:
    res = factorial(req.n)
    return MathResponse(result=res, details=f"fact({req.n})={res}")
