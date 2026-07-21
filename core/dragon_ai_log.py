"""
Dragon Media Manager
Dragon AI logging helper.
"""

from datetime import datetime
from pathlib import Path

from core.settings import LOG_FOLDER


def dragon_ai_log(message: str):

    try:
        log_dir = Path(LOG_FOLDER)
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / "dragon_ai.log"

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"[{timestamp}] {message}\n"

        with log_file.open("a", encoding="utf-8") as handle:
            handle.write(line)

    except Exception:
        pass
