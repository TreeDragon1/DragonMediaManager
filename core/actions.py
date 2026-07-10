"""
Dragon Media Manager
Dragon Actions

Version: v0.1.3-alpha
Build 6
"""

import webbrowser


class DragonActions:

    def open_jellyfin(self):
        webbrowser.open("http://localhost:8096")

    def open_radarr(self):
        webbrowser.open("http://localhost:7878")

    def open_sonarr(self):
        webbrowser.open("http://localhost:8989")

    def open_prowlarr(self):
        webbrowser.open("http://localhost:9696")

    def open_bazarr(self):
        webbrowser.open("http://localhost:6767")

    def open_jellyseerr(self):
        webbrowser.open("http://localhost:5055")

    def open_portainer(self):
        webbrowser.open("https://localhost:9443")
