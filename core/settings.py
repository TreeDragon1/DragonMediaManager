"""
Dragon Media Manager
Settings

Version: v0.1.3-alpha
Build 9.0

Central configuration for Dragon Media Manager.
"""

# ==========================================
# Server
# ==========================================

SERVER_HOST = "127.0.0.1"
SERVER_LAN = "192.168.1.126"

# ==========================================
# Media Services
# ==========================================

JELLYFIN_URL = f"http://{SERVER_HOST}:8096"
RADARR_URL = f"http://{SERVER_HOST}:7878"
SONARR_URL = f"http://{SERVER_HOST}:8989"
PROWLARR_URL = f"http://{SERVER_HOST}:9696"
BAZARR_URL = f"http://{SERVER_HOST}:6767"
JELLYSEERR_URL = f"http://{SERVER_HOST}:5055"
QBITTORRENT_URL = f"http://{SERVER_HOST}:8080"
PORTAINER_URL = f"https://{SERVER_HOST}:9443"

# ==========================================
# qBittorrent Web API
# ==========================================

QBITTORRENT_USERNAME = "admin"
QBITTORRENT_PASSWORD = ""

# ==========================================
# Library Paths
# ==========================================

MOVIES_PATH = "/media/treedragon/Movies1"
TV_PATH = "/media/treedragon/TV Series"
DOWNLOADS_PATH = "/media/treedragon/download"

# ==========================================
# Dashboard
# ==========================================

REFRESH_INTERVAL = 30
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 1000
THEME = "dark"
