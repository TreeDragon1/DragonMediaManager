"""
Dragon Media Manager
Dragon AI Core

Version: v0.1.3-alpha
Build 5.5
"""

from core.dragon_health import DragonHealthCore


class DragonAI:

    def get_message(self):

        health = DragonHealthCore().get_health()

        return f"""Good day Peter.

Docker: {health['docker']}
Jellyfin: {health['jellyfin']}
Movies Drive: {health['movies']}
Memory: {health['memory']}

Dragon Health Score: {health['score']}%

Everything looks healthy.

Have a great day, Founder.
"""
