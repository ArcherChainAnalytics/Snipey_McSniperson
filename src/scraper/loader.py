from src.scraper.registry import SCRAPERS

def load(name):
    """Load a scraper instance by name."""
    if name not in SCRAPERS:
        raise KeyError(f"Scraper '{name}' not found")
    return SCRAPERS[name]()
