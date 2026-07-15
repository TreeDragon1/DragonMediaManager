"""
Dragon Media Centre
Settings

Version: v1.2.0
Build: 001

Central Configuration
"""

# ==========================================================
# SERVER CONFIGURATION
# ==========================================================

SERVER_IP = "192.168.1.126"

LOCALHOST = "127.0.0.1"

USE_LAN = True

HOST = SERVER_IP if USE_LAN else LOCALHOST

# ==========================================================
# PORTS
# ==========================================================

JELLYFIN_PORT = 8096
RADARR_PORT = 7878
SONARR_PORT = 8989
PROWLARR_PORT = 9696
BAZARR_PORT = 6767
JELLYSEERR_PORT = 5055
QBITTORRENT_PORT = 8080
PORTAINER_PORT = 9443

# ==========================================================
# WEB URLS
# ==========================================================

JELLYFIN_URL = f"http://{HOST}:{JELLYFIN_PORT}"
RADARR_URL = f"http://{HOST}:{RADARR_PORT}"
SONARR_URL = f"http://{HOST}:{SONARR_PORT}"
PROWLARR_URL = f"http://{HOST}:{PROWLARR_PORT}"
BAZARR_URL = f"http://{HOST}:{BAZARR_PORT}"
JELLYSEERR_URL = f"http://{HOST}:{JELLYSEERR_PORT}"
QBITTORRENT_URL = f"http://{HOST}:{QBITTORRENT_PORT}"
PORTAINER_URL = f"https://{HOST}:{PORTAINER_PORT}"

# ==========================================================
# LOGIN
# ==========================================================

QBITTORRENT_USERNAME = "admin"
QBITTORRENT_PASSWORD = ""

# ==========================================================
# LIBRARY PATHS
# ==========================================================

MOVIES_PATH = "/media/treedragon/Movies1"
TV_PATH = "/media/treedragon/TV Series1"
DOWNLOADS_PATH = "/media/treedragon/download1"

# ==========================================================
# DRAGON MEDIA CENTRE
# ==========================================================

BACKUP_SCRIPT = (
    "/media/treedragon/Steam Gam/"
    "Dragon Media Centre/Scripts/"
    "dragon-backup.sh"
)

BACKUP_FOLDER = (
    "/media/treedragon/Steam Gam/"
    "Dragon Media Centre/Backups"
)

LOG_FOLDER = (
    "/media/treedragon/Steam Gam/"
    "Dragon Media Centre/Logs"
)

# ==========================================================
# DASHBOARD
# ==========================================================

REFRESH_INTERVAL = 30

WINDOW_WIDTH = 1550
WINDOW_HEIGHT = 980

THEME = "dark"

# ==========================================================
# BUILD INFO
# ==========================================================

APP_NAME = "🐉 Dragon Media Centre"

VERSION = "1.2.0"

BUILD = "001"