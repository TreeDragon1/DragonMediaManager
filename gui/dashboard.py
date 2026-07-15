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
from gui.widgets.quick_actions import QuickActionsPanel
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
        self.build_log()
        self.build_statusbar()

    #################################################################
    # SIDEBAR
    #################################################################

    def build_sidebar(self):

        self.sidebar = Sidebar(self)

        self.sidebar.grid(
            row=0,
            column=0,
            sticky="ns"
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
            pady=20
        )

        self.main.grid_columnconfigure(0, weight=1)

        self.main.grid_rowconfigure(3, weight=1)
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
    # BUILD USER INTERFACE
    #################################################################

    def build_ui(self):

        self.build_sidebar()
        self.build_main()
        self.build_header()
        self.build_statistics()
        self.build_action_bar()
        self.build_content()
        self.build_log()
        self.build_statusbar()

    #################################################################
    # SIDEBAR
    #################################################################

    def build_sidebar(self):

        self.sidebar = Sidebar(self)

        self.sidebar.grid(
            row=0,
            column=0,
            sticky="ns"
        )

    #################################################################
    # MAIN FRAME
    #################################################################

    def build_main(self):

        self.main = ctk.CTkFrame(self)

        self.main.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=20,
            pady=20
        )

        self.main.grid_columnconfigure(0, weight=1)

        self.main.grid_rowconfigure(3, weight=3)
        self.main.grid_rowconfigure(4, weight=1)

    #################################################################
    # HEADER
    #################################################################

    def build_header(self):

        header = ctk.CTkFrame(self.main)

        header.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=10,
            pady=(10,15)
        )

        header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            header,
            text="🐉 Dragon Media Manager",
            font=("Arial",30,"bold")
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=15,
            pady=(12,2)
        )

        ctk.CTkLabel(
            header,
            text="Dragon Command Center",
            font=("Arial",16)
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=15,
            pady=(0,12)
        )

        self.header_status = ctk.CTkLabel(
            header,
            text="🟢 Online",
            font=("Arial",16,"bold")
        )

        self.header_status.grid(
            row=0,
            column=1,
            rowspan=2,
            padx=20
        )
            #################################################################
    # STATISTICS
    #################################################################

    def create_card(self, parent, title, value):

        frame = ctk.CTkFrame(parent)

        frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            frame,
            text=title,
            font=("Arial", 16, "bold")
        ).grid(
            row=0,
            column=0,
            pady=(12,4)
        )

        value_label = ctk.CTkLabel(
            frame,
            text=value,
            font=("Arial",30)
        )

        value_label.grid(
            row=1,
            column=0,
            pady=(0,12)
        )

        frame.value_label = value_label

        return frame


    def build_statistics(self):

        stats = ctk.CTkFrame(self.main)

        stats.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=10,
            pady=(0,15)
        )

        for i in range(4):
            stats.grid_columnconfigure(i, weight=1)

        self.movie_card = self.create_card(
            stats,
            "🎬 Movies",
            "0"
        )

        self.category_card = self.create_card(
            stats,
            "📂 Categories",
            "0"
        )

        self.poster_card = self.create_card(
            stats,
            "🖼 Posters",
            "0"
        )

        self.nfo_card = self.create_card(
            stats,
            "📄 NFO Files",
            "0"
        )

        self.movie_card.grid(
            row=0,
            column=0,
            padx=8,
            pady=8,
            sticky="ew"
        )

        self.category_card.grid(
            row=0,
            column=1,
            padx=8,
            pady=8,
            sticky="ew"
        )

        self.poster_card.grid(
            row=0,
            column=2,
            padx=8,
            pady=8,
            sticky="ew"
        )

        self.nfo_card.grid(
            row=0,
            column=3,
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

        content = ctk.CTkFrame(self.main)

        content.grid(
            row=3,
            column=0,
            sticky="nsew",
            padx=10,
            pady=5
        )

        content.grid_columnconfigure(0, weight=1)
        content.grid_columnconfigure(1, weight=1)
        content.grid_rowconfigure(0, weight=1)
        content.grid_rowconfigure(1, weight=1)

        #
        # LEFT COLUMN
        #

        self.health = DragonHealth(content)

        self.health.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0,8),
            pady=(0,8)
        )

        self.downloads = DownloadsPanel(content)

        self.downloads.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=(0,8),
            pady=(8,0)
        )

        #
        # RIGHT COLUMN
        #

        self.ai = DragonAIFrame(content)

        self.ai.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(8,0),
            pady=(0,8)
        )

        self.activity = RecentActivity(content)

        self.activity.grid(
            row=1,
            column=1,
            sticky="nsew",
            padx=(8,0),
            pady=(8,0)
        )

        content.grid_rowconfigure(2, weight=0)

        self.quick_actions = QuickActionsPanel(content)

        self.quick_actions.grid(
            row=2,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=8,
            pady=(12,0)
        )
    #################################################################
    # DRAGON LOG
    #################################################################

    def build_log(self):

        log_frame = ctk.CTkFrame(self.main)

        log_frame.grid(
            row=4,
            column=0,
            sticky="nsew",
            padx=10,
            pady=(10,5)
        )

        ctk.CTkLabel(
            log_frame,
            text="📜 Dragon Log",
            font=("Arial",18,"bold")
        ).pack(
            anchor="w",
            padx=10,
            pady=(10,5)
        )

        self.log = ctk.CTkTextbox(
            log_frame,
            height=120
        )

        self.log.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=(0,10)
        )

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
            pady=(0,10)
        )

    #################################################################
    # LOGGING
    #################################################################

    def write_log(self, message):

        self.log.insert("end", message + "\n")
        self.log.see("end")

        if hasattr(self, "activity"):
            self.activity.add(message)

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

        self.category_card.value_label.configure(
            text=str(stats["categories"])
        )

        self.poster_card.value_label.configure(
            text=str(stats["posters"])
        )

        self.nfo_card.value_label.configure(
            text=str(stats["nfo"])
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
