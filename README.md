# code_review_agent

## Development checks

Install the development dependencies and Git hook once per clone:

```bash
uv sync
uv run pre-commit install
```

Commits containing staged Python files run Ruff formatting, Ruff lint fixes,
ty type checking, and pytest in that order. If Ruff changes a file, the commit
stops so you can review and stage the formatted result before trying again.
Run the checks manually with `uv run pre-commit run --all-files`.
