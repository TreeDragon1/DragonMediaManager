"""
Dragon Media Manager
Dragon Command Center

Version: v0.1.3-alpha
Build 6
"""

import customtkinter as ctk
from core.actions import DragonActions


class DragonActionsFrame(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.actions = DragonActions()

        self.configure(corner_radius=12)

        title = ctk.CTkLabel(
            self,
            text="🐉 Dragon Command Center",
            font=("Arial", 22, "bold")
        )

        title.pack(anchor="w", padx=20, pady=(15, 15))

        self.add_button("🎬 Launch Jellyfin", self.actions.open_jellyfin)
        self.add_button("🎥 Launch Radarr", self.actions.open_radarr)
        self.add_button("📺 Launch Sonarr", self.actions.open_sonarr)
        self.add_button("🔍 Launch Prowlarr", self.actions.open_prowlarr)
        self.add_button("💬 Launch Bazarr", self.actions.open_bazarr)
        self.add_button("📦 Launch Portainer", self.actions.open_portainer)

    def add_button(self, text, command):

        button = ctk.CTkButton(
            self,
            text=text,
            command=command,
            height=40
        )

        button.pack(
            fill="x",
            padx=20,
            pady=5
        )
