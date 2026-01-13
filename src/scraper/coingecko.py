# src/scraper/coingecko.py

from src.scraper.registry import register
from src.scraper.base import BaseScraper
from src.core.http import fetch_json


@register("coingecko")
class CoinGeckoScraper(BaseScraper):
    async def fetch(self):
        url = (
            "https://api.coingecko.com/api/v3/simple/price"
            "?ids=bitcoin,ethereum&vs_currencies=usd"
        )
        return await fetch_json(url)

    def parse(self, raw):
        btc = raw.get("bitcoin", {}).get("usd")
        eth = raw.get("ethereum", {}).get("usd")

        results = []
        if btc is not None:
            results.append(
                {"exchange": "coingecko", "symbol": "BTC", "price": float(btc)}
            )
        if eth is not None:
            results.append(
                {"exchange": "coingecko", "symbol": "ETH", "price": float(eth)}
            )
        return results
