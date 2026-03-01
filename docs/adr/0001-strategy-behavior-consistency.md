# ADR 0001: Strategy behavior consistency after non-canonical path removal

## Status

Accepted

## Context

Issue `intellistream/sage-agentic-tooluse#4` requires explicit verification that selector behavior remains consistent after removing non-canonical paths.

The boundary cleanup standard is:
- no implicit config coercion,
- no alias entry paths,
- no dual branch for factory inputs.

## Decision

- Enforce strict typed config in selector factories:
  - `HybridSelector.from_config` requires `HybridSelectorConfig`
  - `DFSDTSelector.from_config` requires `DFSDTSelectorConfig`
  - `GorillaSelector.from_config` requires `GorillaSelectorConfig`
- Keep canonical registry names only: `keyword`, `embedding`, `hybrid`, `gorilla`, `dfsdt`
- Add behavior consistency tests that compare direct selector creation and registry creation outputs.

## Consequences

- API behavior is explicit and stable.
- Callers must pass canonical typed configs.
- Strategy outputs stay verifiable with deterministic regression tests.
