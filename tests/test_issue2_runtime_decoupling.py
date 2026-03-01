from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from sage_libs.sage_agentic_tooluse.base import SelectorResources
from sage_libs.sage_agentic_tooluse.dfsdt_selector import DFSDTSelector
from sage_libs.sage_agentic_tooluse.gorilla_selector import GorillaSelector
from sage_libs.sage_agentic_tooluse.schemas import (
    DFSDTSelectorConfig,
    GorillaSelectorConfig,
    ToolSelectionQuery,
)


class _Tool:
    def __init__(
        self,
        tool_id: str,
        name: str,
        description: str,
        capabilities: list[str] | None = None,
        category: str = "",
        parameters: dict[str, Any] | None = None,
    ) -> None:
        self.tool_id = tool_id
        self.name = name
        self.description = description
        self.capabilities = capabilities or []
        self.category = category
        self.parameters = parameters or {}


class _ToolsLoader:
    def __init__(self, tools: list[_Tool]) -> None:
        self._tools = tools

    def iter_all(self):
        return iter(self._tools)


class _MockLLMClient:
    def __init__(self, response: str) -> None:
        self.response = response

    def chat(self, *args, **kwargs):
        _ = args, kwargs
        return self.response


class _MockEmbeddingClient:
    def embed(self, texts: list[str], model: str | None = None, batch_size: int | None = None):
        _ = model, batch_size
        rows = []
        for text in texts:
            rows.append([float(len(text) % 7 + 1), float((len(text) % 5) + 1), 1.0])
        return np.asarray(rows)


def _make_tools_loader() -> _ToolsLoader:
    tools = [
        _Tool("weather_api", "WeatherAPI", "Get weather and forecast", ["weather", "forecast"]),
        _Tool("calendar_api", "CalendarAPI", "Manage meetings and events", ["calendar"]),
        _Tool("search_api", "SearchAPI", "General web search", ["search"]),
    ]
    return _ToolsLoader(tools)


def test_dfsdt_uses_injected_llm_client_for_scoring() -> None:
    resources = SelectorResources(
        tools_loader=_make_tools_loader(),
        llm_client=_MockLLMClient("9"),
    )
    selector = DFSDTSelector(DFSDTSelectorConfig(top_k=2), resources)

    query = ToolSelectionQuery(
        sample_id="q1",
        instruction="what is the weather tomorrow",
        candidate_tools=["weather_api", "calendar_api", "search_api"],
    )

    predictions = selector.select(query, top_k=2)

    assert predictions
    assert all(p.metadata.get("method") == "dfsdt" for p in predictions)


def test_dfsdt_works_without_llm_client_via_heuristic_scoring() -> None:
    resources = SelectorResources(
        tools_loader=_make_tools_loader(),
        llm_client=None,
    )
    selector = DFSDTSelector(DFSDTSelectorConfig(top_k=2), resources)

    query = ToolSelectionQuery(
        sample_id="q2",
        instruction="weather forecast",
        candidate_tools=["weather_api", "calendar_api"],
    )

    predictions = selector.select(query, top_k=2)

    assert predictions
    assert all(0.0 <= p.score <= 1.0 for p in predictions)


def test_gorilla_uses_injected_llm_client_from_resources() -> None:
    resources = SelectorResources(
        tools_loader=_make_tools_loader(),
        embedding_client=_MockEmbeddingClient(),
        llm_client=_MockLLMClient('["weather_api", "search_api"]'),
    )
    selector = GorillaSelector(GorillaSelectorConfig(top_k_retrieve=3, top_k_select=2), resources)

    query = ToolSelectionQuery(
        sample_id="q3",
        instruction="find weather updates",
        candidate_tools=["weather_api", "calendar_api", "search_api"],
    )

    predictions = selector.select(query, top_k=2)

    assert len(predictions) == 2
    assert predictions[0].tool_id == "weather_api"


def test_no_direct_runtime_client_imports_in_selectors() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    dfsdt_content = (repo_root / "src/sage_libs/sage_agentic_tooluse/dfsdt_selector.py").read_text(
        encoding="utf-8"
    )
    gorilla_content = (
        repo_root / "src/sage_libs/sage_agentic_tooluse/gorilla_selector.py"
    ).read_text(encoding="utf-8")

    assert "UnifiedInferenceClient" not in dfsdt_content
    assert "from sage.llm" not in dfsdt_content
    assert "UnifiedInferenceClient" not in gorilla_content
    assert "from sage.llm" not in gorilla_content
