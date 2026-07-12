"""
Dragon Media Manager
Dragon Health Core

Version: v0.1.3-alpha
Build 8.5.2
"""

import subprocess
import shutil

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

    def get_health(self):
        services = self.check_services()
        score = self.calculate_score(services)
        return {
            "services": services,
            "movies": self.check_movies_drive(),
            "memory": self.check_memory(),
            "status": self.overall_status(score),
            "score": score,
            "docker": services["🐳 Docker"],
            "jellyfin": services["🎬 Jellyfin"],
        }

    def docker_ps(self):
        try:
            r = subprocess.run(["docker","ps"], capture_output=True, text=True)
            return r.stdout.lower() if r.returncode == 0 else ""
        except Exception:
            return ""

    def qbittorrent_running(self):
        try:
            r = subprocess.run(["pgrep","-f","qbittorrent"], capture_output=True, text=True)
            return r.returncode == 0
        except Exception:
            return False

    def check_services(self):
        ps = self.docker_ps()
        result = {"🐳 Docker": "🟢 Running" if ps != "" else "🔴 Offline"}

        for label, container in SERVICES.items():
            if label == "🐳 Docker":
                continue
            if label == "⬇️ qBittorrent":
                result[label] = "🟢 Online" if self.qbittorrent_running() else "🔴 Offline"
            else:
                result[label] = "🟢 Online" if container in ps else "🔴 Offline"
        return result

    def check_movies_drive(self):
        try:
            _,_,free = shutil.disk_usage("/media/treedragon/Movies1")
            return f"{free/(1024**4):.1f} TB Free"
        except Exception:
            return "--"

    def check_memory(self):
        try:
            r = subprocess.run(["free","-h"], capture_output=True, text=True)
            for line in r.stdout.splitlines():
                if line.startswith("Mem:"):
                    return f"{line.split()[6]} Available"
        except Exception:
            pass
        return "--"

    def calculate_score(self, services):
        total = len(services)
        online = sum(1 for s in services.values() if "🟢" in s)
        return round((online/total)*100)

    def overall_status(self, score):
        if score >= 90:
            return "🟢 Excellent"
        if score >= 70:
            return "🟡 Good"
        return "🔴 Needs Attention"
