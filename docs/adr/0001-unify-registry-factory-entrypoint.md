# ADR 0001: Unify Registry/Factory Entrypoint

## Status

Accepted

## Context

Issue `intellistream/sage-agentic-tooluse#3` requires unifying registry/factory paths and deleting historical non-canonical branches.

Observed problems:

- Multiple registry/factory entry paths (`get_selector`, `create_selector_from_config`, singleton accessor) increased API surface ambiguity.
- Public exports kept old helper paths that were not needed for current call sites.
- README examples still referenced obsolete selector names and outdated factory usage.

## Decision

1. Keep a single canonical factory entrypoint at module level: `create_selector(config_dict, resources)`.
2. Remove old helper paths:
   - `get_selector`
   - `create_selector_from_config`
   - `SelectorRegistry.get_instance()` singleton accessor
3. Keep explicit registration entrypoint: `register_selector(name, selector_class)`.
4. Update README to canonical selector names and canonical factory usage.

## Consequences

- Registry/factory API is explicit and easier to maintain.
- Removed paths are unavailable.
- Callers must use canonical creation path directly.
