# Contributing

Thanks for your interest in contributing to this GenesisAeon ecosystem
package!

## Getting started

1. Fork and clone the repository.
2. Create a virtual environment: `python -m venv .venv && source .venv/bin/activate`
   (or `.venv\Scripts\activate` on Windows).
3. Install in editable mode with dev dependencies:
   `pip install -e ".[dev]"`.
4. Run the test suite: `pytest`.

## Code style

- Format and lint with `ruff format` / `ruff check`.
- Type-check with `mypy` (this repo uses `strict = true`).
- Keep functions documented with docstrings.

## Diamond Interface packages

`genesis-q4-core` does not currently implement the GenesisAeon Diamond
Interface (`run_cycle`, `get_crep_state`, `get_utac_state`,
`get_phase_events`, `to_zenodo_record`) — it is a foundational math
library (Gray-Code, Tesseract topology, Q4 state space) consumed by
Diamond packages elsewhere in the ecosystem. Any change to the public API
in `genesis_q4/` (`Q4State`, `GrayCode`, `Tesseract`,
`Q4TransitionValidator`) that breaks signatures or return shapes is a
**breaking change** and requires a MAJOR version bump (see
`RELEASE_GUIDE.md`).

## Pull requests

- One logical change per PR.
- Add or update tests for any behavioral change.
- Update `CHANGELOG.md` under an `## [Unreleased]` section.
- Fill out the PR template (`.github/PULL_REQUEST_TEMPLATE.md`).

## Reporting issues

Please use the issue templates in `.github/ISSUE_TEMPLATE/` — they help us
triage bug reports vs. feature requests quickly.

## Scientific claims

This is part of a research framework. If your contribution touches the
mathematical invariants documented in the README (e.g. the Hamming-1
invariant for consecutive Gray codes, Tesseract vertex/edge/face/cell
counts), please cite the source and keep speculative vs. validated claims
clearly marked.
