# Spec Delta

## Purpose

Lets applications choose short-term conversation persistence and explicit long-term memory policies while retaining control over what information is saved and retrieved.

## ADDED Requirements

### Requirement: Pluggable short-term state
The harness SHALL accept an application-selected checkpoint backend for each workflow and SHALL require a thread identifier when checkpointing is enabled.

#### Scenario: Resume one thread
- **WHEN** a workflow runs again with the same thread identifier and checkpointer
- **THEN** it can access the checkpointed state from the earlier run

#### Scenario: Missing thread identifier
- **WHEN** a checkpointed workflow is invoked without a thread identifier
- **THEN** invocation fails before executing the workflow

### Requirement: Pluggable long-term store
The harness SHALL accept an application-selected long-term store and SHALL expose namespace-scoped read, write, and search operations.

#### Scenario: Read saved memory
- **WHEN** an application saves a value under a namespace and key and later reads that key
- **THEN** it receives the saved value

#### Scenario: Store not configured
- **WHEN** an application requests a long-term memory operation without a configured store
- **THEN** the operation fails with a clear configuration error

### Requirement: Explicit memory policies
The harness SHALL let an application configure retrieval and save behavior for long-term memory, and SHALL not save conversation content merely because a store is present.

#### Scenario: Configured retrieval and save
- **WHEN** a workflow runs with application-defined memory policies
- **THEN** those policies determine which namespace-scoped memories are supplied to and saved from the run

#### Scenario: No policy
- **WHEN** a workflow runs with a store but no save policy
- **THEN** the harness does not automatically persist conversation content to long-term memory
