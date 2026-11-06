# Contributing to Obs_AI

Thank you for your interest in contributing to Obs_AI!

---

## Development Setup

1. Fork and clone the repository:

```bash
git clone https://github.com/DarshanAguru/Obs_AI.git
cd obs_ai
```

2. Create virtual environment and install development dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ./sdk -e ./server pytest
```

3. Run test suite:

```bash
pytest
```

---

## Coding Guidelines

- Write clean, typed Python code (`list[str]`, `str | None`).
- Maintain test coverage for all new functionality.
- Ensure no telemetry exporter errors ever crash user applications.
- Follow conventional commits (`feat: ...`, `fix: ...`, `docs: ...`).

