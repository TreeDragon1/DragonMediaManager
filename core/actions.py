"""
Dragon Media Centre
Dragon Actions

Version: 1.2.0
Build: 002
"""

import subprocess
import webbrowser

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