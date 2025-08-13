"""FastAPI layer that reuses the same services & DB."""
from __future__ import annotations

from fastapi import FastAPI, HTTPException
from pydantic import ValidationError

from .db import init_db, log_computation
from .models import FactRequest, FibRequest, MathResponse, PowRequest
from .services import compute_fact, compute_fib, compute_pow

app = FastAPI(title="Math Microservice", version="1.0.0")
init_db()


@app.post("/pow", response_model=MathResponse)
def pow_endpoint(req: PowRequest) -> MathResponse:  # noqa: D401
    try:
        resp = compute_pow(req)
        log_computation("pow", req.model_dump(), resp.result)
        return resp
    except (ValueError, ValidationError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/fibonacci", response_model=MathResponse)
def fibonacci_endpoint(req: FibRequest) -> MathResponse:
    try:
        resp = compute_fib(req)
        log_computation("fib", req.model_dump(), resp.result)
        return resp
    except (ValueError, ValidationError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/factorial", response_model=MathResponse)
def factorial_endpoint(req: FactRequest) -> MathResponse:
    try:
        resp = compute_fact(req)
        log_computation("fact", req.model_dump(), resp.result)
        return resp
    except (ValueError, ValidationError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
