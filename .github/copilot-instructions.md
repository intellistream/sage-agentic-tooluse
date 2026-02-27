# sage-agentic-tooluse Copilot Instructions

## Scope
- Package: `isage-agentic-tooluse`, import path `sage_libs.sage_agentic_tooluse`.
- Layer: **L3** algorithm library — tool-use / tool-selection implementations for SAGE agents.

## Polyrepo Context (Important)
SAGE was restructured from a monorepo into a polyrepo. This repo provides **concrete tool-use implementations** (selectors, hybrid strategies, schema handling) that register into the `sage-libs` (L3) interface layer. It depends on `sage-libs` interfaces and `sage-agentic` base classes, not the reverse.

## Critical rules
- Keep this package runtime/service-neutral; no L4+ dependencies.
- Do not create new local virtual environments (`venv`/`.venv`); use the existing configured Python environment.
- No fallback logic; fail fast.
- Keep registry-based integration via `_register.py` and `sage.libs.agentic` factories.

## Architecture focus
- Tool selection strategies: `HybridSelector`, `DFSDTSelector`, `GorillaSelector`, etc.
- `base.py` — base tool-use interface.
- `schemas.py` — tool schema definitions.
- Registers implementations into `sage-libs` tool-use factory.

## Dependencies
- **Depends on**: `isage-common` (L1), `isage-libs` (L3 interfaces), `isage-agentic` (L3 base).
- **Depended on by**: `sage-agentic-tooluse-benchmark`, `sage-agentic-tooluse-sias`, application repos.

## Workflow
1. Make minimal changes under `src/sage_libs/sage_agentic_tooluse/`.
2. Keep public imports stable in `__init__.py`.
3. Run `pytest tests/ -v` and update docs for behavior changes.

## Development setup
```bash
./quickstart.sh       # installs hooks + pip install -e .[dev]
./quickstart.sh --doctor  # diagnose env issues
```

## Git Hooks (Mandatory)
- Never use `git commit --no-verify` or `git push --no-verify`.
- If hooks fail, fix the issue first.
