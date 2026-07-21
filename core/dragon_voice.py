"""
Dragon Media Centre
Dragon AI local Piper TTS voice engine.

Completely offline. Never falls back to eSpeak.
"""

from __future__ import annotations

import json
import queue
import subprocess
import tempfile
import threading
import time
from pathlib import Path

from core.dragon_ai_log import dragon_ai_log
from core.version import APP_NAME


VOICE_DATA_DIR = Path.home() / ".local" / "share" / "dragon-media-centre"
VOICE_DIR = VOICE_DATA_DIR / "voices"
PREF_PATH = VOICE_DATA_DIR / "voice_prefs.json"
PIPER_BIN = VOICE_DATA_DIR / "piper" / "piper"
VOICE_MODEL = VOICE_DIR / "en_GB-alba-medium.onnx"
VOICE_CONFIG = VOICE_DIR / "en_GB-alba-medium.onnx.json"

# Do not re-speak identical event keys within this window.
ANNOUNCEMENT_COOLDOWN_SECONDS = 600


class DragonVoice:

    def __init__(self):
        self._queue: queue.Queue[tuple[str, str] | None] = queue.Queue()
        self._worker: threading.Thread | None = None
        self._stop = threading.Event()
        self._started = False
        self._lock = threading.Lock()
        self._last_spoken: dict[str, float] = {}
        self._startup_announced = False
        self.enabled = True
        self._load_prefs()

    # --------------------------------------------------
    # Preferences
    # --------------------------------------------------

    def _load_prefs(self):

        try:
            if PREF_PATH.is_file():
                data = json.loads(PREF_PATH.read_text(encoding="utf-8"))
                self.enabled = bool(data.get("voice_enabled", True))
        except Exception as error:
            dragon_ai_log(f"Voice preference load failed: {error}")
            self.enabled = True

    def _save_prefs(self):

        try:
            VOICE_DATA_DIR.mkdir(parents=True, exist_ok=True)
            PREF_PATH.write_text(
                json.dumps({"voice_enabled": self.enabled}, indent=2),
                encoding="utf-8",
            )
        except Exception as error:
            dragon_ai_log(f"Voice preference save failed: {error}")

    def set_enabled(self, enabled: bool):

        self.enabled = bool(enabled)
        self._save_prefs()

    def toggle(self) -> bool:

        self.set_enabled(not self.enabled)
        return self.enabled

    # --------------------------------------------------
    # Availability
    # --------------------------------------------------

    def is_available(self) -> bool:

        return (
            PIPER_BIN.is_file()
            and os_access_executable(PIPER_BIN)
            and VOICE_MODEL.is_file()
            and VOICE_CONFIG.is_file()
        )

    # --------------------------------------------------
    # Queue lifecycle
    # --------------------------------------------------

    def start(self):

        with self._lock:
            if self._started:
                return

            self._stop.clear()
            self._worker = threading.Thread(
                target=self._worker_loop,
                name="DragonVoiceWorker",
                daemon=True,
            )
            self._worker.start()
            self._started = True

    def stop(self):

        with self._lock:
            if not self._started:
                return

            self._stop.set()
            try:
                self._queue.put_nowait(None)
            except Exception:
                pass

            worker = self._worker
            self._worker = None
            self._started = False

        if worker is not None and worker.is_alive():
            worker.join(timeout=2.0)

    def speak(
        self,
        text: str,
        event_key: str | None = None,
        force: bool = False,
    ):

        if not text or not text.strip():
            return

        # Automatic announcements respect Voice ON/OFF.
        # Speak Status uses force=True as an explicit user request.
        if not self.enabled and not force:
            return

        key = event_key or text.strip()

        if not force and self._is_duplicate(key):
            return

        if not force:
            self._last_spoken[key] = time.time()

        try:
            self.start()
            self._queue.put_nowait((key, text.strip()))
        except Exception as error:
            dragon_ai_log(f"Voice queue error: {error}")

    def _is_duplicate(self, key: str) -> bool:

        last = self._last_spoken.get(key)
        if last is None:
            return False

        return (time.time() - last) < ANNOUNCEMENT_COOLDOWN_SECONDS

    def _worker_loop(self):

        while not self._stop.is_set():
            try:
                item = self._queue.get(timeout=0.5)
            except queue.Empty:
                continue

            if item is None:
                break

            _key, text = item

            try:
                self._speak_blocking(text)
            except Exception as error:
                dragon_ai_log(f"Voice playback failed: {error}")
            finally:
                try:
                    self._queue.task_done()
                except Exception:
                    pass

    def _speak_blocking(self, text: str):

        if not self.is_available():
            dragon_ai_log(
                "Voice unavailable: Piper binary or voice model missing"
            )
            return

        with tempfile.NamedTemporaryFile(
            prefix="dragon_voice_",
            suffix=".wav",
            delete=False,
        ) as handle:
            wav_path = Path(handle.name)

        try:
            process = subprocess.run(
                [
                    str(PIPER_BIN),
                    "--model",
                    str(VOICE_MODEL),
                    "--output_file",
                    str(wav_path),
                ],
                input=text.encode("utf-8"),
                capture_output=True,
                timeout=60,
                check=False,
            )

            if process.returncode != 0:
                stderr = (process.stderr or b"").decode("utf-8", errors="ignore")
                raise RuntimeError(
                    f"Piper failed (code {process.returncode}): {stderr[:200]}"
                )

            play = subprocess.run(
                ["paplay", str(wav_path)],
                capture_output=True,
                timeout=120,
                check=False,
            )

            if play.returncode != 0:
                play = subprocess.run(
                    ["aplay", str(wav_path)],
                    capture_output=True,
                    timeout=120,
                    check=False,
                )
                if play.returncode != 0:
                    raise RuntimeError("Audio playback failed (paplay/aplay)")

        finally:
            try:
                wav_path.unlink(missing_ok=True)
            except Exception:
                pass

    # --------------------------------------------------
    # Announcement helpers
    # --------------------------------------------------

    @staticmethod
    def _time_aware_greeting(name: str = "Peter") -> str:
        """Return a local-time greeting. Uses the machine clock only."""

        from datetime import datetime

        hour = datetime.now().hour

        if 5 <= hour <= 11:
            return f"Good morning, {name}."
        if 12 <= hour <= 16:
            return f"Good afternoon, {name}."
        if 17 <= hour <= 21:
            return f"Good evening, {name}."
        return f"Good night, {name}."

    def announce_startup(self, healthy: bool, storage_normal: bool):

        if self._startup_announced:
            return

        self._startup_announced = True

        if not healthy:
            return

        greeting = self._time_aware_greeting("Peter")

        if storage_normal:
            text = (
                f"{greeting} {APP_NAME} is online. All systems are healthy "
                "and storage levels are normal."
            )
        else:
            text = (
                f"{greeting} {APP_NAME} is online. Monitored services are "
                "healthy. Please review current storage warnings."
            )

        self.speak(text, event_key="startup_healthy", force=False)

    def announce_recovery_start(self, service_label: str):

        self.speak(
            (
                f"{service_label} has stopped responding. "
                "I am attempting automatic recovery."
            ),
            event_key=f"recovery_start:{service_label}",
        )

    def announce_recovery_success(self, service_label: str):

        self.speak(
            (
                f"{service_label} has been restarted and is "
                "responding normally."
            ),
            event_key=f"recovery_success:{service_label}",
        )

    def announce_recovery_failed(self, service_label: str):

        self.speak(
            (
                f"Attention. I was unable to recover {service_label} "
                "automatically. Manual attention is required."
            ),
            event_key=f"recovery_failed:{service_label}",
        )

    def announce_docker_unavailable(self):

        self.speak(
            (
                "Attention. Docker is unavailable. Automatic recovery "
                "of media services has been suspended."
            ),
            event_key="docker_unavailable",
        )

    def announce_storage(self, label: str, level: str):

        if level == "warning":
            text = (
                f"Storage warning. Your {label} is running low. "
                "I recommend planning a storage upgrade."
            )
        elif level == "critical":
            text = (
                f"Critical storage warning. Your {label} is critically low. "
                "A storage upgrade is recommended soon."
            )
        elif level == "emergency":
            text = (
                f"Emergency storage warning. Your {label} has very little "
                "free space remaining. Additional downloads or media "
                "imports may fail."
            )
        else:
            return

        self.speak(text, event_key=f"storage_capacity:{label}:{level}")

    def announce_storage_capacity_restored(self, label: str):

        self.speak(
            f"{label} capacity has returned to a healthy level.",
            event_key=f"storage_capacity_restored:{label}",
        )

    def announce_storage_unavailable(self, label: str, libraries: list[str] | None = None):

        libraries = libraries or []

        if "Movies" in libraries and "TV" not in " ".join(libraries):
            text = (
                "Attention. Movies storage is unavailable. "
                "I cannot access the Movies library."
            )
        elif any("TV" in item or "Episodes" in item for item in libraries):
            text = (
                "Attention. TV Series storage is unavailable. "
                "I cannot access the TV Shows and Episodes library."
            )
        elif "movies" in label.lower():
            text = (
                "Attention. Movies storage is unavailable. "
                "I cannot access the Movies library."
            )
        elif "tv" in label.lower():
            text = (
                "Attention. TV Series storage is unavailable. "
                "I cannot access the TV Shows and Episodes library."
            )
        else:
            text = (
                f"Attention. {label} is unavailable. "
                "I cannot access the media library."
            )

        self.speak(text, event_key=f"storage_unavailable:{label}")

    def announce_storage_restored(self, label: str, libraries: list[str] | None = None):

        libraries = libraries or []

        if "Movies" in libraries and not any(
            "TV" in item or "Episodes" in item for item in libraries
        ):
            text = (
                "Movies storage is available again. "
                "Library access has been restored."
            )
        elif any("TV" in item or "Episodes" in item for item in libraries):
            text = (
                "TV Series storage is available again. "
                "Library access has been restored."
            )
        elif "movies" in label.lower():
            text = (
                "Movies storage is available again. "
                "Library access has been restored."
            )
        elif "tv" in label.lower():
            text = (
                "TV Series storage is available again. "
                "Library access has been restored."
            )
        else:
            text = (
                f"{label} is available again. "
                "Library access has been restored."
            )

        self.speak(text, event_key=f"storage_restored:{label}")

    def announce_backup_success(self):

        self.speak(
            f"{APP_NAME} backup completed successfully.",
            event_key="backup_success",
        )

    def announce_backup_failure(self):

        self.speak(
            (
                f"Attention. The {APP_NAME} backup was unsuccessful. "
                "Please check the backup system."
            ),
            event_key="backup_failure",
        )

    def speak_status_summary(self, summary: str):

        # Explicit user request — speak even if automatic voice is off.
        self.speak(summary, event_key=None, force=True)


