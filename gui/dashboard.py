"""
Dragon Media Manager
Version 1.2
Build 003 - Professional Command Center
"""

import customtkinter as ctk
from datetime import datetime

from core.scanner import LibraryScanner

from gui.sidebar import Sidebar
from gui.dragon_health import DragonHealth
from gui.dragon_ai import DragonAIFrame

from gui.widgets.action_bar import ActionBar
from gui.widgets.downloads_panel import DownloadsPanel
from gui.widgets.recent_activity import RecentActivity
from gui.widgets.status_bar import StatusBar

# New widget



class Dashboard(ctk.CTk):

    #################################################################
    # INITIALISE
    #################################################################

    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title("🐉 Dragon Media Manager")
        self.geometry("1850x1040")
        self.minsize(1600, 900)

        self.configure(fg_color="#111418")

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)

        self.build_ui()

    #################################################################
    # BUILD UI
    #################################################################

    def build_ui(self):

        self.build_sidebar()
        self.build_main()
        self.build_header()
        self.build_statistics()
        self.build_action_bar()
        self.build_content()
        self.build_lower()
        self.build_statusbar()

    #################################################################
    # SIDEBAR
    #################################################################

    def build_sidebar(self):

        self.sidebar = Sidebar(self)

        self.sidebar.grid(
            row=0,
            column=0,
            sticky="nsw"
        )

    #################################################################
    # MAIN FRAME
    #################################################################

    def build_main(self):

        self.main = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.main.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=20,
            pady=(16, 8)
        )

        self.main.grid_columnconfigure(0, weight=1)

        self.main.grid_rowconfigure(0, weight=0)
        self.main.grid_rowconfigure(1, weight=0)
        self.main.grid_rowconfigure(2, weight=0)
        self.main.grid_rowconfigure(3, weight=1, minsize=420)
        self.main.grid_rowconfigure(4, weight=0)

    #################################################################
    # HEADER
    #################################################################

    def build_header(self):

        header = ctk.CTkFrame(
            self.main,
            corner_radius=15,
            fg_color="#1a1d22",
            height=95
        )

        header.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=10,
            pady=(5, 15)
        )

        header.grid_columnconfigure(1, weight=1)

        #
        # Dragon Logo
        #

        logo = ctk.CTkLabel(
            header,
            text="🐉",
            font=("Segoe UI Emoji", 42)
        )

        logo.grid(
            row=0,
            column=0,
            rowspan=2,
            padx=(20, 10),
            pady=15
        )

        #
        # Title
        #

        ctk.CTkLabel(
            header,
            text="Dragon Media Manager",
            font=("Segoe UI", 28, "bold")
        ).grid(
            row=0,
            column=1,
            sticky="sw"
        )

        ctk.CTkLabel(
            header,
            text="Dragon Command Center",
            font=("Segoe UI", 15),
            text_color="#8f98a3"
        ).grid(
            row=1,
            column=1,
            sticky="nw"
        )

        #
        # Right Side
        #

        right = ctk.CTkFrame(
            header,
            fg_color="transparent"
        )

        right.grid(
            row=0,
            column=2,
            rowspan=2,
            padx=20
        )

        self.clock_label = ctk.CTkLabel(
            right,
            text=datetime.now().strftime("%H:%M:%S"),
            font=("Segoe UI", 16, "bold")
        )

        self.clock_label.pack(anchor="e")

        self.status_label = ctk.CTkLabel(
            right,
            text="🟢 ONLINE",
            font=("Segoe UI", 15, "bold"),
            text_color="#4ade80"
        )

        self.status_label.pack(anchor="e", pady=(5, 0))

        self.version_label = ctk.CTkLabel(
            right,
            text="Version 1.2 • Build 003",
            font=("Segoe UI", 12),
            text_color="#9aa3af"
        )

        self.version_label.pack(anchor="e")

        self.update_clock()

    #################################################################
    # CLOCK
    #################################################################

    def update_clock(self):

        self.clock_label.configure(
            text=datetime.now().strftime("%H:%M:%S")
        )

        self.after(1000, self.update_clock)

    #################################################################
    # STATISTICS
    #################################################################

    def create_card(
        self,
        parent,
        icon,
        title,
        value,
        subtitle,
        accent
    ):

        frame = ctk.CTkFrame(
            parent,
            corner_radius=15,
            fg_color="#1a1d22",
            border_width=1,
            border_color="#2a3038"
        )

        frame.grid_columnconfigure(0, weight=1)

        accent_bar = ctk.CTkFrame(
            frame,
            height=4,
            corner_radius=0,
            fg_color=accent
        )

        accent_bar.grid(
            row=0,
            column=0,
            sticky="ew"
        )

        content = ctk.CTkFrame(
            frame,
            fg_color="transparent"
        )

        content.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=16,
            pady=(12, 14)
        )

        content.grid_columnconfigure(0, weight=1)

        top = ctk.CTkFrame(
            content,
            fg_color="transparent"
        )

        top.grid(
            row=0,
            column=0,
            sticky="ew"
        )

        top.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            top,
            text=icon,
            font=("Segoe UI Emoji", 22),
            text_color=accent
        ).grid(
            row=0,
            column=0,
            sticky="w"
        )

        ctk.CTkLabel(
            top,
            text=title,
            font=("Segoe UI", 14, "bold"),
            text_color="#c5ccd6"
        ).grid(
            row=0,
            column=1,
            sticky="w",
            padx=(10, 0)
        )

        value_label = ctk.CTkLabel(
            content,
            text=value,
            font=("Segoe UI", 32, "bold"),
            text_color=accent
        )

        value_label.grid(
            row=1,
            column=0,
            sticky="w",
            pady=(10, 2)
        )

        subtitle_label = ctk.CTkLabel(
            content,
            text=subtitle,
            font=("Segoe UI", 12),
            text_color="#8f98a3"
        )

        subtitle_label.grid(
            row=2,
            column=0,
            sticky="w"
        )

        frame.value_label = value_label
        frame.subtitle_label = subtitle_label

        return frame

    def build_statistics(self):

        stats = ctk.CTkFrame(
            self.main,
            fg_color="transparent"
        )

        stats.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=10,
            pady=(0, 15)
        )

        for i in range(5):
            stats.grid_columnconfigure(i, weight=1, uniform="stats")

        self.movie_card = self.create_card(
            stats,
            icon="🎬",
            title="Movies",
            value="0",
            subtitle="Total Movies",
            accent="#3b82f6"
        )

        self.tv_card = self.create_card(
            stats,
            icon="📺",
            title="TV Shows",
            value="0",
            subtitle="Series",
            accent="#a855f7"
        )

        self.episode_card = self.create_card(
            stats,
            icon="🎞",
            title="Episodes",
            value="0",
            subtitle="Episodes",
            accent="#f59e0b"
        )

        self.download_card = self.create_card(
            stats,
            icon="⬇",
            title="Downloads",
            value="0",
            subtitle="Active",
            accent="#22c55e"
        )

        self.backup_card = self.create_card(
            stats,
            icon="💾",
            title="Last Backup",
            value="--",
            subtitle="Status",
            accent="#14b8a6"
        )

        cards = [
            self.movie_card,
            self.tv_card,
            self.episode_card,
            self.download_card,
            self.backup_card
        ]

        for column, card in enumerate(cards):
            card.grid(
                row=0,
                column=column,
                padx=8,
                pady=8,
                sticky="ew"
            )

    #################################################################
    # ACTION BAR
    #################################################################

    def build_action_bar(self):

        self.action_bar = ActionBar(
            self.main,
            scan_callback=self.scan_library,
            refresh_callback=self.refresh_dashboard,
            settings_callback=self.open_settings
        )

        self.action_bar.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=10,
            pady=(0,15)
        )


    def refresh_dashboard(self):

        self.write_log("🔄 Dashboard refreshed")


    def open_settings(self):

        self.write_log("⚙ Settings clicked")
    #################################################################
    # COMMAND CENTER
    #################################################################

    def build_content(self):

        content = ctk.CTkFrame(
            self.main,
            fg_color="transparent"
        )

        content.grid(
            row=3,
            column=0,
            sticky="nsew",
            padx=10,
            pady=(0, 8)
        )

        content.grid_columnconfigure(0, weight=1, uniform="command")
        content.grid_columnconfigure(1, weight=1, uniform="command")
        content.grid_rowconfigure(0, weight=1)

        ###############################################################
        # Middle-left: Dragon Health (large)
        ###############################################################

        self.health = DragonHealth(content)

        self.health.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 10),
            pady=0
        )

        ###############################################################
        # Middle-right: Dragon AI (expanded)
        ###############################################################

        self.ai = DragonAIFrame(content)

        self.ai.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(10, 0),
            pady=0
        )

    #################################################################
    # LOWER SECTION (Downloads + Dragon Monitor)
    #################################################################

    def build_lower(self):

        lower = ctk.CTkFrame(
            self.main,
            fg_color="transparent"
        )

        lower.grid(
            row=4,
            column=0,
            sticky="ew",
            padx=10,
            pady=(0, 4)
        )

        lower.grid_columnconfigure(0, weight=1)

        #
        # Compact Active Downloads (does not compete with Health)
        #

        downloads_wrap = ctk.CTkFrame(
            lower,
            fg_color="#1a1d22",
            corner_radius=12,
            border_width=1,
            border_color="#2a3038",
            height=88
        )

        downloads_wrap.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(0, 8)
        )

        downloads_wrap.grid_propagate(False)
        downloads_wrap.grid_columnconfigure(0, weight=1)

        self.downloads = DownloadsPanel(downloads_wrap)

        self.downloads.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=4,
            pady=2
        )

        #
        # Full-width Dragon Monitor (reuses RecentActivity)
        #

        monitor = ctk.CTkFrame(
            lower,
            fg_color="#1a1d22",
            corner_radius=12,
            border_width=1,
            border_color="#2a3038",
            height=190
        )

        monitor.grid(
            row=1,
            column=0,
            sticky="ew"
        )

        monitor.grid_propagate(False)
        monitor.grid_columnconfigure(0, weight=1)
        monitor.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            monitor,
            text="📡 Dragon Monitor",
            font=("Segoe UI", 16, "bold"),
            text_color="#e5e7eb"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=14,
            pady=(10, 4)
        )

        self.activity = RecentActivity(monitor)

        self.activity.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=8,
            pady=(0, 8)
        )

        # Compatibility log sink used by write_log()
        self.log = ctk.CTkTextbox(
            monitor,
            height=1,
            width=1
        )
        self.log.grid_remove()

        self.write_log("🐉 Dragon Media Centre started")
        self.write_log("Version 1.2 • Build 003")
        self.write_log("Widgets initialized")

    #################################################################
    # STATUS BAR
    #################################################################

    def build_statusbar(self):

        self.statusbar = StatusBar(self)

        self.statusbar.grid(
            row=1,
            column=1,
            sticky="ew",
            padx=20,
            pady=(0, 10)
        )

    #################################################################
    # LOGGING
    #################################################################

    def write_log(self, message):

        if hasattr(self, "activity"):
            self.activity.add(message)

        if hasattr(self, "log"):
            try:
                self.log.insert("end", message + "\n")
                self.log.see("end")
            except Exception:
                pass

    #################################################################
    # LIBRARY SCANNER
    #################################################################

    def scan_library(self):

        self.write_log("🔍 Library Scan Started")

        self.action_bar.scan_button.configure(state="disabled")

        self.update()

        scanner = LibraryScanner("/media/treedragon/Movies1")

        stats = scanner.scan()

        self.movie_card.value_label.configure(
            text=str(stats["movies"])
        )

        self.episode_card.value_label.configure(
            text=str(stats.get("tv", 0))
        )

        self.statusbar.set_last_scan("Just Now")

        self.write_log("✅ Library Scan Complete")

        self.action_bar.scan_button.configure(state="normal")

    #################################################################
    # APPLICATION START
    #################################################################

if __name__ == "__main__":

    app = Dashboard()

    app.mainloop()
