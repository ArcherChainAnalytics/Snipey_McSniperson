# src/scraper/kraken.py

from src.scraper.registry import register
from src.scraper.base import BaseScraper
from src.core.http import fetch_json


@register("kraken")
class KrakenScraper(BaseScraper):
    async def fetch(self):
        # Example pairs; adjust as needed
        url = "https://api.kraken.com/0/public/Ticker?pair=BTCUSD,ETHUSD"
        return await fetch_json(url)

    def parse(self, raw):
        results = []
        result = raw.get("result", {})
        for pair, data in result.items():
            price = float(data["c"][0])
            results.append(
                {
                    "exchange": "kraken",
                    "symbol": pair,
                    "price": price,
                }
            )
        return results
