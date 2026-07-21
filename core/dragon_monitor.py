"""
Dragon Media Manager
Dragon AI service and storage monitoring.
"""

from __future__ import annotations

import os
import subprocess
import time
from dataclasses import dataclass, field

import psutil
import requests

from core.dragon_ai_config import (
    CONFIRMATION_RETRIES,
    CONFIRMATION_RETRY_DELAY_SECONDS,
    FAILURE_THRESHOLD,
    MONITORED_SERVICES,
    STORAGE_CRITICAL_FREE_GB,
    STORAGE_CRITICAL_PERCENT_FREE,
    STORAGE_EMERGENCY_FREE_GB,
    STORAGE_EMERGENCY_PERCENT_FREE,
    STORAGE_VOLUMES,
    STORAGE_WARNING_FREE_GB,
    STORAGE_WARNING_PERCENT_FREE,
)
from core.docker_status import DockerStatus


@dataclass
class ServiceStatus:
    service_id: str
    label: str
    state: str
    container_running: bool | None = None
    application_responding: bool | None = None
    detail: str = ""
    consecutive_failures: int = 0


@dataclass
class StorageStatus:
    volume_id: str
    label: str
    path: str
    libraries: list[str] = field(default_factory=list)
    total_gb: float = 0.0
    used_gb: float = 0.0
    free_gb: float = 0.0
    percent_used: float = 0.0
    percent_free: float = 0.0
    level: str = "normal"
    available: bool = True
    message: str = ""
    detail: str = ""


