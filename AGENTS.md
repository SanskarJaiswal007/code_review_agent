# Project guidance

## Structure

- Put every executable application, service, worker, and CLI entry point under
  `apps/`. Application packages may compose reusable libraries and contain
  deployment or runtime configuration specific to that application.
- Put reusable libraries and components under `packages/`. A package should be
  usable by more than one app without importing from `apps/` or embedding one
  application's business logic. Apps may depend on packages; packages must not
  depend on apps.
- `packages/harness/` is the reusable LangChain and LangGraph harness. `core.py`
  wraps a default tool-calling agent or a supplied graph, with checkpointing and
  explicit LangGraph store access. `mcp_tools.py` connects to HTTP MCP servers
  and supports bearer tokens or custom authentication headers. Keep the harness
  independent of Azure DevOps and pull-request-specific workflows so another
  application can use it as a general agent harness.
- `apps/mcp/` is the Azure DevOps MCP gateway. It selects a local or remote
  upstream and exposes tools through a local HTTP MCP endpoint.
- `apps/harness-worker/` is the worker app scaffold. It does not yet run a code
  review workflow.
- `packages/harness/tests/` holds the current pytest coverage for the harness.
- Root `pyproject.toml` defines the uv workspace and development dependencies;
  `ruff.toml`, `ty.toml`, and `.pre-commit-config.yaml` define quality checks.

## Python workflow

- Use Python 3.14 and install the workspace with `uv sync`.
- Before considering a Python change complete, run these commands from the
  repository root, in order:

  ```bash
  uv run ruff format --check .
  uv run ruff check .
  uv run ty check
  uv run pytest -q
  ```

- When formatting is needed, run `uv run ruff format .`, then repeat the four
  verification commands. Fix lint, type, and test failures instead of disabling
  their checks without a specific reason.
- The installed pre-commit hook runs Ruff format, Ruff lint fixes, ty, and
  pytest when staged Python files are committed. Run `uv run pre-commit install`
  once per clone. If Ruff changes a file during commit, review and stage that
  change, then commit again.
- Add or update pytest coverage for behavior changes. Keep credentials out of
  source files and tests; use environment variables or a secret provider.
