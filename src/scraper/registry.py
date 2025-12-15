# src/scraper/registry.py

import pkgutil
import importlib
import os

SCRAPERS = {}


def register(name):
    """
    Decorator to register a scraper class by name.
    """

    def decorator(cls):
        SCRAPERS[name] = cls
        return cls

    return decorator


# ---------------------------------------------------------
# Auto-import core scrapers from src.scraper package
# ---------------------------------------------------------
_scraper_pkg_name = "src.scraper"
_scraper_pkg = importlib.import_module(_scraper_pkg_name)

for _, module_name, _ in pkgutil.iter_modules(_scraper_pkg.__path__):
    if module_name not in ("base", "loader", "registry"):
        importlib.import_module(f"{_scraper_pkg_name}.{module_name}")


# ---------------------------------------------------------
# Plugin loading from ./plugins directory (optional)
# ---------------------------------------------------------
def _load_plugins():
    """
    Load additional scraper modules from a top-level ./plugins directory.
    Each plugin file can use @register() exactly like core scrapers.
    """
    # Base dir is one level above src/
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    plugins_dir = os.path.join(base_dir, "plugins")

    if not os.path.isdir(plugins_dir):
        return

    for filename in os.listdir(plugins_dir):
        if not filename.endswith(".py"):
            continue

        module_name = filename[:-4]
        path = os.path.join(plugins_dir, filename)

        spec = importlib.util.spec_from_file_location(
            f"plugins.{module_name}", path
        )
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)


import importlib.util
import types

# Load plugins after core scrapers
_load_plugins()
