# Design

## Context

See `proposal.md` for motivation and the three capability specs for required behavior. Today `Harness` owns one graph (a LangChain agent graph or a supplied compiled graph), forwards sync/async invocation and streaming, and accepts a LangGraph checkpointer and store. A supplied compiled graph is already compiled, so passing memory objects to `Harness` does not retroactively attach them. The reusable package has no trigger registry or event dispatcher.

## Goals / Non-Goals

**Goals:**

- Compose named LangGraph workflows, memory configuration, and trigger bindings without importing application code into `packages/harness`.
- Keep native graphs, checkpoint savers, stores, and LangChain tools available to callers.
- Preserve the existing single-graph `Harness` API during migration.

**Non-Goals:**

- Run a scheduler daemon, expose an HTTP endpoint, validate webhook signatures, or implement a GitHub PR adapter inside the harness.
- Choose a production database or a universal memory extraction algorithm.

## Decisions

### Named workflows and graph ownership

Add a `Workflow` component with a stable name and a compiled LangGraph graph. A registry rejects duplicate names and resolves a workflow for dispatch. For workflows that need harness-managed memory, allow a graph factory that receives the selected checkpointer and store before compilation; an already compiled graph remains usable, but its own compilation controls persistence. Expose the graph directly. Keep `Harness.invoke`, `ainvoke`, `stream`, and `astream` as the default-workflow path.

**Alternative considered:** Rebuild or wrap every graph at dispatch time. That would hide native LangGraph behavior and cannot safely add a checkpointer after compilation.

### Memory components and policies

Represent short-term memory as a selected LangGraph checkpointer and long-term memory as a selected LangGraph store. Add optional retrieval and save policy hooks scoped to a workflow. The hooks receive execution context, including an application-provided tenant namespace and thread identifier; retrieval returns data for the workflow input mapping, while save receives the result and decides what to persist. No hooks means no automatic long-term memory writes. Keep the existing explicit store methods for callers that manage memory themselves.

**Alternative considered:** Save every message automatically. That risks retaining sensitive or irrelevant content and does not provide a meaningful retrieval policy.

### Trigger events and bindings

Define a trigger event containing trigger ID, payload, and optional execution ID. A `TriggeredWorkflow` binding joins one registered trigger to one registered workflow, with an input mapper to adapt the event to that graph's state schema. Multiple bindings can target one workflow; a trigger ID has at most one enabled binding for deterministic dispatch. The dispatcher validates registration and binding before running any graph, passes event provenance in execution context, and uses the mapper to provide event data as graph input. Caller-supplied execution IDs are passed through; durable deduplication is left to the hosting application.

**Alternative considered:** Hard-code an event-shaped graph state for all workflows. That would prevent applications from reusing existing LangGraph graphs with different input schemas.

### Trigger adapters and hosting

Provide a common trigger contract and thin user, cron, and webhook adapters that normalize accepted application events. A user adapter accepts a direct request. A cron adapter accepts a due event from an application scheduler. A webhook adapter accepts an event already accepted by application HTTP ingress. The app owns scheduling, transport, authentication, signature verification, retry, and admission controls. A later GitHub PR adapter can implement the same contract without changing the dispatcher.

**Alternative considered:** Start background cron and HTTP servers in the harness. That would turn a reusable library into an executable service and conflict with the repository's `apps/` boundary.

## Risks / Trade-offs

- **Compiled graph lacks the intended checkpointer** → Document that persistence must be attached before compilation and provide the graph-factory path.
- **Trigger event is delivered more than once** → Pass through an execution ID and document that durable deduplication belongs to the hosting app.
- **Webhook event reaches a binding without verification** → Require the application ingress to authenticate and verify it before calling the adapter; test that the harness never treats transport receipt as authentication.
- **Memory crosses tenant boundaries** → Require application-scoped namespaces in memory policies and test distinct namespaces and thread IDs.
- **Existing callers break during migration** → Retain direct `Harness` methods and cover the existing invocation behavior in regression tests.

## Migration Plan

1. Add workflow and memory components alongside the existing `Harness` constructor.
2. Add trigger registration, bindings, adapters, and dispatch without changing the existing MCP client or gateway.
3. Update tests and `docs/design/harness.md`; demonstrate an app-owned event source using the reusable components.
4. Roll back by removing new registrations; existing direct harness invocation remains available.
