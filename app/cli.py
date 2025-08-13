"""Click-powered CLI – runs computations and logs them to SQLite."""
from __future__ import annotations

import json
import sys
from typing import Optional

import click
from tabulate import tabulate

from .db import init_db, log_computation
from .models import FactRequest, FibRequest, PowRequest
from .services import compute_fact, compute_fib, compute_pow

# Ensure DB exists once per process
init_db()


@click.group()
def math() -> None:
    """Compute pow, fibonacci and factorial from the terminal."""
    # no-op: Click needs a group function


def _print(resp_details: str, result: int, verbose: bool) -> None:
    if verbose:
        click.echo(tabulate([[resp_details, result]], headers=["Details", "Result"]))
    else:
        click.echo(result)


# ----------------- pow ----------------- #
@math.command()
@click.option("--base", "-b", type=int, required=True, help="Integer base")
@click.option("--exp", "-e", "exponent", type=int, required=True,
              help="Non-negative integer exponent")
@click.option("-v", "--verbose", is_flag=True, help="Pretty table output")
def pow(base: int, exponent: int, verbose: bool) -> None:  # noqa: A003 - Click name
    """Compute pow(base, exp)."""
    try:
        req = PowRequest(base=base, exponent=exponent)
        resp = compute_pow(req)
        log_computation("pow", {"base": base, "exponent": exponent}, resp.result)
        _print(resp.details, resp.result, verbose)
    except Exception as exc:  # noqa: BLE001
        click.secho(f"Error: {exc}", fg="red", err=True)
        sys.exit(1)


# ----------------- fibonacci ----------------- #
@math.command(name="fib")
@click.argument("n", type=int)
@click.option("-v", "--verbose", is_flag=True)
def fibonacci(n: int, verbose: bool) -> None:
    """Compute the n-th Fibonacci number."""
    try:
        req = FibRequest(n=n)
        resp = compute_fib(req)
        log_computation("fib", {"n": n}, resp.result)
        _print(resp.details, resp.result, verbose)
    except Exception as exc:  # noqa: BLE001
        click.secho(f"Error: {exc}", fg="red", err=True)
        sys.exit(1)


# ----------------- factorial ----------------- #
@math.command(name="fact")
@click.argument("n", type=int)
@click.option("-v", "--verbose", is_flag=True)
def factorial_cmd(n: int, verbose: bool) -> None:
    """Compute n! (factorial)."""
    try:
        req = FactRequest(n=n)
        resp = compute_fact(req)
        log_computation("fact", {"n": n}, resp.result)
        _print(resp.details, resp.result, verbose)
    except Exception as exc:  # noqa: BLE001
        click.secho(f"Error: {exc}", fg="red", err=True)
        sys.exit(1)


# ----------------- history ----------------- #
@math.command()
@click.option("--limit", "-l", type=int, default=10, show_default=True)
def history(limit: int) -> None:
    """Show last N computations (from SQLite)."""
    from sqlalchemy import text  # local import to keep global deps minimal
    from sqlalchemy.orm import Session
    from .db import ENGINE

    with Session(ENGINE) as s:
        rows = s.execute(
            text(
                "SELECT id, op, params, result, created_at "
                "FROM computations ORDER BY id DESC LIMIT :lim"
            ),
            {"lim": limit},
        ).fetchall()

    if not rows:
        click.echo("No computations found.")
        return

    table = []
    for rid, op, params, result, created_at in rows:
        table.append([rid, op, params, result, str(created_at)[:19]])
    click.echo(tabulate(table, headers=["id", "op", "params", "result", "created_at"]))


if __name__ == "__main__":
    math()
