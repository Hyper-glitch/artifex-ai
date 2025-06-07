"""
This module is used to provide configuration, plugins, and plugins for pytest.

It may be also used for extending doctest's context:
1. https://docs.python.org/3/library/doctest.html
2. https://docs.pytest.org/en/latest/doctest.html
"""

from pathlib import Path


def _discover_plugins(package: str) -> list[str]:
    """Discover modules and convert a path to a module-like string."""
    parent = Path(__file__).parent
    plugin_dir = parent.joinpath(package)

    return [
        path.relative_to(parent).with_suffix("").as_posix().replace("/", ".")
        for path in plugin_dir.rglob("*.py")
    ]


pytest_plugins = _discover_plugins("plugins")