def os_access_executable(path: Path) -> bool:

    try:
        return path.is_file() and (path.stat().st_mode & 0o111) != 0
    except Exception:
        return False


def build_status_summary(state) -> str:

    parts = [f"{APP_NAME} system status."]

    if getattr(state, "mode", "") == "healthy":
        parts.append("All monitored services are healthy.")
        parts.append("Automatic recovery is active.")
        if getattr(state, "storage_warnings", None):
            parts.append("There are current storage notices.")
        else:
            parts.append("Storage levels are normal.")
        parts.append("No repairs are currently required.")
        return " ".join(parts)

    if getattr(state, "mode", "") == "attention":
        attention = getattr(state, "attention_services", []) or []
        if attention:
            names = ", ".join(attention[:4])
            parts.append(f"Attention is required for {names}.")
        else:
            parts.append("Attention is currently required.")

        if getattr(state, "storage_warnings", None):
            parts.append("Storage warnings are active.")

        parts.append("Automatic recovery remains available where permitted.")
        return " ".join(parts)

    if getattr(state, "mode", "") == "recovery":
        recovery = getattr(state, "active_recovery", None) or {}
        label = recovery.get("label", "a service")
        if recovery.get("resolved"):
            parts.append(
                f"{label} was automatically recovered and is responding normally."
            )
        else:
            parts.append(
                f"Automatic recovery for {label} did not succeed. "
                "Manual attention is required."
            )
        return " ".join(parts)

    parts.append(
        "Dragon AI monitoring is active. Please check the protection panel "
        "for the latest details."
    )
    return " ".join(parts)
