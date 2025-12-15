# src/scraper/okx.py

from src.scraper.registry import register
from src.scraper.base import BaseScraper
from src.core.http import fetch_json


@register("okx")
class OKXScraper(BaseScraper):
    async def fetch(self):
        url = "https://www.okx.com/api/v5/market/tickers?instType=SPOT"
        return await fetch_json(url)

    def parse(self, raw):
        data = raw.get("data", [])
        results = []
        for item in data:
            inst_id = item.get("instId")
            last = item.get("last")
            if inst_id is None or last is None:
                continue
            try:
                price = float(last)
            except (TypeError, ValueError):
                continue
            results.append(
                {
                    "exchange": "okx",
                    "symbol": inst_id,
                    "price": price,
                }
            )
        return results
