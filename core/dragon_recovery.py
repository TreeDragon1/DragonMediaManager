"""
Dragon Media Manager
Dragon AI controlled automatic recovery.
"""

from __future__ import annotations

import time

from core.actions import DragonActions
from core.dragon_ai_config import (
    MAX_AUTO_RECOVERY_ATTEMPTS,
    MONITORED_SERVICES,
    RECOVERY_COOLDOWN_SECONDS,
    STARTUP_WAIT_SECONDS,
)
from core.dragon_ai_log import dragon_ai_log
from core.dragon_monitor import DragonMonitor, ServiceStatus


class DragonRecovery:

    def __init__(self):
        self.actions = DragonActions()
        self._last_restart: dict[str, float] = {}
        self._attempt_counts: dict[str, int] = {}
        self._recovery_failed: dict[str, bool] = {}

    def can_attempt_recovery(
        self,
        service_id: str,
        docker_available: bool = True,
    ) -> tuple[bool, str]:

        config = MONITORED_SERVICES.get(service_id, {})

        if not docker_available:
            return False, "Docker unavailable"

        if not config.get("auto_recovery"):
            return False, "Automatic recovery not enabled for this service"

        if self._recovery_failed.get(service_id):
            return False, "Recovery failed — manual attention required"

        attempts = self._attempt_counts.get(service_id, 0)
        if attempts >= MAX_AUTO_RECOVERY_ATTEMPTS:
            self._recovery_failed[service_id] = True
            return False, "Maximum automatic recovery attempts reached"

        last = self._last_restart.get(service_id, 0.0)
        elapsed = time.time() - last

        if last and elapsed < RECOVERY_COOLDOWN_SECONDS:
            remaining = int(RECOVERY_COOLDOWN_SECONDS - elapsed)
            return False, f"Cooldown active ({remaining}s remaining)"

        return True, ""

    def mark_recovery_failed(self, service_id: str):

        self._recovery_failed[service_id] = True

    def clear_recovery_state(self, service_id: str):

        self._recovery_failed.pop(service_id, None)
        self._attempt_counts.pop(service_id, None)

    def attempt_recovery(
        self,
        service_id: str,
        monitor: DragonMonitor,
        status: ServiceStatus,
        docker_available: bool = True,
    ) -> dict:

        config = MONITORED_SERVICES[service_id]
        label = config["label"]
        allowed, reason = self.can_attempt_recovery(
            service_id,
            docker_available=docker_available,
        )

        if not allowed:
            return {
                "attempted": False,
                "service_id": service_id,
                "label": label,
                "reason": reason,
                "resolved": False,
                "state": "recovery_failed" if self._recovery_failed.get(service_id) else "warning",
            }

        restart_method = config.get("restart_method")
        if not restart_method:
            return {
                "attempted": False,
                "service_id": service_id,
                "label": label,
                "reason": "No restart method configured",
                "resolved": False,
                "state": "warning",
            }

        attempt_number = self._attempt_counts.get(service_id, 0) + 1
        self._attempt_counts[service_id] = attempt_number
        self._last_restart[service_id] = time.time()

        dragon_ai_log(
            f"Recovery attempt {attempt_number}/"
            f"{MAX_AUTO_RECOVERY_ATTEMPTS} for {label}: {status.detail}"
        )

        restart_fn = getattr(self.actions, restart_method)
        success, message = restart_fn()

        if not success:
            if attempt_number >= MAX_AUTO_RECOVERY_ATTEMPTS:
                self.mark_recovery_failed(service_id)

            dragon_ai_log(
                f"Recovery failed for {label}: restart command failed ({message})"
            )
            return {
                "attempted": True,
                "service_id": service_id,
                "label": label,
                "reason": message or "Restart command failed",
                "resolved": False,
                "verified": False,
                "attempt": attempt_number,
                "state": "recovery_failed",
            }

        time.sleep(STARTUP_WAIT_SECONDS)
        verified_status = monitor.verify_service(service_id)
        resolved = verified_status.state == "healthy"

        if resolved:
            monitor.reset_failure_count(service_id)
            self.clear_recovery_state(service_id)
            dragon_ai_log(
                f"Recovery verified for {label}: service responding normally"
            )
            return {
                "attempted": True,
                "service_id": service_id,
                "label": label,
                "reason": verified_status.detail,
                "resolved": True,
                "verified": True,
                "attempt": attempt_number,
                "state": "healthy",
                "verified_status": verified_status,
            }

        if attempt_number >= MAX_AUTO_RECOVERY_ATTEMPTS:
            self.mark_recovery_failed(service_id)

        dragon_ai_log(
            f"Recovery verification failed for {label}: still unhealthy"
        )

        return {
            "attempted": True,
            "service_id": service_id,
            "label": label,
            "reason": verified_status.detail,
            "resolved": False,
            "verified": True,
            "attempt": attempt_number,
            "state": "recovery_failed",
            "verified_status": verified_status,
        }
