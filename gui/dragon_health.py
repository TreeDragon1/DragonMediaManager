"""
Dragon Media Manager
Dragon Health Panel

Version: v0.1.3-alpha
Build 4
"""

import customtkinter as ctk
from core.dragon_health import DragonHealthCore


class DragonHealth(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.configure(corner_radius=12)

        self.health = DragonHealthCore().get_health()

        # -------------------------
        # Title
        # -------------------------

        title = ctk.CTkLabel(
            self,
            text="🐉 Dragon Health",
            font=("Arial", 22, "bold")
        )

        title.pack(anchor="w", padx=20, pady=(15, 10))

        # -------------------------
        # Health Rows
        # -------------------------

        self.create_row("🐳 Docker", self.health["docker"])
        self.create_row("🎬 Jellyfin", self.health["jellyfin"])
        self.create_row("💾 Movies Drive", self.health["movies"])
        self.create_row("🧠 Memory", self.health["memory"])

        # -------------------------
        # Score
        # -------------------------

        ctk.CTkLabel(
            self,
            text="Dragon Score",
            font=("Arial", 16, "bold")
        ).pack(pady=(20, 0))

        self.score = ctk.CTkLabel(
            self,
            text=f"{self.health['score']}%",
            font=("Arial", 38, "bold")
        )

        self.score.pack(pady=(0, 20))

    def create_row(self, title, value):

        row = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        row.pack(
            fill="x",
            padx=20,
            pady=5
        )

        left = ctk.CTkLabel(
            row,
            text=title,
            font=("Arial", 15)
        )

        left.pack(side="left")

        right = ctk.CTkLabel(
            row,
            text=value,
            font=("Arial", 15, "bold")
        )

        right.pack(side="right")