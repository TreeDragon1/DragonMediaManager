"""
Dragon Media Manager
Dragon Health Core

Version: v0.1.3-alpha
Build 4
"""

import subprocess
import shutil


class DragonHealthCore:

    def get_health(self):

        return {
            "docker": self.check_docker(),
            "jellyfin": self.check_jellyfin(),
            "movies": self.check_movies_drive(),
            "memory": self.check_memory(),
            "score": self.calculate_score()
        }

    # -----------------------------------------

    def check_docker(self):

        try:

            result = subprocess.run(
                ["docker", "ps"],
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                return "🟢 Running"

            return "🔴 Offline"

        except Exception:
            return "🔴 Error"

    # -----------------------------------------

    def check_jellyfin(self):

        try:

            result = subprocess.run(
                ["docker", "ps"],
                capture_output=True,
                text=True
            )

            if "jellyfin" in result.stdout.lower():
                return "🟢 Online"

            return "🔴 Offline"

        except Exception:
            return "🔴 Error"

    # -----------------------------------------

    def check_movies_drive(self):

        total, used, free = shutil.disk_usage(
            "/media/treedragon/Movies1"
        )

        free_tb = free / (1024 ** 4)

        return f"{free_tb:.1f} TB Free"

    # -----------------------------------------

    def check_memory(self):

        try:

            result = subprocess.run(
                ["free", "-h"],
                capture_output=True,
                text=True
            )

            for line in result.stdout.splitlines():

                if line.startswith("Mem:"):

                    parts = line.split()

                    return f"{parts[6]} Available"

        except Exception:
            pass

        return "--"

    # -----------------------------------------

    def calculate_score(self):

        return 99