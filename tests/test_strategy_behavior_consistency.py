"""Strategy behavior consistency tests for Wave B3 (#4)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import pytest

from sage_libs.sage_agentic_tooluse import create_selector
from sage_libs.sage_agentic_tooluse.base import SelectorResources
from sage_libs.sage_agentic_tooluse.dfsdt_selector import DFSDTSelector
from sage_libs.sage_agentic_tooluse.gorilla_selector import GorillaSelector
from sage_libs.sage_agentic_tooluse.hybrid_selector import HybridSelector, HybridSelectorConfig
from sage_libs.sage_agentic_tooluse.keyword_selector import KeywordSelector
from sage_libs.sage_agentic_tooluse.registry import _registry
from sage_libs.sage_agentic_tooluse.schemas import (
    KeywordSelectorConfig,
    SelectorConfig,
    ToolSelectionQuery,
)


@dataclass
class _Tool:
    tool_id: str
    name: str
    description: str = ""
    capabilities: list[str] = field(default_factory=list)
    category: str = ""
    parameters: dict[str, Any] = field(default_factory=dict)


class _ToolsLoader:
    def __init__(self, tools: list[_Tool]) -> None:
        self._tools = tools

    def iter_all(self):
        return iter(self._tools)


class _EmbeddingClient:
    def embed(self, texts: list[str], model: str | None = None, batch_size: int = 32):
        _ = model, batch_size
        vectors = []
        for text in texts:
            t = text.lower()
            vectors.append(
                [
                    float("weather" in t),
                    float("search" in t),
                    float("translate" in t),
                    float("database" in t),
                ]
            )
        return vectors


def _make_tools() -> list[_Tool]:
    return [
        _Tool("weather", "WeatherTool", "weather forecast and climate search"),
        _Tool("translate", "TranslateTool", "translate text across languages"),
        _Tool("db", "DatabaseTool", "search database records and analytics"),
    ]


def _make_query() -> ToolSelectionQuery:
    return ToolSelectionQuery(
        sample_id="q1",
        instruction="search weather forecast",
        candidate_tools=["weather", "translate", "db"],
    )


def test_registry_and_direct_keyword_outputs_are_consistent() -> None:
    resources = SelectorResources(tools_loader=_ToolsLoader(_make_tools()))
    query = _make_query()

    cfg = KeywordSelectorConfig(name="keyword", method="overlap", top_k=2)
    direct = KeywordSelector.from_config(cfg, resources)
    via_registry = create_selector({"name": "keyword", "method": "overlap", "top_k": 2}, resources)

    direct_results = direct.select(query)
    registry_results = via_registry.select(query)

    assert [(x.tool_id, x.score) for x in direct_results] == [
        (x.tool_id, x.score) for x in registry_results
    ]


def test_hybrid_keyword_only_matches_keyword_ranking() -> None:
    resources = SelectorResources(tools_loader=_ToolsLoader(_make_tools()))
    query = _make_query()

    hybrid_cfg = HybridSelectorConfig(name="hybrid", top_k=2, keyword_method="overlap")
    hybrid = HybridSelector.from_config(hybrid_cfg, resources)

    keyword_cfg = KeywordSelectorConfig(name="keyword", method="overlap", top_k=2)
    keyword = KeywordSelector.from_config(keyword_cfg, resources)

    hybrid_results = hybrid.select(query)
    keyword_results = keyword.select(query)

    assert [x.tool_id for x in hybrid_results] == [x.tool_id for x in keyword_results]


@pytest.mark.parametrize(
    ("selector_cls", "bad_name", "error_text"),
    [
        (HybridSelector, "hybrid", "Expected HybridSelectorConfig"),
        (DFSDTSelector, "dfsdt", "Expected DFSDTSelectorConfig"),
        (GorillaSelector, "gorilla", "Expected GorillaSelectorConfig"),
    ],
)
def test_from_config_rejects_generic_selector_config(selector_cls, bad_name: str, error_text: str) -> None:
    resources = SelectorResources(
        tools_loader=_ToolsLoader(_make_tools()),
        embedding_client=_EmbeddingClient(),
    )

    generic = SelectorConfig(name=bad_name)
    with pytest.raises(TypeError, match=error_text):
        selector_cls.from_config(generic, resources)


def test_registry_names_are_canonical() -> None:
    names = set(_registry.list_selectors())
    canonical = {"keyword", "embedding", "hybrid", "gorilla", "dfsdt"}

    assert canonical.issubset(names)
    assert "get_selector" not in names
    assert "create_selector_from_config" not in names
