"""
Dragon Media Manager
Sidebar

Version: v0.1.3-alpha
Build 8
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

        # ==========================================
        # Logo
        # ==========================================

        logo = ctk.CTkLabel(
            self,
            text="🐉",
            font=("Arial", 46)
        )
        logo.pack(pady=(20, 5))

        # ==========================================
        # Title
        # ==========================================

        title = ctk.CTkLabel(
            self,
            text=APP_NAME.replace(" ", "\n", 1),
            font=("Arial", 20, "bold"),
            justify="center"
        )
        title.pack(pady=(0, 20))

        # ==========================================
        # Navigation
        # ==========================================

        self.make_button("🏠 Dashboard")

        self.make_button("🎬 Movies")

        self.make_button("📺 TV Shows")

        self.make_button("⚙ Settings")

        # ==========================================
        # Quick Launch
        # ==========================================

        quick = ctk.CTkLabel(
            self,
            text="Quick Launch",
            font=("Arial", 14, "bold")
        )
        quick.pack(pady=(25, 5))

        self.make_button(
            "🪼 Jellyfin",
            self.actions.open_jellyfin
        )

        self.make_button(
            "🎞 Radarr",
            self.actions.open_radarr
        )

        # ==========================================
        # Version
        # ==========================================

        version = ctk.CTkLabel(
            self,
            text=f"{VERSION}\nBuild {BUILD}",
            font=("Arial", 12),
            justify="center"
        )

        version.pack(side="bottom", pady=20)

    def make_button(self, text, command=None):

        button = ctk.CTkButton(
            self,
            text=text,
            width=180,
            height=40,
            command=command
        )

        button.pack(pady=6, padx=20)

        return button