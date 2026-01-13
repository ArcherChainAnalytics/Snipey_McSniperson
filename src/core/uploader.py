# src/core/uploader.py

import json
import os
from datetime import datetime
from src.core.config import CFG
from src.utils.logging import log


def upload_json(data, prefix="data"):
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    os.makedirs(CFG.storage_path, exist_ok=True)
    path = os.path.join(CFG.storage_path, f"{prefix}_{ts}.json")

    with open(path, "w") as f:
        json.dump(data, f, indent=2)

    log(f"Saved: {path}")
