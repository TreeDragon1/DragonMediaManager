"""
Dragon Media Manager
Dragon AI configuration — thresholds, services, and timing.
"""

from core.settings import (
    BAZARR_URL,
    JELLYFIN_URL,
    JELLYSEERR_URL,
    MOVIES_PATH,
    PROWLARR_URL,
    QBITTORRENT_URL,
    RADARR_URL,
    SONARR_URL,
    TV_PATH,
)

# Monitoring interval (seconds).
CHECK_INTERVAL_SECONDS = 30

# Consecutive failed checks before declaring a service unhealthy.
FAILURE_THRESHOLD = 2

# Immediate confirmation retries before automatic recovery.
CONFIRMATION_RETRIES = 1
CONFIRMATION_RETRY_DELAY_SECONDS = 5

# Wait after restart before verification (seconds).
STARTUP_WAIT_SECONDS = 25

# Maximum automatic recovery attempts per service before manual attention.
MAX_AUTO_RECOVERY_ATTEMPTS = 2

# Cooldown between automatic restart attempts for the same service.
RECOVERY_COOLDOWN_SECONDS = 900

# History rotation limit.
HISTORY_MAX_ENTRIES = 100

# Storage warning thresholds — percentage free.
# NORMAL:     > 20% free
# WARNING:    <= 20% free
# CRITICAL:   <= 10% free
# EMERGENCY:  <= 5% free
STORAGE_WARNING_PERCENT_FREE = 20.0
STORAGE_CRITICAL_PERCENT_FREE = 10.0
STORAGE_EMERGENCY_PERCENT_FREE = 5.0

# Secondary absolute free-space guards (GB) for large multi-TB volumes.
STORAGE_WARNING_FREE_GB = 500.0
STORAGE_CRITICAL_FREE_GB = 200.0
STORAGE_EMERGENCY_FREE_GB = 100.0

# Logical storage volumes mapped to configured library paths.
STORAGE_VOLUMES = [
    {
        "id": "movies",
        "label": "Movies Storage",
        "path": MOVIES_PATH,
        "libraries": ["Movies"],
    },
    {
        "id": "tv",
        "label": "TV Series Storage",
        "path": TV_PATH,
        "libraries": ["TV Shows", "Episodes"],
    },
]

# Monitored services (Portainer excluded from auto-recovery scope).
MONITORED_SERVICES = {
    "docker": {
        "label": "Docker",
        "container": None,
        "url": None,
        "health_path": None,
        "restart_method": None,
        "auto_recovery": False,
    },
    "jellyfin": {
        "label": "Jellyfin",
        "container": "jellyfin",
        "url": JELLYFIN_URL,
        "health_path": "/System/Info/Public",
        "restart_method": "restart_jellyfin",
        "auto_recovery": True,
    },
    "jellyseerr": {
        "label": "Jellyseerr",
        "container": "jellyseerr",
        "url": JELLYSEERR_URL,
        "health_path": "/api/v1/status",
        "restart_method": "restart_jellyseerr",
        "auto_recovery": True,
    },
    "sonarr": {
        "label": "Sonarr",
        "container": "sonarr",
        "url": SONARR_URL,
        "health_path": "/ping",
        "restart_method": "restart_sonarr",
        "auto_recovery": True,
    },
    "radarr": {
        "label": "Radarr",
        "container": "radarr",
        "url": RADARR_URL,
        "health_path": "/ping",
        "restart_method": "restart_radarr",
        "auto_recovery": True,
    },
    "prowlarr": {
        "label": "Prowlarr",
        "container": "prowlarr",
        "url": PROWLARR_URL,
        "health_path": "/ping",
        "restart_method": "restart_prowlarr",
        "auto_recovery": True,
    },
    "bazarr": {
        "label": "Bazarr",
        "container": "bazarr",
        "url": BAZARR_URL,
        "health_path": "/",
        "restart_method": "restart_bazarr",
        "auto_recovery": True,
    },
    "qbittorrent": {
        "label": "qBittorrent",
        "container": "qbittorrent",
        "url": QBITTORRENT_URL,
        "health_path": "/api/v2/app/version",
        "restart_method": "restart_qbittorrent",
        "auto_recovery": True,
        "use_qbittorrent_api": True,
    },
}
