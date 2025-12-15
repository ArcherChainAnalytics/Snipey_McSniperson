# src/cli/scheduler.py

import asyncio
from datetime import datetime
from src.utils.logging import log


async def schedule_run(mods, persist, interval_seconds):
    """
    Simple in-process scheduler that runs the given scrapers
    every `interval_seconds` seconds.
    """

    # Import here to avoid circular import
    from src.cli.runner import run_once

    log(
        f"Starting scheduler for mods={mods} "
        f"every {interval_seconds} seconds"
    )

    while True:
        start = datetime.utcnow()
        log(f"Scheduled run at {start.isoformat()}Z")
        await run_once(mods, persist)
        log(f"Run completed, sleeping {interval_seconds} seconds...")
        await asyncio.sleep(interval_seconds)
