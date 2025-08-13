"""DB engine + helpers – single responsibility module."""
from __future__ import annotations

import json
from contextlib import contextmanager
from typing import Any, Dict

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from .models import Base, ComputationLog

# SQLite file in project root
ENGINE = create_engine("sqlite:///computations.sqlite3", echo=False, future=True)


def init_db() -> None:
    """Create tables if missing."""
    Base.metadata.create_all(ENGINE)


@contextmanager
def get_session() -> Session:
    """Yield a session; commit or rollback automatically."""
    session: Session = Session(ENGINE)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def log_computation(op: str, params: Dict[str, Any], result: int) -> None:
    """Persist one computation row to SQLite as JSON params + TEXT result."""
    with get_session() as s:
        s.add(
            ComputationLog(
                op=op,
                params=json.dumps(params, separators=(",", ":")),  # compact JSON
                result=str(result),  # TEXT column supports big factorials
            )
        )
