# Python Formatting and Checking Guide: Ruff + uv

This guide is a project-neutral baseline for Python code formatting and linting. It is intended for use by humans and coding agents such as Codex, Claude Code, or other AI coding assistants.

Use **Ruff** for formatting, linting, import sorting, and simple automatic fixes. Use **uv** / **uvx** to run Ruff consistently and quickly.

## Default recommendation

Prefer this workflow:

```bash
uvx ruff format .
uvx ruff check --fix .
```

For check-only mode, such as CI or before submitting a patch:

```bash
uvx ruff format --check .
uvx ruff check .
```

`uvx` is an alias for `uv tool run`, so these are equivalent:

```bash
uvx ruff check .
uv tool run ruff check .
```

## Agent instructions

When editing Python code:

1. Format changed Python files with Ruff.
2. Run Ruff checks and apply safe automatic fixes.
3. Re-run checks without `--fix` before finalizing.
4. Do not introduce project-specific configuration unless the repository already has a clear convention.
5. Preserve existing behavior unless the task explicitly asks for refactoring.
6. Avoid broad rewrites just to satisfy style preferences.
7. Prefer minimal, targeted changes.

Suggested agent command sequence:

```bash
uvx ruff format .
uvx ruff check --fix .
uvx ruff check .
```

When speed or token efficiency matters, summarize failures by file and rule instead of pasting full logs. Include only the relevant error lines and the fix applied.

## One-off usage

Use `uvx` when you want to run Ruff without adding it to the project:

```bash
uvx ruff format .
uvx ruff check --fix .
```

This is good for quick cleanup, ad hoc repositories, and agent-driven edits.

## Project usage

For a maintained project, add Ruff as a development dependency so local development and CI use the same tool version:

```bash
uv add --dev ruff
uv run ruff format .
uv run ruff check --fix .
```

Check-only commands:

```bash
uv run ruff format --check .
uv run ruff check .
```

## Recommended baseline `pyproject.toml`

Use this as a neutral starting point. Adjust only when the project has a reason to diverge.

```toml
[tool.ruff]
line-length = 88
target-version = "py311"

[tool.ruff.lint]
select = [
  "E",    # pycodestyle errors
  "F",    # pyflakes
  "I",    # import sorting
  "UP",   # pyupgrade
  "B",    # flake8-bugbear
  "SIM",  # simplifications
]
ignore = []

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

## More conservative baseline

Use this when touching an existing codebase that may not be ready for broader lint rules:

```toml
[tool.ruff]
line-length = 88
target-version = "py311"

[tool.ruff.lint]
select = [
  "E",
  "F",
  "I",
]
ignore = []

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

## Slightly stricter baseline

Use this for new projects or projects that want more automated cleanup:

```toml
[tool.ruff]
line-length = 88
target-version = "py311"

[tool.ruff.lint]
select = [
  "E",    # pycodestyle errors
  "F",    # pyflakes
  "I",    # import sorting
  "UP",   # pyupgrade
  "B",    # flake8-bugbear
  "SIM",  # simplifications
  "C4",   # comprehensions
  "PIE",  # flake8-pie
  "RET",  # return statements
  "RUF",  # Ruff-specific rules
]
ignore = []

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

## File-specific ignores

Use file-specific ignores sparingly. They are useful for tests, generated files, migrations, or compatibility shims.

```toml
[tool.ruff.lint.per-file-ignores]
"tests/**/*.py" = [
  "S101",  # allow assert in tests, if using security rules
]
"__init__.py" = [
  "F401",  # allow re-exported imports
]
```

Do not add ignores just to avoid fixing simple issues. Prefer fixing the code when the rule is correct.

## Common commands

Format all files:

```bash
uvx ruff format .
```

Check all files:

```bash
uvx ruff check .
```

Apply safe automatic lint fixes:

```bash
uvx ruff check --fix .
```

Check whether formatting is needed:

```bash
uvx ruff format --check .
```

Show what Ruff would change without applying changes:

```bash
uvx ruff check --diff .
```

Run against specific files:

```bash
uvx ruff format path/to/file.py
uvx ruff check --fix path/to/file.py
```

Run a specific Ruff version:

```bash
uvx ruff@latest check .
uvx ruff@0.13.0 check .
```

## CI example

Generic CI command sequence:

```bash
uv run ruff format --check .
uv run ruff check .
```

If Ruff is not installed as a project dependency, use:

```bash
uvx ruff format --check .
uvx ruff check .
```

## Pre-commit example

A simple `.pre-commit-config.yaml` pattern:

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.13.0
    hooks:
      - id: ruff-format
      - id: ruff
        args: [--fix]
```

Update the `rev` periodically. Do not pin this example permanently without checking for the current Ruff release.

## When to use Black instead

Prefer Ruff formatter for new or flexible projects.

Use Black instead when:

- The project already standardizes on Black.
- The existing CI requires Black.
- The team intentionally wants Black as a separate tool.

Do not run Black and `ruff format` together unless the project explicitly requires both. In most cases, choose one formatter.

## Agent output style

When reporting results, keep output compact:

```text
Formatted Python files with Ruff.
Applied safe Ruff fixes.
Remaining issues:
- path/to/file.py:12 F821 undefined name `example`
- path/to/other.py:44 B008 function call in default argument
```

Avoid pasting hundreds of lines of linter output. Include enough detail for the user to understand what remains and where.

## Default policy for coding agents

Use the following policy unless a repository specifies otherwise:

```text
For Python code, use Ruff via uvx.
Run `uvx ruff format .` to format code.
Run `uvx ruff check --fix .` to apply safe lint fixes.
Run `uvx ruff check .` before finishing.
Do not introduce project-specific style rules unless requested.
Prefer minimal diffs and preserve existing behavior.
```

## Notes

- Ruff can be configured in `pyproject.toml`, `ruff.toml`, or `.ruff.toml`.
- `uvx` is best for one-off tool runs.
- `uv add --dev ruff` plus `uv run ruff ...` is best for maintained projects.
- Keep the configuration small until the project has a reason to add more rules.
