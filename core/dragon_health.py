"""
Dragon Media Manager
Dragon Health Core

Version: v0.1.3-alpha
Build 8.2.2
"""

import subprocess
import shutil

SERVICES={
    "🐳 Docker":"docker",
    "🎬 Jellyfin":"jellyfin",
    "🎞️ Radarr":"radarr",
    "📺 Sonarr":"sonarr",
    "🔍 Prowlarr":"prowlarr",
    "💬 Bazarr":"bazarr",
    "🎬 Jellyseerr":"jellyseerr",
    "🐳 Portainer":"portainer",
}

class DragonHealthCore:

    def get_health(self):
        services=self.check_services()
        score=self.calculate_score(services)
        return {
            "services":services,
            "movies":self.check_movies_drive(),
            "memory":self.check_memory(),
            "status":self.overall_status(score),
            "score":score,
            # backward compatibility
            "docker":services["🐳 Docker"],
            "jellyfin":services["🎬 Jellyfin"],
        }

    def docker_ps(self):
        try:
            r=subprocess.run(["docker","ps"],capture_output=True,text=True)
            if r.returncode!=0:
                return None
            return r.stdout.lower()
        except Exception:
            return None

    def check_services(self):
        ps=self.docker_ps()
        result={}
        if ps is None:
            for name in SERVICES:
                result[name]="🔴 Offline"
            return result
        result["🐳 Docker"]="🟢 Running"
        for label,container in list(SERVICES.items())[1:]:
            result[label]="🟢 Online" if container in ps else "🔴 Offline"
        return result

    def check_movies_drive(self):
        try:
            _,_,free=shutil.disk_usage("/media/treedragon/Movies1")
            return f"{free/(1024**4):.1f} TB Free"
        except Exception:
            return "--"

    def check_memory(self):
        try:
            r=subprocess.run(["free","-h"],capture_output=True,text=True)
            for line in r.stdout.splitlines():
                if line.startswith("Mem:"):
                    return f"{line.split()[6]} Available"
        except Exception:
            pass
        return "--"

    def calculate_score(self,services):
        total=len(services)
        online=sum(1 for v in services.values() if "🟢" in v)
        return round((online/total)*100)

    def overall_status(self,score):
        if score>=90:
            return "🟢 Excellent"
        if score>=70:
            return "🟡 Good"
        return "🔴 Needs Attention"
