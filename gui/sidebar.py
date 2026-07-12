"""
Dragon Media Manager
Sidebar

Version: v0.1.3-alpha
Build 8.5
Codename: Dragon Control
"""

import customtkinter as ctk

from core.version import APP_NAME, VERSION, BUILD
from core.actions import DragonActions


class Sidebar(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master, width=220)

        self.actions = DragonActions()

        self.configure(fg_color="#202225")
        self.pack_propagate(False)

        ctk.CTkLabel(
            self,
            text="🐉",
            font=("Arial", 42)
        ).pack(pady=(15, 0))

        ctk.CTkLabel(
            self,
            text=APP_NAME.replace(" ", "\n", 1),
            font=("Arial", 20, "bold"),
            justify="center"
        ).pack(pady=(0, 15))

        self.make_section("Navigation")

        self.make_button("🏠 Dashboard")
        self.make_button("🎬 Movies")
        self.make_button("📺 TV Shows")
        self.make_button("⚙️ Settings")

        self.make_section("🚀 Quick Launch")

        launches = [
            ("🎬 Jellyfin", self.actions.open_jellyfin),
            ("🎞️ Radarr", self.actions.open_radarr),
            ("📺 Sonarr", self.actions.open_sonarr),
            ("🔍 Prowlarr", self.actions.open_prowlarr),
            ("💬 Bazarr", self.actions.open_bazarr),
            ("🎟️ Jellyseerr", self.actions.open_jellyseerr),
            ("⬇️ qBittorrent", self.actions.open_qbittorrent),
            ("🐳 Portainer", self.actions.open_portainer),
        ]

        for text, cmd in launches:
            self.make_button(text, cmd)

        ctk.CTkLabel(
            self,
            text=f"{VERSION}\nBuild {BUILD}",
            font=("Arial", 11),
            justify="center"
        ).pack(side="bottom", pady=15)

    def make_section(self, title):
        ctk.CTkLabel(
            self,
            text=title,
            font=("Arial", 14, "bold")
        ).pack(pady=(12, 6))

    def make_button(self, text, command=None):
        btn = ctk.CTkButton(
            self,
            text=text,
            width=180,
            height=34,
            command=command
        )
        btn.pack(padx=20, pady=3)
        return btn
