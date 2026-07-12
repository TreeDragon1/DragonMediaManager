"""
Dragon Media Manager
Dragon Downloads Engine

Version: v0.1.3-alpha
Build 9.0.1

Connects to the qBittorrent Web API and returns
live download information.
"""

import requests

from core.settings import (
    QBITTORRENT_URL,
    QBITTORRENT_USERNAME,
    QBITTORRENT_PASSWORD,
)


class DragonDownloads:

    def __init__(self):
        self.session = requests.Session()
        self.connected = False

    # -----------------------------------------
    # Login
    # -----------------------------------------

    def login(self):

        try:

            response = self.session.post(
                f"{QBITTORRENT_URL}/api/v2/auth/login",
                data={
                    "username": QBITTORRENT_USERNAME,
                    "password": QBITTORRENT_PASSWORD,
                },
                timeout=5,
            )

            if response.status_code == 200 and response.text == "Ok.":
                self.connected = True
                return True

        except requests.RequestException:
            pass

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

        self.connected = False

    # -----------------------------------------
    # Downloads
    # -----------------------------------------

    def get_downloads(self):

        if not self.login():

            return {
                "connected": False,
                "active": 0,
                "downloads": [],
                "error": "Unable to connect to qBittorrent",
            }

        try:

            response = self.session.get(
                f"{QBITTORRENT_URL}/api/v2/torrents/info",
                timeout=5,
            )

            torrents = response.json()

            downloads = []

            for torrent in torrents:

                downloads.append(
                    {
                        "name": torrent.get("name"),
                        "progress": round(
                            torrent.get("progress", 0) * 100,
                            1,
                        ),
                        "state": torrent.get("state"),
                        "speed": torrent.get("dlspeed"),
                        "upload_speed": torrent.get("upspeed"),
                        "eta": torrent.get("eta"),
                        "size": torrent.get("size"),
                    }
                )

            self.logout()

            return {
                "connected": True,
                "active": len(downloads),
                "downloads": downloads,
            }

        except Exception as e:

            self.logout()

            return {
                "connected": False,
                "active": 0,
                "downloads": [],
                "error": str(e),
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