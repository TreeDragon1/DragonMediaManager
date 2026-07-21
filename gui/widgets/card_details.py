"""
Dragon Media Manager
Clickable statistics card detail windows.
"""

from __future__ import annotations

import customtkinter as ctk

from core.actions import DragonActions
from core.settings import MOVIES_PATH, TV_PATH
from core.version import APP_NAME
from gui.branding import load_dragon_image
from gui.ui_scale import get_ui_scale


class DragonDetailWindow(ctk.CTkToplevel):

    def __init__(self, master, title: str):
        super().__init__(master)

        self.dashboard = master
        self._closed = False

        ui = get_ui_scale()
        width, height = ui.detail_window_size()

        self.title(title)
        self.geometry(f"{width}x{height}")
        self.minsize(640, 420)
        self.configure(fg_color="#111418")
        self.transient(master)
        self.protocol("WM_DELETE_WINDOW", self.close_window)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

    def close_window(self):

        self._closed = True
        self.destroy()

    def _build_header(self, row: int, title: str, subtitle: str = "") -> ctk.CTkFrame:

        header = ctk.CTkFrame(
            self,
            fg_color="#1a1d22",
            corner_radius=12,
            border_width=1,
            border_color="#2a3038",
        )
        header.grid(
            row=row,
            column=0,
            sticky="ew",
            padx=16,
            pady=(16, 10),
        )

        title_row = ctk.CTkFrame(header, fg_color="transparent")
        title_row.pack(fill="x", padx=14, pady=12)

        dragon = load_dragon_image(28)

        if dragon is not None:
            logo = ctk.CTkLabel(title_row, text="", image=dragon)
            self._dragon_image = dragon
            logo.pack(side="left", padx=(0, 8))

        text_frame = ctk.CTkFrame(title_row, fg_color="transparent")
        text_frame.pack(side="left", fill="x", expand=True)

        ctk.CTkLabel(
            text_frame,
            text=title,
            font=("Segoe UI", 20, "bold"),
            text_color="#e5e7eb",
            anchor="w",
        ).pack(anchor="w")

        if subtitle:
            ctk.CTkLabel(
                text_frame,
                text=subtitle,
                font=("Segoe UI", 12),
                text_color="#8f98a3",
                anchor="w",
            ).pack(anchor="w", pady=(2, 0))

        return header

    def _build_body(self, row: int) -> ctk.CTkScrollableFrame:

        body = ctk.CTkScrollableFrame(
            self,
            fg_color="#1a1d22",
            corner_radius=12,
            border_width=1,
            border_color="#2a3038",
        )
        body.grid(
            row=row,
            column=0,
            sticky="nsew",
            padx=16,
            pady=(0, 10),
        )
        return body

    def _add_info_block(
        self,
        parent: ctk.CTkScrollableFrame,
        label: str,
        value: str,
    ):

        block = ctk.CTkFrame(
            parent,
            fg_color="#15181d",
            corner_radius=10,
            border_width=1,
            border_color="#2a3038",
        )
        block.pack(fill="x", padx=10, pady=6)

        ctk.CTkLabel(
            block,
            text=label,
            font=("Segoe UI", 12, "bold"),
            text_color="#8f98a3",
            anchor="w",
        ).pack(anchor="w", fill="x", padx=14, pady=(12, 2))

        ctk.CTkLabel(
            block,
            text=str(value),
            font=("Segoe UI", 15),
            text_color="#e5e7eb",
            anchor="w",
            justify="left",
            wraplength=700,
        ).pack(anchor="w", fill="x", padx=14, pady=(0, 12))

    def _build_footer(
        self,
        row: int,
        primary_text: str | None = None,
        primary_command=None,
    ) -> ctk.CTkButton | None:

        footer = ctk.CTkFrame(self, fg_color="transparent")
        footer.grid(
            row=row,
            column=0,
            sticky="ew",
            padx=16,
            pady=(0, 16),
        )

        primary_button = None

        if primary_text and primary_command:
            primary_button = ctk.CTkButton(
                footer,
                text=primary_text,
                width=140,
                height=36,
                command=primary_command,
            )
            primary_button.pack(side="left")

        ctk.CTkButton(
            footer,
            text="Close",
            width=120,
            height=36,
            command=self.close_window,
        ).pack(side="right")

        return primary_button


