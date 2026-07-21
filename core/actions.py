"""
Dragon Media Centre
Dragon Actions

Version: 1.2.0
Build: 002
"""

import subprocess
import time
import webbrowser
from pathlib import Path

from core.settings import (
    JELLYFIN_URL,
    RADARR_URL,
    SONARR_URL,
    PROWLARR_URL,
    BAZARR_URL,
    JELLYSEERR_URL,
    QBITTORRENT_URL,
    PORTAINER_URL,
    BACKUP_SCRIPT,
    BACKUP_FOLDER,
)


class DragonActions:

    # =====================================================
    # Internal helper
    # =====================================================

    def _run(self, command):
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                return True, "Success"

            return False, result.stderr.strip()

        except Exception as e:
            return False, str(e)

    # =====================================================
    # Open Web Interfaces
    # =====================================================

    def open_jellyfin(self):
        webbrowser.open(JELLYFIN_URL)

    def open_radarr(self):
        webbrowser.open(RADARR_URL)

    def open_sonarr(self):
        webbrowser.open(SONARR_URL)

    def open_prowlarr(self):
        webbrowser.open(PROWLARR_URL)

    def open_bazarr(self):
        webbrowser.open(BAZARR_URL)

    def open_jellyseerr(self):
        webbrowser.open(JELLYSEERR_URL)

    def open_qbittorrent(self):
        webbrowser.open(QBITTORRENT_URL)

    def open_portainer(self):
        webbrowser.open(PORTAINER_URL)

    # =====================================================
    # Backup
    # =====================================================

    def backup_now(self):
        return self._run(f'"{BACKUP_SCRIPT}"')

    @staticmethod
    def get_last_backup_label():
        """
        Return a relative time label for the newest backup file,
        or "N/A" when no backup data is available.
        """

        try:
            folder = Path(BACKUP_FOLDER)

            if not folder.exists() or not folder.is_dir():
                return "N/A"

            backups = [
                path
                for path in folder.iterdir()
                if path.is_file()
            ]

            if not backups:
                return "N/A"

            latest = max(
                backups,
                key=lambda path: path.stat().st_mtime
            )

            age_seconds = max(
                0,
                int(time.time() - latest.stat().st_mtime)
            )

            if age_seconds < 60:
                return "Just now"

            if age_seconds < 3600:
                minutes = age_seconds // 60
                return f"{minutes}m ago"

            if age_seconds < 86400:
                hours = age_seconds // 3600
                return f"{hours}h ago"

            days = age_seconds // 86400
            return f"{days}d ago"

        except Exception:
            return "N/A"

    @staticmethod
    def get_last_backup_info():
        """
        Return basic information about the newest backup file, if available.
        """

        info = {
            "label": "N/A",
            "status": "Unknown",
            "filename": None,
            "modified": None,
            "folder": str(BACKUP_FOLDER),
        }

        try:
            folder = Path(BACKUP_FOLDER)
            info["folder"] = str(folder)

            if not folder.exists() or not folder.is_dir():
                info["status"] = "Backup folder not found"
                return info

            backups = [
                path
                for path in folder.iterdir()
                if path.is_file()
            ]

            if not backups:
                info["status"] = "No backups found"
                return info

            latest = max(
                backups,
                key=lambda path: path.stat().st_mtime
            )

            modified_ts = latest.stat().st_mtime
            modified = time.strftime(
                "%Y-%m-%d %H:%M:%S",
                time.localtime(modified_ts),
            )

            info["label"] = DragonActions.get_last_backup_label()
            info["status"] = "Available"
            info["filename"] = latest.name
            info["modified"] = modified
            return info

        except Exception:
            info["status"] = "Unable to read backup information"
            return info

    # =====================================================
    # Docker Restarts
    # =====================================================

    def restart_jellyfin(self):
        return self._run("docker restart jellyfin")

    def restart_sonarr(self):
        return self._run("docker restart sonarr")

    def restart_radarr(self):
        return self._run("docker restart radarr")

    def restart_prowlarr(self):
        return self._run("docker restart prowlarr")

    def restart_bazarr(self):
        return self._run("docker restart bazarr")

    def restart_qbittorrent(self):
        return self._run("docker restart qbittorrent")

    def restart_jellyseerr(self):
        return self._run("docker restart jellyseerr")

    def restart_media_stack(self):

        containers = [
            "jellyfin",
            "sonarr",
            "radarr",
            "prowlarr",
            "bazarr",
            "qbittorrent",
            "jellyseerr",
        ]

        for container in containers:

            success, message = self._run(
                f"docker restart {container}"
            )

            if not success:
                return False, f"{container}: {message}"

        return True, "Media Stack Restarted"