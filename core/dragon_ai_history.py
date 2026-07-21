"""
Dragon Media Manager
Dragon AI persistent troubleshooting history.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

from core.dragon_ai_config import HISTORY_MAX_ENTRIES
from core.settings import LOG_FOLDER


class DragonAIHistory:

    def __init__(self, path: Path | None = None):
        log_dir = Path(LOG_FOLDER)
        self.path = path or (log_dir / "dragon_ai_history.json")
        self._entries: list[dict] = []
        self._load()

    def _load(self):

        try:
            if self.path.is_file():
                data = json.loads(self.path.read_text(encoding="utf-8"))
                if isinstance(data, list):
                    self._entries = data[-HISTORY_MAX_ENTRIES:]
                    return
        except Exception:
            pass

        self._entries = []

    def _save(self):

        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self.path.write_text(
                json.dumps(self._entries, indent=2),
                encoding="utf-8",
            )
        except Exception:
            pass

    def add_entry(
        self,
        component: str,
        problem: str,
        action: str,
        result: str,
        outcome: str,
    ):

        entry = {
            "timestamp": time.strftime("%H:%M"),
            "epoch": int(time.time()),
            "component": component,
            "problem": problem,
            "action": action,
            "result": result,
            "outcome": outcome,
        }

        self._entries.append(entry)

        if len(self._entries) > HISTORY_MAX_ENTRIES:
            self._entries = self._entries[-HISTORY_MAX_ENTRIES:]

        self._save()
        return entry

    def get_recent(self, limit: int = 8) -> list[dict]:

        return list(self._entries[-limit:])

    def get_last_repair_label(self) -> str:

        for entry in reversed(self._entries):
            outcome = str(entry.get("outcome", "")).upper()
            action = str(entry.get("action", "")).lower()
            component = str(entry.get("component", "Service"))

            if outcome == "RESOLVED" and (
                "restart" in action or "recovery" in action or "restarting" in action
            ):
                return f"{component} automatically recovered"

            if outcome == "RECOVERY FAILED":
                return f"{component} recovery failed"

            if "restart" in action or "recovery" in action or "restarting" in action:
                return self._relative_time(entry.get("epoch", 0))

        return "None required"

    @staticmethod
    def _relative_time(epoch: int) -> str:

        if not epoch:
            return "None required"

        age = max(0, int(time.time()) - int(epoch))

        if age < 60:
            return "Just now"

        if age < 3600:
            return f"{age // 60}m ago"

        if age < 86400:
            return f"{age // 3600}h ago"

        return f"{age // 86400}d ago"
