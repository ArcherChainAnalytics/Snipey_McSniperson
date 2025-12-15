import sys
from datetime import datetime

LEVEL_INFO = "INFO"
LEVEL_ERROR = "ERROR"

def _fmt(level, message):
    ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    return f"[{ts}] [snipey] [{level}] {message}"

def log(message):
    """Info-level log."""
    sys.stdout.write(_fmt(LEVEL_INFO, message) + "\n")
    sys.stdout.flush()

def log_error(message):
    """Error-level log."""
    sys.stderr.write(_fmt(LEVEL_ERROR, message) + "\n")
    sys.stderr.flush()
