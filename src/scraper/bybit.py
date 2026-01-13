# src/scraper/bybit.py

from src.scraper.registry import register
from src.scraper.base import BaseScraper
from src.core.http import fetch_json


@register("bybit")
class BybitScraper(BaseScraper):
    async def fetch(self):
        url = "https://api.bybit.com/v5/market/tickers?category=spot"
        return await fetch_json(url)

    def parse(self, raw):
        result = raw.get("result", {})
        items = result.get("list", [])
        outputs = []
        for item in items:
            symbol = item.get("symbol")
            last_price = item.get("lastPrice")
            if symbol is None or last_price is None:
                continue
            try:
                price = float(last_price)
            except (TypeError, ValueError):
                continue
            outputs.append(
                {
                    "exchange": "bybit",
                    "symbol": symbol,
                    "price": price,
                }
            )
        return outputs
