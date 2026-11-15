# Spec Delta

## Purpose

Allows applications to register and run reusable, named workflows backed by LangGraph graphs while retaining direct access to the underlying workflow object.

## ADDED Requirements

### Requirement: Register pluggable workflows
The harness SHALL let an application register multiple named workflows backed by compiled LangGraph graphs and SHALL reject duplicate workflow names.

#### Scenario: Register separate workflows
- **WHEN** an application registers two workflows with distinct names
- **THEN** both workflows are available for selection by name

#### Scenario: Duplicate name
- **WHEN** an application registers a workflow using a name already registered
- **THEN** registration fails without replacing the existing workflow

### Requirement: Execute a selected workflow
The harness SHALL execute only the selected registered workflow and SHALL expose its underlying graph for native LangGraph operations.

#### Scenario: Select a workflow
- **WHEN** an application invokes a registered workflow with input and execution configuration
- **THEN** that workflow receives the input and configuration, and its result is returned

#### Scenario: Unknown workflow
- **WHEN** an application requests a workflow name that is not registered
- **THEN** execution fails before any workflow runs

### Requirement: Preserve direct harness execution
The harness SHALL keep its existing direct invocation and streaming entry points usable for applications that configure a single default graph.

#### Scenario: Existing invocation
- **WHEN** an application invokes a single configured graph through the existing harness interface
- **THEN** the graph runs with the supplied thread configuration and returns its result
