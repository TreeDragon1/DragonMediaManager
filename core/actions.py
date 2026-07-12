"""
Dragon Media Manager
Dragon Actions

Version: v0.1.3-alpha
Build 8.5
"""

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
)


class DragonActions:

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
