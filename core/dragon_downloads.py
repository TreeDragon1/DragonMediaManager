"""
Dragon Media Manager
Dragon Downloads Engine

Version: v0.1.3-alpha
Build 9.0.1

Connects to the qBittorrent Web API and returns
live download information.
"""

import time

import requests

from core.settings import (
    QBITTORRENT_URL,
    QBITTORRENT_USERNAME,
    QBITTORRENT_PASSWORD,
)


class DragonDownloads:

    AUTH_BACKOFF_SECONDS = 300
    ACTIVE_STATES = {
        "downloading",
        "forcedDL",
        "metaDL",
        "stalledDL",
    }

    def __init__(self):
        self.session = requests.Session()
        self.session.trust_env = False
        self.connected = False
        self.last_error = ""
        self._logged_in = False
        self._auth_blocked_until = 0.0

    # -----------------------------------------
    # Login
    # -----------------------------------------

    def _auth_backoff_active(self):

        return time.time() < self._auth_blocked_until

    def _set_auth_failure(self, message):

        self._logged_in = False
        self.connected = False
        self.last_error = message
        self._auth_blocked_until = time.time() + self.AUTH_BACKOFF_SECONDS

    def _session_alive(self):

        try:
            response = self.session.get(
                f"{QBITTORRENT_URL}/api/v2/app/version",
                timeout=5,
            )

            if response.status_code == 200:
                self.connected = True
                self.last_error = ""
                return True

            if response.status_code == 403:
                self._set_auth_failure(
                    "Session expired (403): Unauthorized"
                )
                return False

            if response.status_code == 401:
                self._set_auth_failure(
                    "Session expired (401): Unauthorized"
                )
                return False

        except requests.RequestException as error:
            self.last_error = f"Connection failed: {error}"

        self._logged_in = False
        self.connected = False
        return False

    def login(self):

        if self._auth_backoff_active():
            return False

        if not QBITTORRENT_PASSWORD:
            self._set_auth_failure(
                "QBITTORRENT_PASSWORD is not configured "
                "(set env var or config/qbittorrent.env)"
            )
            return False

        if self._logged_in and self._session_alive():
            return True

        try:

            response = self.session.post(
                f"{QBITTORRENT_URL}/api/v2/auth/login",
                data={
                    "username": QBITTORRENT_USERNAME,
                    "password": QBITTORRENT_PASSWORD,
                },
                timeout=5,
            )

            # qBittorrent <= 5.1 returns HTTP 200 with body "Ok."
            # qBittorrent 5.2+ returns HTTP 204 No Content on success.
            body = response.text.strip()
            login_ok = (
                response.status_code == 204
                or (
                    response.status_code == 200
                    and (body == "Ok." or body == "")
                )
            )

            if login_ok:
                self._logged_in = True
                self.connected = True
                self.last_error = ""
                self._auth_blocked_until = 0.0
                return True

            if response.status_code in (401, 403) or body == "Fails.":
                self._set_auth_failure(
                    f"Login failed ({response.status_code}): "
                    f"{body or 'Unauthorized'}"
                )
                return False

            self.last_error = (
                f"Login failed ({response.status_code}): "
                f"{body or 'empty response'}"
            )

        except requests.RequestException as error:
            self.last_error = f"Connection failed: {error}"

        self._logged_in = False
        self.connected = False
        return False

    # -----------------------------------------
    # Logout
    # -----------------------------------------

    def logout(self):

        try:
            self.session.get(
                f"{QBITTORRENT_URL}/api/v2/auth/logout",
                timeout=5,
            )
        except requests.RequestException:
            pass

        self._logged_in = False
        self.connected = False

    # -----------------------------------------
    # Downloads
    # -----------------------------------------

    def get_downloads(self):

        if self._auth_backoff_active():
            return {
                "connected": False,
                "active": 0,
                "downloads": [],
                "error": self.last_error or "qBittorrent authentication paused",
                "auth_failure": True,
            }

        if not self.login():

            auth_failure = (
                "401" in self.last_error
                or "403" in self.last_error
                or "Unauthorized" in self.last_error
                or "not configured" in self.last_error
            )

            return {
                "connected": False,
                "active": 0,
                "downloads": [],
                "error": self.last_error or "Unable to connect to qBittorrent",
                "auth_failure": auth_failure,
            }

        try:

            response = self.session.get(
                f"{QBITTORRENT_URL}/api/v2/torrents/info",
                timeout=5,
            )

            if response.status_code in (401, 403):
                self._set_auth_failure(
                    f"API access denied ({response.status_code}): "
                    f"{response.text.strip() or 'Unauthorized'}"
                )

                return {
                    "connected": False,
                    "active": 0,
                    "downloads": [],
                    "error": self.last_error,
                    "auth_failure": True,
                }

            response.raise_for_status()
            torrents = response.json()

            active = []

            for torrent in torrents:

                state = torrent.get("state")

                if state not in self.ACTIVE_STATES:
                    continue

                active.append(
                    {
                        "name": torrent.get("name"),
                        "progress": round(
                            torrent.get("progress", 0) * 100,
                            1,
                        ),
                        "state": state,
                        "speed": torrent.get("dlspeed"),
                        "upload_speed": torrent.get("upspeed"),
                        "eta": torrent.get("eta"),
                        "size": torrent.get("size"),
                    }
                )

            return {
                "connected": True,
                "active": len(active),
                "downloads": active,
                "error": "",
                "auth_failure": False,
            }

        except Exception as error:

            self.last_error = str(error)
            self._logged_in = False
            self.connected = False

            return {
                "connected": False,
                "active": 0,
                "downloads": [],
                "error": str(error),
                "auth_failure": False,
            }

    # -----------------------------------------
    # Statistics
    # -----------------------------------------

    def get_statistics(self):

        data = self.get_downloads()

        if not data["connected"]:
            return data

        total_download_speed = sum(
            item["speed"]
            for item in data["downloads"]
        )

        total_upload_speed = sum(
            item["upload_speed"]
            for item in data["downloads"]
        )

        data["download_speed"] = total_download_speed
        data["upload_speed"] = total_upload_speed

        return data
