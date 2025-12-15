# src/scraper/kucoin.py

from src.scraper.registry import register
from src.scraper.base import BaseScraper
from src.core.http import fetch_json


@register("kucoin")
class KuCoinScraper(BaseScraper):
    async def fetch(self):
        url = "https://api.kucoin.com/api/v1/prices"
        return await fetch_json(url)

    def parse(self, raw):
        data = raw.get("data", {})
        results = []
        for symbol, price in data.items():
            try:
                price_f = float(price)
            except (TypeError, ValueError):
                continue
            results.append(
                {
                    "exchange": "kucoin",
                    "symbol": symbol,
                    "price": price_f,
                }
            )
        return results
