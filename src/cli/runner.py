# src/cli/runner.py

import argparse
import asyncio

from src.scraper.loader import load as load_scraper
from src.scraper.registry import SCRAPERS
from src.core.uploader import upload_json
from src.utils.logging import log, log_error
from src.cli.scheduler import schedule_run


# ---------------------------------------------------------
# List all registered scrapers
# ---------------------------------------------------------
def list_mods():
    if not SCRAPERS:
        print("[snipey] No scrapers registered.")
        return

    print("[snipey] Available scrapers:")
    for name in sorted(SCRAPERS.keys()):
        print(f" - {name}")


# ---------------------------------------------------------
# Run scrapers once
# ---------------------------------------------------------
async def run_once(mods, persist):
    log("Loading scrapers...")

    scrapers = [load_scraper(m) for m in mods]
    all_results = []

    for scraper in scrapers:
        name = scraper.__class__.__name__
        try:
            log(f"Running {name}...")
            raw = await scraper.fetch()
            parsed = scraper.parse(raw)
            all_results.extend(parsed)
        except Exception as exc:
            log_error(f"Scraper {name} failed: {exc}")

    if persist and all_results:
        log("Persisting results...")
        upload_json(all_results, prefix="scrapes")

    return all_results


# ---------------------------------------------------------
# CLI entrypoint
# ---------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Snipey CLI")
    parser.add_argument("--mods", nargs="+", default=[], help="Scrapers to run")
    parser.add_argument("--persist", action="store_true", help="Persist results")
    parser.add_argument("--list-mods", action="store_true", help="List available scrapers")
    parser.add_argument("--schedule", type=int, help="Run scrapers every N seconds")
    args = parser.parse_args()

    # List available scrapers
    if args.list_mods:
        list_mods()
        return

    # No scrapers specified
    if not args.mods:
        print("[snipey] No scrapers specified. Use --list-mods to see available options.")
        return

    # Scheduled mode
    if args.schedule:
        asyncio.run(schedule_run(args.mods, args.persist, args.schedule))
        return

    # Run once
    asyncio.run(run_once(args.mods, args.persist))
