# Selector Factory Migration (Wave B3)

This migration note covers the breaking behavior for selector factory construction.

## Scope

- Repository: `sage-agentic-tooluse`
- Issue: `#4`
- Policy: direct removal of non-canonical paths

## Breaking Change

Selector `from_config` now requires typed config objects and rejects generic `SelectorConfig`.

### Before

```python
from sage_libs.sage_agentic_tooluse.schemas import SelectorConfig
from sage_libs.sage_agentic_tooluse.hybrid_selector import HybridSelector

cfg = SelectorConfig(name="hybrid")
selector = HybridSelector.from_config(cfg, resources)
```

### After

```python
from sage_libs.sage_agentic_tooluse.hybrid_selector import HybridSelector, HybridSelectorConfig

cfg = HybridSelectorConfig(name="hybrid")
selector = HybridSelector.from_config(cfg, resources)
```

Apply the same pattern for:
- `DFSDTSelector` + `DFSDTSelectorConfig`
- `GorillaSelector` + `GorillaSelectorConfig`

## Canonical Registry Names

Use only:
- `keyword`
- `embedding`
- `hybrid`
- `gorilla`
- `dfsdt`

## Verification

Run:

```bash
PYTHONPATH=src pytest -q tests/test_strategy_behavior_consistency.py
ruff check tests/test_strategy_behavior_consistency.py docs/adr/0001-strategy-behavior-consistency.md docs/migration/selector-factory-migration.md
```
