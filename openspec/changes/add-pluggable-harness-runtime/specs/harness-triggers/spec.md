# Spec Delta

## Purpose

Allows applications to bind pluggable event sources to selected workflows so that only configured triggers can start workflow executions.

## ADDED Requirements

### Requirement: Pluggable trigger contract
The harness SHALL accept trigger implementations that identify their source and provide event data without requiring the reusable package to host an HTTP server or scheduler process.

#### Scenario: Application trigger adapter
- **WHEN** an application supplies a trigger implementation that follows the contract
- **THEN** the harness can bind it to a workflow without changing the workflow's graph

### Requirement: Explicit trigger-to-workflow bindings
The harness SHALL dispatch an event only through an enabled binding between a registered trigger and a registered workflow.

#### Scenario: Bound trigger fires
- **WHEN** an enabled trigger emits a valid event for a bound workflow
- **THEN** the selected workflow runs with the event data and trigger identity

#### Scenario: Unbound or disabled trigger
- **WHEN** an unbound or disabled trigger emits an event
- **THEN** no workflow runs and dispatch reports a rejected event

#### Scenario: Unknown workflow binding
- **WHEN** an application configures a trigger binding to an unknown workflow
- **THEN** configuration fails before event dispatch

### Requirement: User, cron, and webhook adapters
The harness SHALL provide adapters for user-initiated, cron, and webhook events. Cron and webhook adapters SHALL accept events from an application-hosted scheduler or HTTP ingress rather than creating those processes themselves.

#### Scenario: User invocation
- **WHEN** a user-initiated trigger receives an application request
- **THEN** it emits an event eligible for its configured workflow binding

#### Scenario: Scheduled event
- **WHEN** an application scheduler supplies a due cron event
- **THEN** the cron adapter emits an event eligible for its configured workflow binding

#### Scenario: Webhook event
- **WHEN** an application HTTP ingress supplies an accepted webhook event
- **THEN** the webhook adapter emits an event eligible for its configured workflow binding

### Requirement: Preserve event provenance
The harness SHALL pass a trigger identifier and event payload to the workflow and SHALL allow applications to supply a unique execution identifier for deduplication or tracing.

#### Scenario: Dispatch context
- **WHEN** a bound trigger dispatches an event with an execution identifier
- **THEN** the workflow receives that identifier, the trigger identifier, and the event payload
