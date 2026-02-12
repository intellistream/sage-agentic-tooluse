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
- **Gorilla Adapter**: Gorilla-style tool retrieval

## 📦 Installation

```bash
# Basic installation
pip install isage-agentic-tooluse

# With embedding support
pip install isage-agentic-tooluse[embedding]

# Development installation
pip install isage-agentic-tooluse[dev]
```

## 🚀 Quick Start

### Keyword-based Tool Selection

```python
from sage_libs.sage_agentic_tooluse import KeywordToolSelector

# Create selector
selector = KeywordToolSelector(tools=available_tools)

# Select tools for a query
selected = selector.select(
    query="Get current weather in New York",
    top_k=5
)

for tool in selected:
    print(f"Tool: {tool.name}, Score: {tool.score}")
```

### Embedding-based Tool Selection

```python
from sage_libs.sage_agentic_tooluse import EmbeddingToolSelector

# Create selector with embedding model
selector = EmbeddingToolSelector(
    tools=available_tools,
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Select tools based on semantic similarity
selected = selector.select(
    query="What's the weather like?",
    top_k=5
)
```

### Hybrid Tool Selection

```python
from sage_libs.sage_agentic_tooluse import HybridToolSelector

# Combine keyword and embedding approaches
selector = HybridToolSelector(
    tools=available_tools,
    keyword_weight=0.3,
    embedding_weight=0.7
)

selected = selector.select(query="...", top_k=5)
```

## 📚 Key Components

### Selectors

- **KeywordToolSelector**: Fast keyword-based matching
- **EmbeddingToolSelector**: Semantic similarity using embeddings
- **HybridToolSelector**: Weighted combination of multiple selectors
- **DFSDTToolSelector**: Decision tree-based selection
- **GorillaAdapter**: Gorilla-style API-centric retrieval

### Base Classes

- **BaseToolSelector**: Abstract base for all selectors
- **ToolRegistry**: Central registry for selector implementations

### Schemas

- **Tool**: Tool representation with metadata
- **ToolSelection**: Selection result with scores
- **SelectionContext**: Context for tool selection

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
from sage_libs.sage_agentic_tooluse import HybridToolSelector

# With SAGE (when available, through interface layer)
from sage.libs.tooluse import create_selector

selector = create_selector("hybrid", tools=available_tools)
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
