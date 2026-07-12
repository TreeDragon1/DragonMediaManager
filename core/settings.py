"""
Dragon Media Manager
Settings

Version: v0.1.3-alpha
Build 8.4

Central configuration for Dragon Media Manager.
"""

# ==========================================
# Media Services
# ==========================================

JELLYFIN_URL = "http://localhost:8096"
RADARR_URL = "http://localhost:7878"
SONARR_URL = "http://localhost:8989"
PROWLARR_URL = "http://localhost:9696"
BAZARR_URL = "http://localhost:6767"
JELLYSEERR_URL = "http://localhost:5055"
QBITTORRENT_URL = "http://localhost:8080"
PORTAINER_URL = "https://localhost:9443"

# ==========================================
# Library Paths
# ==========================================

MOVIES_PATH = "/media/treedragon/Movies1"
TV_PATH = "/media/treedragon/TV Series"
DOWNLOADS_PATH = "/media/treedragon/download"

# ==========================================
# Dashboard
# ==========================================

REFRESH_INTERVAL = 30  # seconds
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 1000
THEME = "dark"
