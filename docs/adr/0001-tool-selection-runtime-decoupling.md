# ADR 0001: Decouple tool selection algorithms from runtime client binding

## Status

Accepted

## Context

Issue `intellistream/sage-agentic-tooluse#2` requires this repository to remain an algorithm/interface package (L3).

Two selectors (`DFSDTSelector`, `GorillaSelector`) previously attempted to initialize runtime clients internally via `sage.llm.UnifiedInferenceClient`. This creates implicit runtime binding and violates the boundary requirement.

## Decision

- Remove internal runtime client creation from selectors.
- Use dependency injection through `SelectorResources`:
  - `embedding_client` for embedding-based retrieval.
  - `llm_client` for LLM-based scoring/reranking.
- Keep algorithmic fallback behavior (retrieval-only or heuristic scoring) when `llm_client` is absent.
- Do not introduce compatibility shim/re-export/dual-path runtime adapters.

## Consequences

- Selectors are runtime-neutral and environment-agnostic.
- Application layer owns concrete client provisioning.
- Boundary remains explicit and testable.