class DragonMonitor:

    def __init__(self):
        self.docker_status = DockerStatus()
        self._failure_counts: dict[str, int] = {}

    def check_docker_daemon(self) -> bool:

        try:
            result = subprocess.run(
                ["docker", "info"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            return result.returncode == 0
        except Exception:
            return False

    def check_container_running(self, container: str) -> bool:

        try:
            result = subprocess.run(
                [
                    "docker",
                    "inspect",
                    "-f",
                    "{{.State.Running}}",
                    container,
                ],
                capture_output=True,
                text=True,
                timeout=10,
            )
            return result.stdout.strip().lower() == "true"
        except Exception:
            return False

    def check_http_health(self, url: str, path: str) -> bool:

        try:
            response = requests.get(
                f"{url.rstrip('/')}{path}",
                timeout=5,
                allow_redirects=True,
            )
            return response.status_code < 500
        except Exception:
            return False

    def check_qbittorrent_health(self) -> bool:

        try:
            from core.dragon_downloads import DragonDownloads

            engine = DragonDownloads()
            data = engine.get_downloads()
            return bool(data.get("connected"))
        except Exception:
            return False

    def _evaluate_service(
        self,
        service_id: str,
        config: dict,
        docker_ok: bool,
    ) -> ServiceStatus:

        label = config["label"]
        container = config.get("container")

        if service_id == "docker":
            if docker_ok:
                return ServiceStatus(
                    service_id=service_id,
                    label=label,
                    state="healthy",
                    detail="Docker daemon responding",
                )

            self._failure_counts[service_id] = (
                self._failure_counts.get(service_id, 0) + 1
            )
            return ServiceStatus(
                service_id=service_id,
                label=label,
                state="offline",
                detail="Docker daemon unavailable",
                consecutive_failures=self._failure_counts[service_id],
            )

        if not docker_ok:
            return ServiceStatus(
                service_id=service_id,
                label=label,
                state="warning",
                container_running=None,
                application_responding=None,
                detail="Docker unavailable — dependent service cannot be checked",
                consecutive_failures=0,
            )

        container_running = (
            self.check_container_running(container)
            if container
            else False
        )

        app_ok = False

        if container_running:
            if config.get("use_qbittorrent_api"):
                app_ok = self.check_qbittorrent_health()
            elif config.get("url") and config.get("health_path") is not None:
                app_ok = self.check_http_health(
                    config["url"],
                    config["health_path"],
                )
            else:
                app_ok = True

        if container_running and app_ok:
            self._failure_counts[service_id] = 0
            return ServiceStatus(
                service_id=service_id,
                label=label,
                state="healthy",
                container_running=True,
                application_responding=True,
                detail="Service healthy",
            )

        if not container_running:
            self._failure_counts[service_id] = (
                self._failure_counts.get(service_id, 0) + 1
            )
            failures = self._failure_counts[service_id]
            state = (
                "offline"
                if failures >= FAILURE_THRESHOLD
                else "warning"
            )
            return ServiceStatus(
                service_id=service_id,
                label=label,
                state=state,
                container_running=False,
                application_responding=False,
                detail="Container not running",
                consecutive_failures=failures,
            )

        self._failure_counts[service_id] = (
            self._failure_counts.get(service_id, 0) + 1
        )
        failures = self._failure_counts[service_id]
        state = (
            "offline"
            if failures >= FAILURE_THRESHOLD
            else "warning"
        )

        return ServiceStatus(
            service_id=service_id,
            label=label,
            state=state,
            container_running=True,
            application_responding=False,
            detail="Container running but application not responding",
            consecutive_failures=failures,
        )

    def check_all_services(self) -> dict[str, ServiceStatus]:

        docker_ok = self.check_docker_daemon()
        results: dict[str, ServiceStatus] = {}

        for service_id, config in MONITORED_SERVICES.items():
            results[service_id] = self._evaluate_service(
                service_id,
                config,
                docker_ok,
            )

        return results

    def verify_service(self, service_id: str) -> ServiceStatus:

        config = MONITORED_SERVICES[service_id]
        docker_ok = self.check_docker_daemon()
        return self._evaluate_service(service_id, config, docker_ok)

    def confirm_failure(self, service_id: str) -> ServiceStatus:
        """
        Retry a failing service before declaring recovery necessary.
        """

        status = self.verify_service(service_id)

        for _ in range(CONFIRMATION_RETRIES):
            if status.state == "healthy":
                return status

            time.sleep(CONFIRMATION_RETRY_DELAY_SECONDS)
            status = self.verify_service(service_id)

        return status

    def _storage_level(self, percent_free: float, free_gb: float) -> str:

        if (
            percent_free <= STORAGE_EMERGENCY_PERCENT_FREE
            or free_gb <= STORAGE_EMERGENCY_FREE_GB
        ):
            return "emergency"

        if (
            percent_free <= STORAGE_CRITICAL_PERCENT_FREE
            or free_gb <= STORAGE_CRITICAL_FREE_GB
        ):
            return "critical"

        if (
            percent_free <= STORAGE_WARNING_PERCENT_FREE
            or free_gb <= STORAGE_WARNING_FREE_GB
        ):
            return "warning"

        return "normal"

    def _storage_message(
        self,
        label: str,
        level: str,
        total_gb: float,
        free_gb: float,
        percent_free: float,
        libraries: list[str],
    ) -> str:

        if level == "normal":
            return ""

        library_text = " / ".join(libraries)
        total_text = self._format_size(total_gb)
        free_text = self._format_size(free_gb)

        if level == "warning":
            return (
                f"STORAGE WARNING\n"
                f"{library_text} storage is running low.\n"
                f"Free Space: {free_text}\n"
                f"Total Capacity: {total_text}\n"
                f"Free: {percent_free:.0f}%\n"
                f"Recommendation:\n"
                f"Plan storage expansion."
            )

        if level == "critical":
            return (
                f"STORAGE CRITICAL\n"
                f"{label} is critically low.\n"
                f"Free Space: {free_text}\n"
                f"Total Capacity: {total_text}\n"
                f"Free: {percent_free:.0f}%\n"
                f"A storage upgrade is recommended soon."
            )

        if level == "emergency":
            return (
                f"STORAGE EMERGENCY\n"
                f"{label} has very little free space remaining.\n"
                f"Free Space: {free_text}\n"
                f"Free: {percent_free:.0f}%\n"
                f"Additional downloads or media imports may fail."
            )

        return ""

    @staticmethod
    def _format_size(size_gb: float) -> str:

        if size_gb >= 1024:
            return f"{size_gb / 1024:.2f} TB"

        return f"{size_gb:.0f} GB"

    def check_path_available(self, path: str) -> tuple[bool, str]:
        """
        Detect whether a configured media path is accessible.

        An empty library folder is still considered available if the path
        exists, is a directory, and can be read/stat'd.
        """

        try:
            if not os.path.exists(path):
                return False, "Configured media path is missing"

            if not os.path.isdir(path):
                return False, "Configured media path is not a directory"

            if not os.access(path, os.R_OK):
                return False, "Configured media path is inaccessible"

            # Confirm the filesystem can be queried.
            os.stat(path)
            psutil.disk_usage(path)
            return True, "Storage accessible"

        except (OSError, PermissionError) as error:
            return False, f"Storage filesystem unavailable ({error.__class__.__name__})"
        except Exception:
            return False, "Storage filesystem unavailable"

    def check_storage(self) -> list[StorageStatus]:

        results: list[StorageStatus] = []

        for volume in STORAGE_VOLUMES:
            path = volume["path"]
            available, detail = self.check_path_available(path)

            if not available:
                results.append(
                    StorageStatus(
                        volume_id=volume["id"],
                        label=volume["label"],
                        path=path,
                        libraries=list(volume["libraries"]),
                        level="unavailable",
                        available=False,
                        detail=detail,
                        message=(
                            f"STORAGE UNAVAILABLE\n"
                            f"{volume['label']} is unavailable.\n"
                            f"{detail}."
                        ),
                    )
                )
                continue

            try:
                usage = psutil.disk_usage(path)
                total_gb = usage.total / (1024 ** 3)
                used_gb = usage.used / (1024 ** 3)
                free_gb = usage.free / (1024 ** 3)
                percent_used = usage.percent
                percent_free = max(0.0, 100.0 - percent_used)

                level = self._storage_level(percent_free, free_gb)
                message = self._storage_message(
                    volume["label"],
                    level,
                    total_gb,
                    free_gb,
                    percent_free,
                    list(volume["libraries"]),
                )

                results.append(
                    StorageStatus(
                        volume_id=volume["id"],
                        label=volume["label"],
                        path=path,
                        libraries=list(volume["libraries"]),
                        total_gb=round(total_gb, 1),
                        used_gb=round(used_gb, 1),
                        free_gb=round(free_gb, 1),
                        percent_used=round(percent_used, 1),
                        percent_free=round(percent_free, 1),
                        level=level,
                        available=True,
                        detail=detail,
                        message=message,
                    )
                )

            except Exception:
                results.append(
                    StorageStatus(
                        volume_id=volume["id"],
                        label=volume["label"],
                        path=path,
                        libraries=list(volume["libraries"]),
                        level="unavailable",
                        available=False,
                        detail="Unable to read storage filesystem",
                        message=(
                            f"STORAGE UNAVAILABLE\n"
                            f"{volume['label']} is unavailable.\n"
                            f"Unable to read storage filesystem."
                        ),
                    )
                )

        return results

    def reset_failure_count(self, service_id: str):

        self._failure_counts[service_id] = 0