class MoviesDetailsWindow(DragonDetailWindow):

    def __init__(self, master):
        super().__init__(master, "Movies Library")
        self._build_header(0, "Movies Library", "Movie collection overview")
        self.body = self._build_body(1)
        self.scan_button = self._build_footer(
            2,
            primary_text="Scan Library",
            primary_command=self._scan_library,
        )
        self._refresh_content()
        self.after(100, self.lift)

    def _refresh_content(self):

        for child in self.body.winfo_children():
            child.destroy()

        stats = self.dashboard.get_library_statistics()

        self._add_info_block(
            self.body,
            "Total Movies",
            stats.get("movies", 0),
        )
        self._add_info_block(
            self.body,
            "Library Path",
            MOVIES_PATH,
        )
        self._add_info_block(
            self.body,
            "Library Status",
            self.dashboard.get_library_path_status(MOVIES_PATH),
        )
        self._add_info_block(
            self.body,
            "Categories",
            stats.get("categories", 0),
        )
        self._add_info_block(
            self.body,
            "Posters",
            stats.get("posters", 0),
        )
        self._add_info_block(
            self.body,
            "Metadata Files",
            stats.get("nfo", 0),
        )
        self._add_info_block(
            self.body,
            "Library Size (GB)",
            stats.get("size_gb", 0.0),
        )
        self._add_info_block(
            self.body,
            "Last Scan",
            self.dashboard.get_last_scan_label(),
        )

    def _scan_library(self):

        self.dashboard.scan_library(button=self.scan_button)
        self._refresh_content()


class TVShowsDetailsWindow(DragonDetailWindow):

    def __init__(self, master):
        super().__init__(master, "TV Shows Library")
        self._build_header(0, "TV Shows Library", "Series collection overview")
        self.body = self._build_body(1)
        self.scan_button = self._build_footer(
            2,
            primary_text="Scan Library",
            primary_command=self._scan_library,
        )
        self._refresh_content()
        self.after(100, self.lift)

    def _refresh_content(self):

        for child in self.body.winfo_children():
            child.destroy()

        stats = self.dashboard.get_library_statistics()

        self._add_info_block(
            self.body,
            "TV Series",
            stats.get("tv_shows", 0),
        )
        self._add_info_block(
            self.body,
            "Library Path",
            TV_PATH,
        )
        self._add_info_block(
            self.body,
            "Library Status",
            self.dashboard.get_library_path_status(TV_PATH),
        )
        self._add_info_block(
            self.body,
            "Episodes",
            stats.get("episodes", 0),
        )
        self._add_info_block(
            self.body,
            "Last Scan",
            self.dashboard.get_last_scan_label(),
        )

    def _scan_library(self):

        self.dashboard.scan_library(button=self.scan_button)
        self._refresh_content()


class EpisodesDetailsWindow(DragonDetailWindow):

    def __init__(self, master):
        super().__init__(master, "Episodes Library")
        self._build_header(0, "Episodes Library", "Episode collection overview")
        self.body = self._build_body(1)
        self._build_footer(2)
        self._refresh_content()
        self.after(100, self.lift)

    def _refresh_content(self):

        for child in self.body.winfo_children():
            child.destroy()

        stats = self.dashboard.get_library_statistics()

        self._add_info_block(
            self.body,
            "Total Episodes",
            stats.get("episodes", 0),
        )
        self._add_info_block(
            self.body,
            "TV Series",
            stats.get("tv_shows", 0),
        )
        self._add_info_block(
            self.body,
            "Library Path",
            TV_PATH,
        )
        self._add_info_block(
            self.body,
            "Library Status",
            self.dashboard.get_library_path_status(TV_PATH),
        )
        self._add_info_block(
            self.body,
            "Last Scan",
            self.dashboard.get_last_scan_label(),
        )


class BackupDetailsWindow(DragonDetailWindow):

    def __init__(self, master):
        super().__init__(master, "Backup Details")
        self._build_header(0, "Backup Details", f"{APP_NAME} backups")
        self.body = self._build_body(1)
        self.backup_button = self._build_footer(
            2,
            primary_text="Backup Now",
            primary_command=self._backup_now,
        )
        self._refresh_content()
        self.after(100, self.lift)

    def _refresh_content(self):

        for child in self.body.winfo_children():
            child.destroy()

        info = DragonActions.get_last_backup_info()

        self._add_info_block(
            self.body,
            "Last Backup",
            info.get("label", "N/A"),
        )
        self._add_info_block(
            self.body,
            "Status",
            info.get("status", "Unknown"),
        )

        if info.get("modified"):
            self._add_info_block(
                self.body,
                "Last Backup Time",
                info["modified"],
            )

        if info.get("filename"):
            self._add_info_block(
                self.body,
                "Latest Backup File",
                info["filename"],
            )

        self._add_info_block(
            self.body,
            "Backup Folder",
            info.get("folder", "N/A"),
        )

    def _backup_now(self):

        self.dashboard.backup_now(button=self.backup_button)
        self._refresh_content()
