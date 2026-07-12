"""
Dragon Media Manager
Build 9.0.3

Downloads Panel
"""

import customtkinter as ctk

from core.dragon_downloads import DragonDownloads


class DownloadsPanel(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            self,
            text="📥 Active Downloads",
            font=("Arial", 18, "bold"),
        )
        title.grid(
            row=0,
            column=0,
            sticky="w",
            padx=15,
            pady=(15, 10),
        )

        self.status = ctk.CTkLabel(
            self,
            text="✔ No Active Downloads",
            font=("Arial", 16),
        )
        self.status.grid(
            row=1,
            column=0,
            sticky="w",
            padx=20,
        )

        self.message = ctk.CTkLabel(
            self,
            text="Dragon is monitoring qBittorrent...",
            text_color="gray",
        )
        self.message.grid(
            row=2,
            column=0,
            sticky="w",
            padx=20,
            pady=(0, 10),
        )

        self.progress = ctk.CTkProgressBar(self)
        self.progress.grid(
            row=3,
            column=0,
            sticky="ew",
            padx=20,
            pady=(0, 15),
        )

        self.progress.set(0)

        # Downloads engine
        self.engine = DragonDownloads()

        # Start automatic refresh
        self.after(1000, self.refresh_downloads)

    def set_idle(self):
        self.status.configure(text="✔ No Active Downloads")
        self.message.configure(text="Dragon is monitoring qBittorrent...")
        self.progress.set(0)

    def refresh_downloads(self):

        data = self.engine.get_downloads()

        if not data["connected"]:
            self.status.configure(text="❌ qBittorrent Offline")
            self.message.configure(text="Unable to connect")
            self.progress.set(0)

        elif data["active"] == 0:
            self.set_idle()

        else:
            download = data["downloads"][0]

            progress = download["progress"]
            speed = download["speed"] // 1024
            eta = download["eta"]

            self.status.configure(text=download["name"])

            self.message.configure(
                text=f"{progress}% • {speed} KB/s • ETA {eta}s"
            )

            self.progress.set(progress / 100)

        self.after(5000, self.refresh_downloads)