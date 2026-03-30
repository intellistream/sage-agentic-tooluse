"""Regression tests for issue #3 registry/factory boundary cleanup."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from sage_libs.sage_agentic_tooluse import create_selector, register_selector
from sage_libs.sage_agentic_tooluse.base import BaseToolSelector, SelectorResources
from sage_libs.sage_agentic_tooluse.registry import SelectorRegistry
from sage_libs.sage_agentic_tooluse.schemas import (
    SelectorConfig,
    ToolPrediction,
    ToolSelectionQuery,
)


class _DummySelector(BaseToolSelector):
    @classmethod
    def from_config(cls, config: SelectorConfig, resources: SelectorResources) -> _DummySelector:
        return cls(config, resources)

    def _select_impl(self, query: ToolSelectionQuery, top_k: int) -> list[ToolPrediction]:
        return [ToolPrediction(tool_id=query.candidate_tools[0], score=0.99)]


def test_canonical_factory_entrypoint_create_selector() -> None:
    register_selector("dummy_issue3", _DummySelector)

    resources = SelectorResources(tools_loader=object())
    selector = create_selector({"name": "dummy_issue3", "top_k": 1}, resources)

    assert isinstance(selector, _DummySelector)


def test_removed_helper_paths_are_absent() -> None:
    import sage_libs.sage_agentic_tooluse as tooluse

    assert not hasattr(tooluse, "get_selector")
    assert not hasattr(tooluse, "create_selector_from_config")


def test_registry_singleton_accessor_removed() -> None:
    assert not hasattr(SelectorRegistry, "get_instance")
