"""
Dragon Media Manager
Dragon AI Core — orchestration, diagnosis, and recovery.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from core.dragon_ai_config import FAILURE_THRESHOLD, MONITORED_SERVICES
from core.dragon_ai_history import DragonAIHistory
from core.dragon_ai_log import dragon_ai_log
from core.dragon_monitor import DragonMonitor, ServiceStatus, StorageStatus
from core.dragon_recovery import DragonRecovery
from core.dragon_voice import DragonVoice
from core.version import APP_NAME


@dataclass
class DragonAIState:
    mode: str = "protection"
    headline: str = "SYSTEM PROTECTION"
    status_line: str = "● All systems healthy"
    message: str = "No problems detected."
    automatic_recovery: str = "ON"
    storage_monitoring: str = "ON"
    last_check: str = "Just now"
    last_repair: str = "None required"
    attention_services: list[str] = field(default_factory=list)
    active_recovery: dict | None = None
    storage_warnings: list[str] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    error: str = ""


class DragonAI:

    def __init__(self):
        self.monitor = DragonMonitor()
        self.recovery = DragonRecovery()
        self.history = DragonAIHistory()
        self.voice = DragonVoice()
        self.state = DragonAIState()
        self._last_storage_levels: dict[str, str] = {}
        self._last_storage_available: dict[str, bool] = {}
        self._previous_service_states: dict[str, str] = {}
        self._initial_cycle_done = False
        self._docker_alert_spoken = False
        self.voice.start()

    _CAPACITY_RANK = {
        "normal": 0,
        "warning": 1,
        "critical": 2,
        "emergency": 3,
    }

    def run_cycle(self) -> DragonAIState:

        try:
            services = self.monitor.check_all_services()
            storage = self.monitor.check_storage()
            docker_status = services.get("docker")
            docker_available = (
                docker_status is not None
                and docker_status.state == "healthy"
            )

            attention: list[str] = []
            recovery_event: dict | None = None

            if not docker_available:
                attention.append("Docker")
                dragon_ai_log(
                    "Docker unavailable — dependent services cannot be "
                    "checked or recovered"
                )
                if not self._docker_alert_spoken:
                    self.voice.announce_docker_unavailable()
                    self._docker_alert_spoken = True
            else:
                self._docker_alert_spoken = False

            for service_id, status in services.items():
                if service_id == "docker":
                    continue

                previous = self._previous_service_states.get(
                    service_id,
                    "healthy",
                )

                if status.state == "healthy":
                    if previous not in ("healthy", ""):
                        self.recovery.clear_recovery_state(service_id)
                        self._record_recovery_event(
                            status.label,
                            f"{status.label} recovered",
                            "Health check passed",
                            "Service responding normally",
                            "RESOLVED",
                        )
                    self._previous_service_states[service_id] = "healthy"
                    continue

                # Docker down: report only — never restart containers.
                if not docker_available:
                    self._previous_service_states[service_id] = status.state
                    continue

                if status.state == "warning":
                    self._previous_service_states[service_id] = status.state
                    continue

                self._previous_service_states[service_id] = status.state

                if status.consecutive_failures < FAILURE_THRESHOLD:
                    continue

                config = MONITORED_SERVICES[service_id]
                if not config.get("auto_recovery"):
                    attention.append(status.label)
                    continue

                allowed, reason = self.recovery.can_attempt_recovery(
                    service_id,
                    docker_available=docker_available,
                )

                if not allowed:
                    if (
                        self.recovery._recovery_failed.get(service_id)
                        or "Maximum" in reason
                        or "manual" in reason.lower()
                    ):
                        attention.append(status.label)
                    continue

                # Confirm failure with an immediate retry before recovery.
                confirmed = self.monitor.confirm_failure(service_id)
                if confirmed.state == "healthy":
                    self._previous_service_states[service_id] = "healthy"
                    dragon_ai_log(
                        f"{status.label} recovered during confirmation retry"
                    )
                    continue

                self.voice.announce_recovery_start(status.label)

                recovery_event = self.recovery.attempt_recovery(
                    service_id,
                    self.monitor,
                    confirmed,
                    docker_available=docker_available,
                )

                if recovery_event.get("attempted"):
                    if recovery_event.get("resolved"):
                        self._record_recovery_event(
                            status.label,
                            f"{status.label} is not responding",
                            f"Restarting {status.label}...",
                            f"{status.label} responding normally",
                            "RESOLVED",
                        )
                        recovery_event["display"] = self._recovery_success_view(
                            status,
                        )
                        self.voice.announce_recovery_success(status.label)
                    else:
                        self._record_recovery_event(
                            status.label,
                            f"{status.label} is not responding",
                            f"Automatic restart attempted",
                            recovery_event.get("reason", "Verification failed"),
                            "RECOVERY FAILED",
                        )
                        attention.append(status.label)
                        recovery_event["display"] = (
                            self._recovery_failed_view(status)
                        )
                        self.voice.announce_recovery_failed(status.label)

            storage_warnings = self._process_storage(storage)

            self.state = self._build_state(
                services,
                attention,
                recovery_event,
                storage_warnings,
                docker_available,
            )

            if not self._initial_cycle_done:
                self._initial_cycle_done = True
                healthy = (
                    self.state.mode == "healthy"
                    and docker_available
                )
                storage_normal = not bool(storage_warnings)
                self.voice.announce_startup(healthy, storage_normal)

        except Exception as error:
            dragon_ai_log(f"Dragon AI internal error: {error}")
            self.state = DragonAIState(
                mode="error",
                headline="SYSTEM PROTECTION",
                status_line="● Dragon AI monitoring paused",
                message=(
                    "Dragon AI encountered an internal error but "
                    f"{APP_NAME} remains operational."
                ),
                last_check="Error",
                last_repair=self.history.get_last_repair_label(),
                history=self.history.get_recent(),
                error=str(error),
            )

        return self.state

    def _process_storage(
        self,
        storage: list[StorageStatus],
    ) -> list[str]:

        warnings: list[str] = []

        for item in storage:
            previous_level = self._last_storage_levels.get(
                item.volume_id,
                "normal",
            )
            previous_available = self._last_storage_available.get(
                item.volume_id
            )

            # --------------------------------------------------
            # Availability transitions
            # --------------------------------------------------

            if not item.available:
                warnings.append(item.message or f"{item.label} unavailable")

                if previous_available is not False:
                    self.history.add_entry(
                        item.label,
                        "Storage unavailable",
                        "Storage availability monitoring",
                        item.detail or "Configured media path inaccessible",
                        "UNAVAILABLE",
                    )
                    dragon_ai_log(
                        f"Storage unavailable: {item.label} — {item.detail}"
                    )
                    self.voice.announce_storage_unavailable(
                        item.label,
                        item.libraries,
                    )

                self._last_storage_available[item.volume_id] = False
                self._last_storage_levels[item.volume_id] = "unavailable"
                continue

            if previous_available is False:
                self.history.add_entry(
                    item.label,
                    "Storage restored",
                    "Storage availability monitoring",
                    "Library access has been restored",
                    "RESOLVED",
                )
                dragon_ai_log(f"Storage restored: {item.label}")
                self.voice.announce_storage_restored(
                    item.label,
                    item.libraries,
                )

            self._last_storage_available[item.volume_id] = True

            # --------------------------------------------------
            # Capacity warning / escalation
            # --------------------------------------------------

            if item.level != "normal" and item.message:
                warnings.append(item.message)

                previous_rank = self._CAPACITY_RANK.get(previous_level, 0)
                current_rank = self._CAPACITY_RANK.get(item.level, 0)

                if current_rank > previous_rank and item.level in (
                    "warning",
                    "critical",
                    "emergency",
                ):
                    self.history.add_entry(
                        item.label,
                        f"Storage {item.level.upper()}",
                        "Storage monitoring",
                        item.message.splitlines()[0],
                        item.level.upper(),
                    )
                    dragon_ai_log(
                        f"Storage {item.level}: {item.label}"
                    )
                    self.voice.announce_storage(item.label, item.level)

            if (
                previous_level in ("warning", "critical", "emergency")
                and item.level == "normal"
            ):
                self.history.add_entry(
                    item.label,
                    "Storage capacity recovered",
                    "Storage monitoring",
                    "Storage returned to healthy capacity levels",
                    "RESOLVED",
                )
                dragon_ai_log(
                    f"Storage capacity recovered: {item.label}"
                )
                self.voice.announce_storage_capacity_restored(item.label)

            self._last_storage_levels[item.volume_id] = item.level

        return warnings

    def report_backup_result(self, success: bool, message: str = ""):
        """
        Record and announce the result of an existing backup operation.
        """

        try:
            if success:
                self.history.add_entry(
                    "Backup",
                    "Backup completed",
                    "Manual Backup Now",
                    message or "Backup completed successfully",
                    "RESOLVED",
                )
                dragon_ai_log("Backup completed successfully")
                self.voice.announce_backup_success()
            else:
                self.history.add_entry(
                    "Backup",
                    "Backup unsuccessful",
                    "Manual Backup Now",
                    message or "Backup failed",
                    "ATTENTION REQUIRED",
                )
                dragon_ai_log(
                    f"Backup unsuccessful: {message or 'unknown error'}"
                )
                self.voice.announce_backup_failure()
        except Exception as error:
            dragon_ai_log(f"Backup notification failed: {error}")

    def _record_recovery_event(
        self,
        component: str,
        problem: str,
        action: str,
        result: str,
        outcome: str,
    ):

        self.history.add_entry(
            component,
            problem,
            action,
            result,
            outcome,
        )

    def _recovery_success_view(self, status: ServiceStatus) -> dict:

        return {
            "status_line": f"⚠ {status.label} problem detected",
            "lines": [
                f"{status.label} is not responding.",
                "Automatic Recovery:",
                f"Restarting {status.label}...",
                "Verification:",
                f"{status.label} responding normally.",
                "✓ RESOLVED",
            ],
            "last_repair": f"{status.label} automatically recovered",
        }

    def _recovery_failed_view(self, status: ServiceStatus) -> dict:

        return {
            "status_line": f"⚠ {status.label} recovery failed",
            "lines": [
                f"{status.label} remains unavailable after automatic recovery.",
                "Automatic restart attempted.",
                f"{status.label} did not recover.",
                "No further automatic restart attempts will be made.",
                "User investigation required.",
            ],
            "last_repair": f"{status.label} recovery failed",
        }

    def _build_state(
        self,
        services: dict[str, ServiceStatus],
        attention: list[str],
        recovery_event: dict | None,
        storage_warnings: list[str],
        docker_available: bool,
    ) -> DragonAIState:

        attention = list(dict.fromkeys(attention))
        history = self.history.get_recent()
        last_repair = self.history.get_last_repair_label()

        if recovery_event and recovery_event.get("display"):
            display = recovery_event["display"]
            return DragonAIState(
                mode="recovery",
                headline="SYSTEM PROTECTION",
                status_line=display["status_line"],
                message="\n".join(display["lines"]),
                last_check="Just now",
                last_repair=display.get("last_repair", last_repair),
                attention_services=attention,
                active_recovery=recovery_event,
                storage_warnings=storage_warnings,
                history=history,
            )

        if not docker_available:
            return DragonAIState(
                mode="attention",
                headline="SYSTEM PROTECTION",
                status_line="⚠ Docker unavailable",
                message=(
                    "Docker is unavailable.\n"
                    "Dependent services cannot be checked or recovered.\n"
                    "Automatic container restarts are suspended until "
                    "Docker is restored.\n"
                    "User investigation required."
                ),
                last_check="Just now",
                last_repair=last_repair,
                attention_services=attention,
                storage_warnings=storage_warnings,
                history=history,
            )

        if attention:
            lines = [
                "The following areas need attention:",
                "",
            ]
            lines.extend(f"• {item}" for item in attention)

            if storage_warnings:
                lines.append("")
                for warning in storage_warnings:
                    lines.append(warning)
                    lines.append("")

            return DragonAIState(
                mode="attention",
                headline="SYSTEM PROTECTION",
                status_line="⚠ Attention required",
                message="\n".join(lines).rstrip(),
                last_check="Just now",
                last_repair=last_repair,
                attention_services=attention,
                storage_warnings=storage_warnings,
                history=history,
            )

        message_lines = ["No problems detected."]

        if storage_warnings:
            message_lines.append("")
            for warning in storage_warnings:
                message_lines.append(warning)

        return DragonAIState(
            mode="healthy",
            headline="SYSTEM PROTECTION",
            status_line="● All systems healthy",
            message="\n".join(message_lines),
            last_check="Just now",
            last_repair=last_repair,
            storage_warnings=storage_warnings,
            history=history,
        )

    def get_panel_state(self) -> DragonAIState:

        return self.state

    def shutdown(self):

        try:
            self.voice.stop()
        except Exception:
            pass
