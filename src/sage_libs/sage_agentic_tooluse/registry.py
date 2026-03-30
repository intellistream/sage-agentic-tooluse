"""
Registry for tool selector strategies.

Provides registration, lookup, and factory creation of selectors.
"""

import logging
from typing import Any

from .base import BaseToolSelector, SelectorResources
from .schemas import CONFIG_TYPES, SelectorConfig, create_selector_config

logger = logging.getLogger(__name__)


class SelectorRegistry:
    """
    Registry for tool selector strategies.

    Supports registration, lookup, and factory creation of selectors.
    """

    def __init__(self):
        """Initialize registry."""
        self._selectors = {}
        self._instances: dict[str, BaseToolSelector] = {}

    def register(self, name: str, selector_class: type[BaseToolSelector]) -> None:
        """
        Register a selector class.

        Args:
            name: Selector strategy name
            selector_class: Selector class to register
        """
        if name in self._selectors:
            logger.warning(f"Overwriting existing selector: {name}")

        self._selectors[name] = selector_class
        logger.info(f"Registered selector: {name}")

    def get_class(self, name: str) -> type[BaseToolSelector] | None:
        """
        Get selector class by name.

        Args:
            name: Selector strategy name

        Returns:
            Selector class or None if not found
        """
        return self._selectors.get(name)

    def create(
        self,
        name: str,
        resources: SelectorResources,
        config: SelectorConfig | None = None,
        cache: bool = True,
    ) -> BaseToolSelector:
        """
        Get or create selector instance.

        Args:
            name: Selector strategy name
            resources: Shared resources
            config: Optional selector configuration
            cache: Whether to cache and reuse instances

        Returns:
            Selector instance

        Raises:
            ValueError: If selector not registered
        """
        # Check cache
        if cache and name in self._instances:
            return self._instances[name]

        # Get class
        selector_class = self.get_class(name)
        if selector_class is None:
            raise ValueError(f"Unknown selector: {name}. Available: {list(self._selectors.keys())}")

        # Create config if needed
        if config is None:
            config = create_selector_config({"name": name})

        # Create instance
        instance = selector_class.from_config(config, resources)

        # Cache if requested
        if cache:
            self._instances[name] = instance

        return instance

    def create_from_config(
        self, config_dict: dict[str, Any], resources: SelectorResources
    ) -> BaseToolSelector:
        """
        Create selector from configuration dictionary.

        Args:
            config_dict: Configuration dictionary
            resources: Shared resources

        Returns:
            Initialized selector instance
        """
        selector_name = config_dict.get("name", "keyword")

        if selector_name in CONFIG_TYPES:
            config = create_selector_config(config_dict)
            return self.create(config.name, resources, config, cache=False)

        selector_class = self.get_class(selector_name)
        if selector_class is None:
            raise ValueError(f"Unknown selector type: {selector_name}")

        config = SelectorConfig(**config_dict)
        return self.create(selector_name, resources, config, cache=False)

    def list_selectors(self) -> list:
        """List all registered selector names."""
        return list(self._selectors.keys())

    def clear_cache(self) -> None:
        """Clear cached selector instances."""
        self._instances.clear()
        logger.info("Cleared selector instance cache")


# Global registry instance
_registry = SelectorRegistry()


def register_selector(name: str, selector_class: type[BaseToolSelector]) -> None:
    """
    Register a selector class globally.

    Args:
        name: Selector strategy name
        selector_class: Selector class to register
    """
    _registry.register(name, selector_class)


def create_selector(
    config_dict: dict[str, Any], resources: SelectorResources
) -> BaseToolSelector:
    """
    Create selector from config dictionary using global registry.

    Args:
        config_dict: Configuration dictionary
        resources: Shared resources

    Returns:
        Initialized selector instance
    """
    return _registry.create_from_config(config_dict, resources)
