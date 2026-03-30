"""Smoke tests for sage-agentic-tooluse."""


def test_import_package() -> None:
    import sage_libs.sage_agentic_tooluse as tooluse

    assert tooluse.__version__


def test_registry_has_builtin_selectors() -> None:
    from sage_libs.sage_agentic_tooluse import SelectorRegistry

    names = SelectorRegistry.get_instance().list_selectors()
    for expected in ["keyword", "embedding", "hybrid", "gorilla", "dfsdt"]:
        assert expected in names
