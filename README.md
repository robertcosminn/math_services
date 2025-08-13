# Math Microservice — CLI + (optional) REST API

A compact **math microservice** that computes:

* `pow(base, exponent)`
* n‑th **Fibonacci** number
* **factorial** `n!`

The project demonstrates:

* Clean **MVCS** architecture (Model–View/Controller–Service)
* Validation & serialization with **Pydantic v2**
* **SQLite** persistence via **SQLAlchemy ORM** (every call is logged)
* **Click** CLI (self-documented, testable)
* Optional **FastAPI** HTTP layer with Swagger
* Quality gates: **flake8** + **pytest**

---

## Folder layout

```
math_services/
├─ app/
│  ├─ __init__.py      # marks package
│  ├─ api.py           # FastAPI routes (optional HTTP layer)
│  ├─ cli.py           # Click CLI (controller/view)
│  ├─ db.py            # DB engine + helpers (infrastructure)
│  ├─ models.py        # Pydantic schemas + ORM models (model)
│  └─ services.py      # Business logic + caching (service)
├─ tests/
│  └─ test_services.py # unit tests for core ops
├─ .flake8             # linter config
├─ requirements.txt    # reproducible deps
└─ computations.sqlite3# auto-created on first run
```

---

## Quick start

> **Python 3.11+** recommended.

### 1) Create & activate a virtual environment

**Windows PowerShell**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
# If scripts are blocked:
# Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

**Windows cmd.exe**

```bat
python -m venv .venv
.\.venv\Scripts\activate.bat
```

**macOS/Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2) Install dependencies

```bash
pip install -r requirements.txt
```

`requirements.txt` pins compatible versions:

```
click==8.2.0
pydantic==2.7.1
SQLAlchemy==1.4.52
tabulate==0.9.0
pytest==8.2.0
flake8==7.0.0
# Optional HTTP microservice
fastapi==0.115.9
uvicorn==0.30.0
```

---

## Run from the CLI (recommended)

Top‑level help:

```bash
python -m app.cli --help
```

### Operations

**pow**

```bash
python -m app.cli pow --base 2 --exp 10 -v
# Details              Result
# -----------------  -------
# pow(2,10)=1024         1024
```

**fibonacci**

```bash
python -m app.cli fib 50
# 12586269025
```

**factorial**

```bash
python -m app.cli fact 20 -v
```

**history** (persisted in SQLite)

```bash
python -m app.cli history --limit 5
```

> Use `-v/--verbose` for a table view; omit for raw numeric output.

---

## Run as a REST API (optional)

Start the server:

```bash
uvicorn app.api:app --reload
```

Open **Swagger UI**:

```
http://127.0.0.1:8000/docs
```

### Example cURL

```bash
# pow(2, 10)
curl -s -X POST http://127.0.0.1:8000/pow \
  -H 'Content-Type: application/json' \
  -d '{"base":2, "exponent":10}'

# fibonacci(50)
curl -s -X POST http://127.0.0.1:8000/fibonacci \
  -H 'Content-Type: application/json' \
  -d '{"n":50}'

# factorial(20)
curl -s -X POST http://127.0.0.1:8000/factorial \
  -H 'Content-Type: application/json' \
  -d '{"n":20}'
```

---

## Tests

From the project root (**inside the venv**):

```bash
python -m pytest -q
```


---

## Linting

```bash
flake8 .
# (no output means zero lint errors)
```

---

## How it works (high level)

1. **CLI/API controller** receives input and builds a Pydantic request model.
2. **Service layer** computes the result:

   * `pow` → Python’s fast integer exponentiation
   * `fib` → **fast doubling** algorithm (O(log n))
   * `fact` → iterative product to avoid recursion limits
     Results are memoised via `functools.lru_cache` for instant repeats.
3. **DB layer** writes one row per successful call to SQLite (`computations` table) with JSON parameters and TEXT result (supports big integers).
4. Output is returned as a Pydantic response (CLI prints as number/table; API returns JSON).

---

## Architecture (MVCS)

* **Model**: `models.py` (Pydantic schemas + SQLAlchemy ORM)
* **View/Controller**: `cli.py` (Click) and `api.py` (FastAPI)
* **Service**: `services.py` (pure business logic + caching)
* **Infrastructure**: `db.py` (engine, sessions, logging helper)


---
