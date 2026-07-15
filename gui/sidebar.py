"""
Dragon Media Manager
Sidebar

Version: v0.1.3-alpha
Build 9.1
Codename: Dragon Command Center
"""

import customtkinter as ctk

from core.version import (
    APP_NAME,
    VERSION,
    BUILD,
)

from core.actions import DragonActions


class Sidebar(ctk.CTkFrame):

    WIDTH = 220

    def __init__(self, master):

        super().__init__(
            master,
            width=self.WIDTH,
            corner_radius=0
        )

        self.master = master
        self.actions = DragonActions()

        self.configure(
            fg_color="#202225"
        )

        self.grid_propagate(False)

        #
        # Logo
        #

        ctk.CTkLabel(
            self,
            text="🐉",
            font=("Arial", 42)
        ).pack(
            pady=(18, 0)
        )

        ctk.CTkLabel(
            self,
            text=APP_NAME.replace(
                " ",
                "\n",
                1
            ),
            justify="center",
            font=("Arial", 20, "bold")
        ).pack(
            pady=(0, 15)
        )

        #
        # Navigation
        #

        self.section("Navigation")

        self.dashboard_btn = self.button(
            "🏠 Dashboard",
            self.open_dashboard
        )

        self.movies_btn = self.button(
            "🎬 Movies",
            self.open_movies
        )

        self.tv_btn = self.button(
            "📺 TV Shows",
            self.open_tv
        )

        self.settings_btn = self.button(
            "⚙ Settings",
            self.open_settings
        )

        self.highlight(
            self.dashboard_btn
        )

        #
        # Quick Launch
        #

        self.section(
            "🚀 Quick Launch"
        )

        self.button(
            "🎬 Jellyfin",
            self.actions.open_jellyfin
        )

        self.button(
            "🎞 Radarr",
            self.actions.open_radarr
        )

        self.button(
            "📺 Sonarr",
            self.actions.open_sonarr
        )

        self.button(
            "🔍 Prowlarr",
            self.actions.open_prowlarr
        )

        self.button(
            "💬 Bazarr",
            self.actions.open_bazarr
        )

        self.button(
            "🎟 Jellyseerr",
            self.actions.open_jellyseerr
        )

        self.button(
            "⬇ qBittorrent",
            self.actions.open_qbittorrent
        )

        self.button(
            "🐳 Portainer",
            self.actions.open_portainer
        )        #
        # Footer
        #

        ctk.CTkLabel(
            self,
            text=f"{VERSION}\nBuild {BUILD}",
            justify="center",
            font=("Arial", 11),
            text_color="gray70",
        ).pack(
            side="bottom",
            pady=15,
        )

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    def section(self, title):

        ctk.CTkLabel(
            self,
            text=title,
            font=("Arial", 14, "bold"),
        ).pack(
            pady=(12, 6)
        )

    def button(self, text, command=None):

        btn = ctk.CTkButton(
            self,
            text=text,
            width=180,
            height=36,
            command=command,
        )

        btn.pack(
            padx=20,
            pady=3,
            fill="x",
        )

        return btn

    def highlight(self, active):

        buttons = [
            getattr(self, "dashboard_btn", None),
            getattr(self, "movies_btn", None),
            getattr(self, "tv_btn", None),
            getattr(self, "settings_btn", None),
        ]

        for btn in buttons:

            if btn is None:
                continue

            if btn == active:
                btn.configure(
                    fg_color=("#1f6aa5", "#1f6aa5")
                )
            else:
                btn.configure(
                    fg_color=("gray25", "gray25")
                )

    # --------------------------------------------------
    # Navigation
    # --------------------------------------------------

    def open_dashboard(self):

        self.highlight(self.dashboard_btn)

        if hasattr(self.master, "write_log"):
            self.master.write_log(
                "🏠 Dashboard selected"
            )

    def open_movies(self):

        self.highlight(self.movies_btn)

        if hasattr(self.master, "write_log"):
            self.master.write_log(
                "🎬 Movies selected"
            )

    def open_tv(self):

        self.highlight(self.tv_btn)

        if hasattr(self.master, "write_log"):
            self.master.write_log(
                "📺 TV Shows selected"
            )

    def open_settings(self):

        self.highlight(self.settings_btn)

        if hasattr(self.master, "write_log"):
            self.master.write_log(
                "⚙ Settings selected"
            )