from app.models import FactRequest, FibRequest, PowRequest
from app.services import compute_fact, compute_fib, compute_pow


def test_pow():
    assert compute_pow(PowRequest(base=2, exponent=10)).result == 1024


def test_fib():
    assert compute_fib(FibRequest(n=10)).result == 55
    assert compute_fib(FibRequest(n=0)).result == 0
    assert compute_fib(FibRequest(n=1)).result == 1


def test_fact():
    assert compute_fact(FactRequest(n=0)).result == 1
    assert compute_fact(FactRequest(n=5)).result == 120
