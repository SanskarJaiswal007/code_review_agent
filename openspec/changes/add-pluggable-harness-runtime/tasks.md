# Tasks

## 1. Workflow component

- [ ] 1.1 Add a named `Workflow` wrapper and registry for compiled LangGraph graphs; verify tests cover distinct registrations, duplicate rejection, and unknown workflow lookup.
- [ ] 1.2 Add graph-factory construction with selected persistence objects and preserve direct `Harness` invocation and streaming; verify tests cover native graph access, selected execution, and existing call behavior.
- [ ] 1.3 Document workflow registration and compiled-graph persistence rules in `packages/harness/README.md` and `docs/design/harness.md`; verify examples match the public API.

## 2. Memory components

- [ ] 2.1 Expose per-workflow short-term checkpointer selection and thread configuration; verify tests cover resumed state, isolated threads, and missing thread ID errors.
- [ ] 2.2 Add long-term retrieval and save policy hooks with application-scoped namespaces while preserving explicit store methods; verify tests cover policy execution, namespace isolation, absent-store errors, and no automatic writes without a policy.
- [ ] 2.3 Document memory lifecycle, namespace requirements, and production backend selection in `packages/harness/README.md` and `docs/design/harness.md`; verify the documented example runs in tests.

## 3. Triggers and bindings

- [ ] 3.1 Add trigger event and adapter contracts plus user, cron, and webhook adapters; verify tests show each adapter normalizes application-supplied events without starting a scheduler or HTTP server.
- [ ] 3.2 Add explicit trigger-to-workflow registration and dispatch with input mapping and event provenance; verify tests cover a bound event, unknown workflow, unbound or disabled triggers, and execution ID pass-through.
- [ ] 3.3 Document application-owned scheduler, webhook verification, and a future GitHub PR adapter in `packages/harness/README.md` and `docs/design/harness.md`; verify examples match the public API.

## 4. Integration verification

- [ ] 4.1 Run `uv run ruff format --check .`, `uv run ruff check .`, `uv run ty check`, and `uv run pytest -q`; verify all commands pass with the workflow, memory, and trigger tests included.
- [ ] 4.2 Validate the OpenSpec change with `openspec validate add-pluggable-harness-runtime --strict`; verify no errors or warnings remain and mark implementation tasks complete.

## Workflow follow-up

- Report the implemented change and any limitations to the developer for review.
- Archive the change after the developer directs that step, then move to the next change.
