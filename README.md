# SAGE Tool Use

**Tool retrieval and ranking algorithms for LLM agents**

[![PyPI version](https://badge.fury.io/py/isage-agentic-tooluse.svg)](https://badge.fury.io/py/isage-agentic-tooluse)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🎯 Overview

`sage-agentic-tooluse` provides a comprehensive suite of tool selection and ranking algorithms for LLM agents:

- **Keyword Selector**: Fast matching based on keyword overlap
- **Embedding Selector**: Semantic similarity using embeddings
- **Hybrid Selector**: Combines keyword and embedding approaches
- **DFS-DT Selector**: Decision tree-based tool selection
- **Gorilla Selector**: Gorilla-style tool retrieval

## 📦 Installation

```bash
# Basic installation
pip install isage-agentic-tooluse

# Development installation
pip install isage-agentic-tooluse[dev]
```

## 🚀 Quick Start

### Keyword-based Tool Selection

```python
from sage_libs.sage_agentic_tooluse import KeywordSelector, ToolSelectionQuery

# Create selector
selector = KeywordSelector.from_config(config=keyword_config, resources=resources)

# Select tools for a query
selected = selector.select(
    query=ToolSelectionQuery(
        sample_id="q1",
        instruction="Get current weather in New York",
        candidate_tools=["weather_api", "search_api"],
    ),
    top_k=5
)

for tool in selected:
    print(f"Tool: {tool.tool_id}, Score: {tool.score}")
```

### Embedding-based Tool Selection

```python
from sage_libs.sage_agentic_tooluse import EmbeddingSelector, ToolSelectionQuery

# Create selector with embedding model
selector = EmbeddingSelector.from_config(config=embedding_config, resources=resources)

# Select tools based on semantic similarity
selected = selector.select(
    query=ToolSelectionQuery(
        sample_id="q2",
        instruction="What's the weather like?",
        candidate_tools=["weather_api", "search_api"],
    ),
    top_k=5
)
```

### Hybrid Tool Selection

```python
from sage_libs.sage_agentic_tooluse import HybridSelector, ToolSelectionQuery

# Combine keyword and embedding approaches
selector = HybridSelector.from_config(config=hybrid_config, resources=resources)

selected = selector.select(
    query=ToolSelectionQuery(
        sample_id="q3",
        instruction="Find tools for weather updates",
        candidate_tools=["weather_api", "search_api", "calendar_api"],
    ),
    top_k=5,
)
```

## 📚 Key Components

### Selectors

- **KeywordSelector**: Fast keyword-based matching
- **EmbeddingSelector**: Semantic similarity using embeddings
- **HybridSelector**: Weighted combination of multiple selectors
- **DFSDTSelector**: Decision tree-based selection
- **GorillaSelector**: Gorilla-style API-centric retrieval

### Base Classes

- **BaseToolSelector**: Abstract base for all selectors
- **SelectorRegistry**: Central registry for selector implementations

### Schemas

- **ToolSelectionQuery**: Query payload for selector input
- **ToolPrediction**: Selection result with score and metadata
- **SelectorConfig**: Base selector configuration schema

## 🏗️ Architecture

```
sage_libs.sage_agentic_tooluse/
├── __init__.py              # Public API exports
├── base.py                  # Base selector interface
├── keyword_selector.py      # Keyword-based selection
├── embedding_selector.py    # Embedding-based selection
├── hybrid_selector.py       # Hybrid selection strategy
├── dfsdt_selector.py        # Decision tree selector
├── gorilla_selector.py      # Gorilla-style retrieval
├── registry.py              # Selector registry
├── schemas.py               # Data schemas
└── retriever/               # Retrieval utilities
```

## 🎓 Use Cases

1. **Agent Tool Selection**: Help agents choose the right tools
2. **API Discovery**: Find relevant APIs for a task
3. **Function Calling**: Select appropriate functions for LLMs
4. **Tool Recommendation**: Recommend tools to users
5. **Multi-step Planning**: Select tool sequences for complex tasks

## 🔗 Integration with SAGE

This package is part of the SAGE ecosystem and can be used with SAGE agents:

```python
# Standalone usage
from sage_libs.sage_agentic_tooluse import HybridSelector

from sage_libs.sage_agentic_tooluse import create_selector

selector = create_selector({"name": "hybrid", "top_k": 5}, resources)
```

## 📖 Documentation

- **Repository**: https://github.com/intellistream/sage-agentic-tooluse
- **SAGE Documentation**: https://intellistream.github.io/SAGE-Pub/
- **Issues**: https://github.com/intellistream/sage-agentic-tooluse/issues

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

Originally part of the [sage-agentic](https://github.com/intellistream/sage-agentic) package, now maintained as an independent repository for focused development and research.

## 📧 Contact

- **Team**: IntelliStream Team
- **Email**: shuhao_zhang@hust.edu.cn
- **GitHub**: https://github.com/intellistream

---

**Part of the SAGE ecosystem** - Stream Analytics for Generative AI Engines
