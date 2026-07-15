"""
Dragon Media Manager
Dragon Health Core

Version: v0.1.3-alpha
Build 9.1
"""

import socket
import subprocess
from datetime import datetime

import psutil

from core.settings import MOVIES_PATH

SERVICES = {
    "🐳 Docker": "docker",
    "🎬 Jellyfin": "jellyfin",
    "🎞️ Radarr": "radarr",
    "📺 Sonarr": "sonarr",
    "🔍 Prowlarr": "prowlarr",
    "💬 Bazarr": "bazarr",
    "🎬 Jellyseerr": "jellyseerr",
    "⬇️ qBittorrent": "qbittorrent",
    "🐳 Portainer": "portainer",
}


class DragonHealthCore:

    # --------------------------------------------------
    # System Information
    # --------------------------------------------------

    def get_cpu_usage(self) -> float:
        """Return current CPU usage."""
        return round(psutil.cpu_percent(interval=0.2), 1)

    def get_memory_usage(self) -> dict:
        """Return memory information."""
        memory = psutil.virtual_memory()

        return {
            "percent": round(memory.percent, 1),
            "available_gb": round(memory.available / (1024 ** 3), 1),
            "total_gb": round(memory.total / (1024 ** 3), 1),
        }

    def get_disk_usage(self) -> dict:
        """Return movie drive disk usage."""
        disk = psutil.disk_usage(MOVIES_PATH)

        return {
            "percent": round(disk.percent, 1),
            "free_tb": round(disk.free / (1024 ** 4), 2),
            "total_tb": round(disk.total / (1024 ** 4), 2),
        }

    def get_hostname(self) -> str:
        return socket.gethostname()

    def get_last_updated(self) -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # --------------------------------------------------
    # Docker / Services
    # --------------------------------------------------

    def docker_ps(self) -> str:
        try:
            result = subprocess.run(
                ["docker", "ps"],
                capture_output=True,
                text=True,
            )

            if result.returncode == 0:
                return result.stdout.lower()

        except Exception:
            pass

        return ""

    def qbittorrent_running(self) -> bool:
        try:
            result = subprocess.run(
                ["pgrep", "-f", "qbittorrent"],
                capture_output=True,
                text=True,
            )

            return result.returncode == 0

        except Exception:
            return False

    def check_services(self):

        docker = self.docker_ps()

        results = {
            "🐳 Docker": "🟢 Running" if docker else "🔴 Offline"
        }

        for label, container in SERVICES.items():

            if label == "🐳 Docker":
                continue

            if label == "⬇️ qBittorrent":
                results[label] = (
                    "🟢 Online"
                    if self.qbittorrent_running()
                    else "🔴 Offline"
                )
            else:
                results[label] = (
                    "🟢 Online"
                    if container in docker
                    else "🔴 Offline"
                )

        return results

    # --------------------------------------------------
    # Legacy Compatibility
    # --------------------------------------------------

    def check_movies_drive(self):

        try:
            disk = self.get_disk_usage()
            return f"{disk['free_tb']} TB Free"

        except Exception:
            return "--"

    def check_memory(self):

        try:
            memory = self.get_memory_usage()
            return f"{memory['available_gb']} GB Available"

        except Exception:
            return "--"

    # --------------------------------------------------
    # Dragon Score
    # --------------------------------------------------

    def calculate_score(self, services):

        total = len(services)

        online = sum(
            1
            for status in services.values()
            if "🟢" in status
        )

        return round((online / total) * 100)

    def overall_status(self, score):

        if score >= 90:
            return "🟢 Excellent"

        if score >= 70:
            return "🟡 Good"

        return "🔴 Needs Attention"

    # --------------------------------------------------
    # Main Health Report
    # --------------------------------------------------

    def get_health(self):

        services = self.check_services()

        score = self.calculate_score(services)

        cpu = self.get_cpu_usage()
        memory = self.get_memory_usage()
        disk = self.get_disk_usage()

        return {

            # -------- New Build 9.1 --------

            "cpu": {
                "percent": cpu,
            },

            "memory": {
                "percent": memory["percent"],
                "available_gb": memory["available_gb"],
                "total_gb": memory["total_gb"],
            },

            "disk": {
                "percent": disk["percent"],
                "free_tb": disk["free_tb"],
                "total_tb": disk["total_tb"],
            },

            "hostname": self.get_hostname(),

            "last_updated": self.get_last_updated(),

            "services": services,

            "score": score,

            "status": self.overall_status(score),

            # -------- Compatibility --------

            "movies": f"{disk['free_tb']} TB Free",

            "memory_text": (
                f"{memory['available_gb']} GB Available"
            ),

            "docker": services["🐳 Docker"],

            "jellyfin": services["🎬 Jellyfin"],
        }