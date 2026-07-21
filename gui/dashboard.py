"""
Dragon Media Manager
Version 1.2
Build 003 - Professional Command Center
"""

import customtkinter as ctk
import threading
from datetime import datetime

from core.scanner import LibraryScanner
from core.settings import MOVIES_PATH, TV_PATH
from core.dragon_downloads import DragonDownloads
from core.actions import DragonActions
from core.version import APP_NAME, VERSION_DISPLAY, WINDOW_TITLE

from gui.sidebar import Sidebar
from gui.dragon_health import DragonHealth
from gui.dragon_ai import DragonAIFrame
from gui.branding import load_dragon_image

from gui.widgets.status_bar import StatusBar
from gui.widgets.downloads_details import DownloadsDetailsWindow
from gui.widgets.card_details import (
    MoviesDetailsWindow,
    TVShowsDetailsWindow,
    EpisodesDetailsWindow,
    BackupDetailsWindow,
)
from gui.ui_scale import configure_initial_window, get_ui_scale


class Dashboard(ctk.CTk):

    DOWNLOAD_REFRESH_MS = 5000
    DOWNLOAD_AUTH_BACKOFF_MS = 300000

    #################################################################
    # INITIALISE
    #################################################################

    def __init__(self):
        super().__init__()

        self.withdraw()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title(WINDOW_TITLE)
        self.ui = configure_initial_window(self)

        self.configure(fg_color="#111418")

        self.downloads_engine = DragonDownloads()
        self._download_refresh_after_id = None
        self._download_refresh_in_progress = False
        self._download_refresh_delay_ms = self.DOWNLOAD_REFRESH_MS
        self._downloads_details_window = None
        self._movies_details_window = None
        self._tv_details_window = None
        self._episodes_details_window = None
        self._backup_details_window = None
        self._last_scan_label = "Never"

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)

        self.build_ui()

        self.deiconify()

    #################################################################
    # BUILD UI
    #################################################################

    def build_ui(self):

        self.build_sidebar()
        self.build_main()
        self.build_header()
        self.build_statistics()
        self.build_content()
        self.build_statusbar()
        self.refresh_statistics()
        self.start_download_refresh()

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
        self.main.grid_rowconfigure(
            2,
            weight=1,
            minsize=get_ui_scale().content_row_minsize(),
        )

    #################################################################
    # HEADER
    #################################################################

    def build_header(self):

        header = ctk.CTkFrame(
            self.main,
            corner_radius=15,
            fg_color="#1a1d22",
        )

        header.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=10,
            pady=(5, 15)
        )

        header.grid_columnconfigure(1, weight=1)
        header.grid_columnconfigure(2, weight=0)

        #
        # Dragon Logo
        #

        dragon_logo = load_dragon_image(48)

        if dragon_logo is not None:
            logo = ctk.CTkLabel(
                header,
                text="",
                image=dragon_logo,
            )
            self._header_dragon_image = dragon_logo
        else:
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
            text=APP_NAME,
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

        self.refresh_button = ctk.CTkButton(
            right,
            text="🔄",
            width=32,
            height=32,
            font=("Segoe UI", 14),
            command=self.refresh_dashboard,
        )
        self.refresh_button.pack(anchor="e", pady=(0, 6))

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
            text=VERSION_DISPLAY,
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

        self._make_card_clickable(
            self.movie_card,
            self.open_movies_details,
            hover_border="#4b7fd6",
        )
        self._make_card_clickable(
            self.tv_card,
            self.open_tv_details,
            hover_border="#b56df0",
        )
        self._make_card_clickable(
            self.episode_card,
            self.open_episodes_details,
            hover_border="#f7b84a",
        )
        self._make_card_clickable(
            self.download_card,
            self.open_downloads_details,
            hover_border="#3dd66b",
        )
        self._make_card_clickable(
            self.backup_card,
            self.open_backup_details,
            hover_border="#2ec4b6",
        )

    def _make_card_clickable(self, card, callback, hover_border="#3b4a5c"):

        normal_border = "#2a3038"

        def on_click(_event=None):
            callback()

        def on_enter(_event=None):
            try:
                card.configure(border_color=hover_border)
            except Exception:
                pass

        def on_leave(_event=None):
            try:
                card.configure(border_color=normal_border)
            except Exception:
                pass

        widgets = []

        def collect(widget):
            widgets.append(widget)
            for child in widget.winfo_children():
                collect(child)

        collect(card)

        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)

        for widget in widgets:
            try:
                widget.configure(cursor="hand2")
            except Exception:
                pass

            widget.bind("<Button-1>", on_click)

    def _open_detail_window(self, attr_name, window_class):

        existing = getattr(self, attr_name, None)

        if existing is not None:
            try:
                if existing.winfo_exists():
                    existing.lift()
                    existing.focus_force()
                    return
            except Exception:
                pass

        window = window_class(self)
        setattr(self, attr_name, window)

    def open_movies_details(self):

        self._open_detail_window(
            "_movies_details_window",
            MoviesDetailsWindow,
        )

    def open_tv_details(self):

        self._open_detail_window(
            "_tv_details_window",
            TVShowsDetailsWindow,
        )

    def open_episodes_details(self):

        self._open_detail_window(
            "_episodes_details_window",
            EpisodesDetailsWindow,
        )

    def open_backup_details(self):

        self._open_detail_window(
            "_backup_details_window",
            BackupDetailsWindow,
        )

    def open_downloads_details(self):

        existing = self._downloads_details_window

        if existing is not None:
            try:
                if existing.winfo_exists():
                    existing.lift()
                    existing.focus_force()
                    return
            except Exception:
                pass

        self._downloads_details_window = DownloadsDetailsWindow(
            self,
            self.downloads_engine,
        )

    def refresh_dashboard(self):

        self.refresh_statistics()

    def backup_now(self, button=None):

        try:
            if button is not None:
                button.configure(state="disabled")
        except Exception:
            pass

        self.update()

        success = False
        message = ""

        try:
            success, message = DragonActions().backup_now()

            if success:
                try:
                    self.set_card_value(
                        self.backup_card,
                        DragonActions.get_last_backup_label(),
                    )
                except Exception:
                    self.set_card_value(self.backup_card, "N/A")

            self.notify_backup_result(success, message)

        except Exception as error:
            self.notify_backup_result(False, str(error))

        finally:
            try:
                if button is not None:
                    button.configure(state="normal")
            except Exception:
                pass

    def notify_backup_result(self, success, message=""):

        try:
            if hasattr(self, "ai") and hasattr(self.ai, "core"):
                self.ai.core.report_backup_result(success, message)
        except Exception:
            pass

    def get_library_statistics(self):

        try:
            return LibraryScanner.scan_libraries(
                MOVIES_PATH,
                TV_PATH,
            )
        except Exception:
            return {
                "movies": 0,
                "tv_shows": 0,
                "episodes": 0,
                "categories": 0,
                "posters": 0,
                "nfo": 0,
                "size_gb": 0.0,
            }

    @staticmethod
    def get_library_path_status(path):

        from pathlib import Path

        library_path = Path(path)

        if not library_path.exists():
            return "Path not found"

        if not library_path.is_dir():
            return "Path is not a directory"

        return "Available"

    def get_last_scan_label(self):

        return self._last_scan_label

    def set_card_value(self, card, value):

        try:
            if hasattr(card, "value_label"):
                card.value_label.configure(text=str(value))
        except Exception:
            pass

    def refresh_statistics(self):
        """
        Update the five statistics cards from real application data.
        """

        #
        # Library counts
        #

        try:
            stats = LibraryScanner.scan_libraries(
                MOVIES_PATH,
                TV_PATH,
            )

            self.set_card_value(
                self.movie_card,
                stats.get("movies", 0),
            )
            self.set_card_value(
                self.tv_card,
                stats.get("tv_shows", 0),
            )
            self.set_card_value(
                self.episode_card,
                stats.get("episodes", 0),
            )

        except Exception as error:
            self.set_card_value(self.movie_card, 0)
            self.set_card_value(self.tv_card, 0)
            self.set_card_value(self.episode_card, 0)

        self.refresh_active_downloads()

        #
        # Last backup
        #

        try:
            backup_label = DragonActions.get_last_backup_label()
            self.set_card_value(
                self.backup_card,
                backup_label if backup_label else "N/A",
            )
        except Exception:
            self.set_card_value(self.backup_card, "N/A")

    def _apply_download_result(self, data):

        if data.get("connected"):
            active = int(data.get("active", 0) or 0)
            error = ""
            self._download_refresh_delay_ms = self.DOWNLOAD_REFRESH_MS
        else:
            active = 0
            error = data.get("error", "Unable to connect to qBittorrent")

            if data.get("auth_failure"):
                self._download_refresh_delay_ms = self.DOWNLOAD_AUTH_BACKOFF_MS

        self.set_card_value(self.download_card, active)

        if hasattr(self, "statusbar"):
            self.statusbar.set_downloads(active)
            if error:
                self.statusbar.set_status(f"qBittorrent: {error}")
            else:
                self.statusbar.set_status("🟢 Ready")

        return active

    def refresh_active_downloads(self):
        """
        Update the Downloads card and status bar from qBittorrent.
        """

        try:
            data = self.downloads_engine.get_downloads()
            return self._apply_download_result(data)
        except Exception as error:
            return self._apply_download_result(
                {
                    "connected": False,
                    "active": 0,
                    "error": str(error),
                    "auth_failure": False,
                }
            )

    def start_download_refresh(self):
        """
        Begin automatic active-download polling (single timer chain).
        """

        self._schedule_download_refresh(initial=True)

    def _schedule_download_refresh(self, initial=False):

        if self._download_refresh_after_id is not None:
            try:
                self.after_cancel(self._download_refresh_after_id)
            except Exception:
                pass
            self._download_refresh_after_id = None

        delay = 0 if initial else self._download_refresh_delay_ms
        self._download_refresh_after_id = self.after(
            delay,
            self._poll_active_downloads,
        )

    def _poll_active_downloads(self):

        self._download_refresh_after_id = None

        if self._download_refresh_in_progress:
            self._schedule_download_refresh()
            return

        self._download_refresh_in_progress = True

        def worker():

            try:
                data = self.downloads_engine.get_downloads()
            except Exception as exc:
                data = {
                    "connected": False,
                    "active": 0,
                    "error": str(exc),
                    "auth_failure": False,
                }

            self.after(
                0,
                lambda: self._apply_active_downloads(data),
            )

        threading.Thread(target=worker, daemon=True).start()

    def _apply_active_downloads(self, data):

        self._download_refresh_in_progress = False
        self._apply_download_result(data)
        self._schedule_download_refresh()

    #################################################################
    # COMMAND CENTER
    #################################################################

    def build_content(self):

        content = ctk.CTkFrame(
            self.main,
            fg_color="transparent"
        )

        content.grid(
            row=2,
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
    # LIBRARY SCANNER
    #################################################################

    def scan_library(self, button=None):

        try:
            if button is not None:
                button.configure(state="disabled")
        except Exception:
            pass

        self.update()

        try:
            stats = LibraryScanner.scan_libraries(
                MOVIES_PATH,
                TV_PATH,
            )

            self.set_card_value(
                self.movie_card,
                stats.get("movies", 0),
            )
            self.set_card_value(
                self.tv_card,
                stats.get("tv_shows", 0),
            )
            self.set_card_value(
                self.episode_card,
                stats.get("episodes", 0),
            )

        except Exception:
            self.set_card_value(self.movie_card, 0)
            self.set_card_value(self.tv_card, 0)
            self.set_card_value(self.episode_card, 0)

        self.refresh_active_downloads()

        try:
            self.set_card_value(
                self.backup_card,
                DragonActions.get_last_backup_label(),
            )
        except Exception:
            self.set_card_value(self.backup_card, "N/A")

        self._last_scan_label = "Just Now"
        self.statusbar.set_last_scan("Just Now")

        try:
            if button is not None:
                button.configure(state="normal")
        except Exception:
            pass

    #################################################################
    # APPLICATION START
    #################################################################

if __name__ == "__main__":

    app = Dashboard()

    app.mainloop()
