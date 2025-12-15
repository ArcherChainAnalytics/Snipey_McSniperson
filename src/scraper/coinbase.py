# src/scraper/coinbase.py

from src.scraper.registry import register
from src.scraper.base import BaseScraper
from src.core.http import fetch_json


@register("coinbase")
class CoinbaseScraper(BaseScraper):
    async def fetch(self):
        # BTC base rates
        url = "https://api.coinbase.com/v2/exchange-rates?currency=BTC"
        return await fetch_json(url)

    def parse(self, raw):
        data = raw.get("data", {})
        rates = data.get("rates", {})
        usd = rates.get("USD")
        if usd is None:
            return []
        return [
            {
                "exchange": "coinbase",
                "symbol": "BTC",
                "price": float(usd),
            }
        ]
