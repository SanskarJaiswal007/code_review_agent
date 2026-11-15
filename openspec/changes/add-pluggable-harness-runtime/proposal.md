# Proposal

## Why

The harness currently accepts a single graph and optional LangGraph persistence objects, but applications cannot declare reusable workflows, memory policies, or which events are allowed to start a workflow. A composable runtime is needed before building application-specific code review automation.

## What Changes

- Introduce pluggable workflow definitions backed by compiled LangGraph graphs, while preserving access to the native graph and existing `Harness` calls.
- Make short-term checkpointing and long-term memory behavior configurable components, including explicit retrieval and save policies rather than assuming a store remembers automatically.
- Add a trigger contract and a binding that pairs configured triggers with workflows. Provide user-initiated, cron, and webhook trigger adapters without embedding an HTTP server or scheduler process in the reusable package.
- Reject dispatch from unknown or unbound triggers; carry trigger identity and event data into the selected workflow.
- Leave a GitHub pull-request trigger as a later adapter built on the same contract.

## Capabilities

### New Capabilities

- `harness-workflows`: Registration and execution of pluggable LangGraph-backed workflows.
- `harness-memory`: Configurable short-term and long-term memory components and policies.
- `harness-triggers`: Trigger contracts, adapters, and explicit trigger-to-workflow bindings.

### Modified Capabilities

None; the project has no published OpenSpec capabilities yet.

## Impact

The reusable `packages/harness` API, tests, and design documentation will change. Applications under `apps/` will be able to configure bindings and host scheduler or HTTP ingress, but this change does not add a production scheduler service, webhook server, or GitHub-specific PR integration. LangGraph and LangChain remain the underlying workflow and memory foundations.
