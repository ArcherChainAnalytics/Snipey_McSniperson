# src/scraper/example_scraper.py

import asyncio
from src.scraper.registry import register
from src.scraper.base import BaseScraper


@register("example")
class ExampleScraper(BaseScraper):
    async def fetch(self):
        await asyncio.sleep(0.1)
        return {"data": [1, 2, 3]}

    def parse(self, raw):
        return raw["data"]

