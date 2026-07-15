"""
Dragon Media Manager
Dragon AI Core

Version: v0.1.3-alpha
Build 9.1
"""

from core.dragon_health import DragonHealthCore


class DragonAI:

    def __init__(self):
        self.health = DragonHealthCore().get_health()

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    def _service(self, name):
        return self.health.get("services", {}).get(name, "Unknown")

    # --------------------------------------------------
    # AI Message
    # --------------------------------------------------

    def get_message(self):

        health = self.health

        cpu = health.get("cpu", {}).get("percent", "--")

        memory = health.get("memory", {})
        memory_percent = memory.get("percent", "--")
        memory_available = memory.get("available_gb", "--")
        memory_total = memory.get("total_gb", "--")

        disk = health.get("disk", {})
        disk_percent = disk.get("percent", "--")
        disk_free = disk.get("free_tb", "--")
        disk_total = disk.get("total_tb", "--")

        score = health.get("score", 0)
        status = health.get("status", "Unknown")

        hostname = health.get("hostname", "--")
        updated = health.get("last_updated", "--")

        return f"""
Good day Peter.

🐉 Dragon Media Manager Build 9.1

Host: {hostname}
Updated: {updated}

══════════════════════════════

System Health

CPU Usage: {cpu}%

Memory:
  {memory_available} GB Available
  {memory_percent}% Used
  {memory_total} GB Installed

Movies Drive:
  {disk_free} TB Free
  {disk_percent}% Used
  {disk_total} TB Total

══════════════════════════════

Service Status

Docker ............. {self._service("🐳 Docker")}
Jellyfin ........... {self._service("🎬 Jellyfin")}
Radarr ............. {self._service("🎞️ Radarr")}
Sonarr ............. {self._service("📺 Sonarr")}
Prowlarr ........... {self._service("🔍 Prowlarr")}
Bazarr ............. {self._service("💬 Bazarr")}
Jellyseerr ......... {self._service("🎬 Jellyseerr")}
qBittorrent ........ {self._service("⬇️ qBittorrent")}
Portainer .......... {self._service("🐳 Portainer")}

══════════════════════════════

Dragon Score : {score}%
Overall Status : {status}

Dragon AI Assessment

The system health report has been generated successfully.

Continue monitoring system resources, Docker services,
downloads and media storage to maintain optimal
performance.

Have a great day, Founder.
"""