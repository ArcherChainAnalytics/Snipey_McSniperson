# src/scraper/binance.py

from src.scraper.registry import register
from src.scraper.base import BaseScraper
from src.core.http import fetch_json


@register("binance")
class BinanceScraper(BaseScraper):
    async def fetch(self):
        url = "https://api.binance.com/api/v3/ticker/price"
        return await fetch_json(url)

    def parse(self, raw):
        return [
            {
                "exchange": "binance",
                "symbol": item["symbol"],
                "price": float(item["price"]),
            }
            for item in raw
        ]
