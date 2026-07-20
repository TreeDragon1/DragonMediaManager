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

    WIDTH = 200

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

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._build_header()
        self._build_scroll_body()
        self._build_footer()

    # --------------------------------------------------
    # Header / Footer
    # --------------------------------------------------

    def _build_header(self):

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew")

        ctk.CTkLabel(
            header,
            text="🐉",
            font=("Arial", 42)
        ).pack(
            pady=(14, 0)
        )

        ctk.CTkLabel(
            header,
            text=APP_NAME.replace(
                " ",
                "\n",
                1
            ),
            justify="center",
            font=("Arial", 18, "bold")
        ).pack(
            pady=(0, 8)
        )

    def _build_footer(self):

        ctk.CTkLabel(
            self,
            text=f"{VERSION}\nBuild {BUILD}",
            justify="center",
            font=("Arial", 11),
            text_color="gray70",
        ).grid(
            row=2,
            column=0,
            pady=10,
            sticky="ew",
        )

    # --------------------------------------------------
    # Scrollable body
    # --------------------------------------------------

    def _build_scroll_body(self):

        self.scroll = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            corner_radius=0,
            width=self.WIDTH - 8,
        )

        self.scroll.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=2,
            pady=(0, 4),
        )

        self.scroll.grid_columnconfigure(0, weight=1)

        self._build_navigation()
        self._build_quick_launch()
        self._build_system_actions()

    def _build_navigation(self):

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

        self.highlight(self.dashboard_btn)

        ctk.CTkFrame(
            self.scroll,
            height=2,
            fg_color="#34373d"
        ).pack(
            fill="x",
            padx=14,
            pady=(10, 6)
        )

    def _build_quick_launch(self):

        self.section("Quick Launch")

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
        )

        ctk.CTkFrame(
            self.scroll,
            height=2,
            fg_color="#34373d"
        ).pack(
            fill="x",
            padx=14,
            pady=(10, 6)
        )

    def _build_system_actions(self):

        self.section("System Actions")

        self.action_status = ctk.CTkLabel(
            self.scroll,
            text="Status: Ready",
            font=("Segoe UI", 11),
            text_color="lightgreen",
        )
        self.action_status.pack(
            anchor="w",
            padx=16,
            pady=(0, 6),
        )

        system_actions = [
            ("💾 Backup Now", self.backup_now),
            ("🎬 Restart Jellyfin", self.restart_jellyfin),
            ("📺 Restart Sonarr", self.restart_sonarr),
            ("🎥 Restart Radarr", self.restart_radarr),
            ("🔍 Restart Prowlarr", self.restart_prowlarr),
            ("💬 Restart Bazarr", self.restart_bazarr),
            ("⬇ Restart qBittorrent", self.restart_qbittorrent),
            ("🎞 Restart Jellyseerr", self.restart_jellyseerr),
            ("🔄 Restart Media Stack", self.restart_stack),
            ("🎬 Scan Jellyfin", self.not_ready),
        ]

        for text, command in system_actions:
            self.compact_button(text, command)

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    def section(self, title):

        ctk.CTkLabel(
            self.scroll,
            text=title,
            font=("Arial", 13, "bold"),
            text_color="#c5ccd6",
        ).pack(
            anchor="w",
            padx=16,
            pady=(8, 4)
        )

    def button(self, text, command=None):

        btn = ctk.CTkButton(
            self.scroll,
            text=text,
            width=160,
            height=32,
            font=("Segoe UI", 12),
            command=command,
        )

        btn.pack(
            padx=14,
            pady=2,
            fill="x",
        )

        return btn

    def compact_button(self, text, command=None):

        btn = ctk.CTkButton(
            self.scroll,
            text=text,
            width=160,
            height=26,
            font=("Segoe UI", 11),
            command=command,
        )

        btn.pack(
            padx=14,
            pady=1,
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

    def update_status(self, success, message):

        if success:

            self.action_status.configure(
                text=f"✅ {message}",
                text_color="lightgreen"
            )

            if hasattr(self.master, "write_log"):
                self.master.write_log(f"✅ {message}")

        else:

            self.action_status.configure(
                text=f"❌ {message}",
                text_color="red"
            )

            if hasattr(self.master, "write_log"):
                self.master.write_log(f"❌ {message}")

    # --------------------------------------------------
    # System Actions (same callbacks as QuickActionsPanel)
    # --------------------------------------------------

    def restart_jellyfin(self):
        self.update_status(*self.actions.restart_jellyfin())

    def restart_sonarr(self):
        self.update_status(*self.actions.restart_sonarr())

    def restart_radarr(self):
        self.update_status(*self.actions.restart_radarr())

    def restart_prowlarr(self):
        self.update_status(*self.actions.restart_prowlarr())

    def restart_bazarr(self):
        self.update_status(*self.actions.restart_bazarr())

    def restart_qbittorrent(self):
        self.update_status(*self.actions.restart_qbittorrent())

    def restart_jellyseerr(self):
        self.update_status(*self.actions.restart_jellyseerr())

    def restart_stack(self):
        self.update_status(*self.actions.restart_media_stack())

    def backup_now(self):
        self.update_status(*self.actions.backup_now())

    def not_ready(self):

        self.action_status.configure(
            text="🚧 Coming Soon",
            text_color="orange"
        )

        if hasattr(self.master, "write_log"):
            self.master.write_log("🚧 Scan Jellyfin: Coming Soon")

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
