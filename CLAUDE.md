# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository is a simple script demonstrating how to use the Google Gemini REST API to generate quick image labels. The codebase is currently a starting point — no source code, dependencies, or scripts exist yet.

## Python Environment

This project uses `uv` for Python dependency, environment, and version management (see `docs/uv.md`):

```bash
# List available Python versions
uv python list

# Run a script in the uv-managed environment
uv run script.py

# Run a module
uv run python -m module
```

## Coding Principles

Follow `docs/effective-code.md` when writing code in this repo. Key points beyond general best practice:
- Prefer early returns/guard clauses over deep nesting.
- Keep functions and classes single-purpose and small.
- Comment only to explain *why*, not *what*.

## Commit Conventions

Use the `/commit` workflow described in `docs/commit.mdc`:
- Conventional commit format (`type(scope): description`), e.g. `feat`, `fix`, `docs`, `refactor`, `chore`.
- Stage specific files/paths — never `git add .` or `git add -A`.
- For multi-line commit messages, use multiple `-m` flags rather than embedded newlines.
- Ensure a sensible `.gitignore` exists (e.g. for `.env`, API keys, `uv` virtualenvs).
