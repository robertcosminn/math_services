"""Pydantic & ORM models for the math service."""
from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field
from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()


# --------------------- SQLAlchemy ORM --------------------- #
class ComputationLog(Base):  # noqa: D101
    __tablename__ = "computations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    op = Column(String, nullable=False)                # 'pow' | 'fib' | 'fact'
    params = Column(Text, nullable=False)              # JSON string of inputs
    result = Column(Text, nullable=False)              # store as TEXT for big ints
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


# --------------------- Pydantic requests/responses --------------------- #
class PowRequest(BaseModel):
    base: int = Field(..., description="Integer base")
    exponent: int = Field(..., ge=0, description="Non-negative integer exponent")

    model_config = {"frozen": True}  # immutable → safer


class FibRequest(BaseModel):
    n: int = Field(..., ge=0, description="n-th fibonacci number (n>=0)")
    model_config = {"frozen": True}


class FactRequest(BaseModel):
    n: int = Field(..., ge=0, description="factorial argument (n>=0)")
    model_config = {"frozen": True}


class MathResponse(BaseModel):
    # Keep as int: Python supports arbitrary precision
    result: int
    details: str  # e.g. "pow(2,10)=1024" or "fib(10)=55" or "fact(5)=120"


# tiny normaliser for any text-like inputs in future
class OpRequest(BaseModel):
    op: Literal["pow", "fib", "fact"]
    # not used directly in CLI, but can be useful for API variants
