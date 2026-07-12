
"""
Dragon Media Manager
Dragon Command Center

Version: v0.1.3-alpha
Build 8.3
"""

import customtkinter as ctk
from core.actions import DragonActions

class DragonActionsFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.actions=DragonActions()
        self.configure(corner_radius=12)

        ctk.CTkLabel(self,text="🚀 Quick Launch",font=("Arial",22,"bold")).pack(anchor="w",padx=20,pady=(15,15))

        buttons=[
            ("🎬 Jellyfin",self.actions.open_jellyfin),
            ("🎞️ Radarr",self.actions.open_radarr),
            ("📺 Sonarr",self.actions.open_sonarr),
            ("🔍 Prowlarr",self.actions.open_prowlarr),
            ("💬 Bazarr",self.actions.open_bazarr),
            ("🎟️ Jellyseerr",self.actions.open_jellyseerr),
            ("⬇️ qBittorrent",self.actions.open_qbittorrent),
            ("🐳 Portainer",self.actions.open_portainer),
        ]

        for text,command in buttons:
            self.add_button(text,command)

    def add_button(self,text,command):
        ctk.CTkButton(
            self,
            text=text,
            command=command,
            height=42
        ).pack(fill="x",padx=20,pady=5)
