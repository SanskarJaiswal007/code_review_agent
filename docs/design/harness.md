# Harness design

## Purpose and boundaries

`packages/harness` is a reusable agent runtime for applications in this
workspace. It wraps LangChain and LangGraph objects instead of replacing them.
Applications supply their own models, tools, prompts, workflows, persistence,
and business rules. The Azure DevOps code review application is one possible
consumer; no Azure DevOps or pull-request policy belongs in the harness.

Executable services and workers belong in `apps/`. Reusable components belong
in `packages/`; the harness must not import from an app.

## Current components

| Component | Responsibility | Native foundation |
| --- | --- | --- |
| `Harness` | Build a default tool-calling agent or run a supplied compiled workflow | LangChain `create_agent`, LangGraph graph |
| Model and tools | Inject application-selected chat model and native LangChain tools | LangChain |
| Short-term memory | Retain graph state by `thread_id` when a checkpointer is supplied | LangGraph checkpointer |
| Long-term memory | Explicitly put, get, and search values in a namespace | LangGraph store |
| MCP access | Discover and call HTTP MCP tools with optional bearer or custom header authentication | FastMCP client |

`Harness.graph` exposes the underlying graph. The wrapper provides `invoke`,
`ainvoke`, `stream`, and `astream`, forwarding graph options and adding a
`thread_id` to the LangGraph configuration. A checkpointer requires a thread
identifier. Callers can supply a compiled workflow instead of the default
agent, preserving LangGraph's workflow features.

## Memory model

Short-term memory is graph execution state. Applications choose an in-memory
checkpointer for development or a durable implementation for production.
Thread IDs must be scoped by the application so unrelated reviews do not share
conversation state.

Long-term memory is a separate LangGraph store. The harness exposes explicit
store operations but does not automatically extract memories from conversations
or inject them into prompts. An application workflow or tool decides what to
save, retrieve, expire, and share. Namespaces should include a tenant or
organization boundary where applicable.

## MCP connections and credentials

`MCPTools` creates an HTTP MCP client for discovery and tool calls. It accepts
a bearer token, a callable that returns the current bearer token, or custom
HTTP headers. The callable is evaluated for each new connection to support
token refresh outside the harness. Credentials must come from the consuming
application's secret provider or environment and must not be committed.

The existing Azure DevOps gateway in `apps/mcp` is an application adapter. It
can connect to a local Azure DevOps MCP process or a remote Azure DevOps MCP
endpoint. Its upstream authentication and the harness-to-gateway connection
are distinct. The harness currently exposes raw MCP discovery and calls;
converting discovered MCP tools into LangChain tools is still application work.

## Intended execution flow

1. An application selects a model, tools, prompt, checkpointer, and store.
2. It constructs `Harness` or supplies its own compiled LangGraph workflow.
3. It invokes the graph with input and an application-scoped `thread_id`.
4. The graph calls tools and checkpoints state. Application-specific nodes or
   tools may read and write the long-term store.
5. The application interprets the graph result and exposes it through its own
   service, worker, or interface.

## Next design work

- Define a reusable adapter from MCP tool schemas and calls to LangChain tools,
  including result conversion and error handling.
- Define extension points for memory retrieval and saving policies without
  embedding a particular application's data model.
- Add a production persistence choice and lifecycle guidance for checkpointers
  and stores.
- Build Azure DevOps pull-request review workflows in an app or a separate
  reusable package only when the behavior is genuinely shared.

Keep this document aligned with the implementation as the harness evolves.
