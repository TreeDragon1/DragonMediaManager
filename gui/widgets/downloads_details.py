"""
Dragon Media Manager
Active Downloads Details Window
"""

import threading

import customtkinter as ctk

from gui.branding import load_dragon_image


STATE_LABELS = {
    "downloading": "Downloading",
    "forcedDL": "Forced Download",
    "metaDL": "Fetching Metadata",
    "stalledDL": "Stalled",
}


def format_speed(bytes_per_sec):

    try:
        speed = float(bytes_per_sec or 0)
    except (TypeError, ValueError):
        return "0 B/s"

    if speed < 1024:
        return f"{speed:.0f} B/s"

    if speed < 1024 ** 2:
        return f"{speed / 1024:.1f} KB/s"

    return f"{speed / (1024 ** 2):.1f} MB/s"


def format_eta(seconds):

    try:
        eta = int(seconds)
    except (TypeError, ValueError):
        return "N/A"

    if eta < 0 or eta >= 8640000:
        return "∞"

    if eta < 60:
        return f"{eta}s"

    if eta < 3600:
        minutes = eta // 60
        secs = eta % 60
        return f"{minutes}m {secs}s"

    hours = eta // 3600
    minutes = (eta % 3600) // 60
    return f"{hours}h {minutes}m"


class DownloadsDetailsWindow(ctk.CTkToplevel):

    REFRESH_MS = 5000

    def __init__(self, master, downloads_engine):
        super().__init__(master)

        self.downloads_engine = downloads_engine
        self._refresh_after_id = None
        self._refresh_in_progress = False
        self._closed = False

        self.title("Active Downloads")
        self.geometry("780x520")
        self.minsize(640, 420)
        self.configure(fg_color="#111418")

        self.transient(master)
        self.protocol("WM_DELETE_WINDOW", self.close_window)

        self._build_ui()

        self.after(100, self.lift)
        self.after(150, self._start_refresh)

    def _build_ui(self):

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        header = ctk.CTkFrame(
            self,
            fg_color="#1a1d22",
            corner_radius=12,
            border_width=1,
            border_color="#2a3038",
        )
        header.grid(
            row=0,
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

        ctk.CTkLabel(
            title_row,
            text="Active Downloads",
            font=("Segoe UI", 20, "bold"),
            text_color="#e5e7eb",
        ).pack(side="left")

        self.status_label = ctk.CTkLabel(
            title_row,
            text="Loading...",
            font=("Segoe UI", 12),
            text_color="#8f98a3",
        )
        self.status_label.pack(side="right")

        self.list_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="#1a1d22",
            corner_radius=12,
            border_width=1,
            border_color="#2a3038",
        )
        self.list_frame.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=16,
            pady=(0, 10),
        )

        footer = ctk.CTkFrame(self, fg_color="transparent")
        footer.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=16,
            pady=(0, 16),
        )

        ctk.CTkButton(
            footer,
            text="Close",
            width=120,
            height=36,
            command=self.close_window,
        ).pack(side="right")

        # Placeholder so the panel is never empty before first refresh.
        self._show_message("Loading active downloads...")

    def _clear_list(self):

        for child in list(self.list_frame.winfo_children()):
            try:
                child.destroy()
            except Exception:
                pass

    def _start_refresh(self):

        self._poll_downloads()

    def _schedule_refresh(self):

        if self._closed:
            return

        if self._refresh_after_id is not None:
            try:
                self.after_cancel(self._refresh_after_id)
            except Exception:
                pass
            self._refresh_after_id = None

        self._refresh_after_id = self.after(
            self.REFRESH_MS,
            self._poll_downloads,
        )

    def _poll_downloads(self):

        if self._closed:
            return

        self._refresh_after_id = None

        if self._refresh_in_progress:
            self._schedule_refresh()
            return

        self._refresh_in_progress = True

        def worker():

            try:
                data = self.downloads_engine.get_downloads()
            except Exception as error:
                data = {
                    "connected": False,
                    "active": 0,
                    "downloads": [],
                    "error": str(error),
                }

            if self._closed:
                return

            # Capture data in default-arg to avoid late-binding issues.
            self.after(0, lambda d=data: self._apply_data(d))

        threading.Thread(target=worker, daemon=True).start()

    def _apply_data(self, data):

        if self._closed:
            return

        self._refresh_in_progress = False

        try:
            self._render_data(data)
        except Exception as error:
            self._clear_list()
            self.status_label.configure(
                text="Error",
                text_color="#f87171",
            )
            self._show_message(f"Unable to display downloads:\n{error}")

        self._schedule_refresh()

    def _render_data(self, data):

        self._clear_list()

        if not isinstance(data, dict):
            self.status_label.configure(
                text="Error",
                text_color="#f87171",
            )
            self._show_message("Unexpected download data format.")
            return

        if not data.get("connected"):
            error = data.get("error") or "Unable to connect to qBittorrent"
            self.status_label.configure(
                text="Offline",
                text_color="#f87171",
            )
            self._show_message(f"qBittorrent unavailable:\n{error}")
            return

        downloads = data.get("downloads")
        if downloads is None:
            downloads = []

        if not isinstance(downloads, list):
            downloads = list(downloads)

        active = int(data.get("active", len(downloads)) or 0)

        self.status_label.configure(
            text=f"{active} active",
            text_color="#4ade80",
        )

        if not downloads:
            self._show_message("No active downloads")
            return

        for item in downloads:
            if not isinstance(item, dict):
                continue
            self._add_download_row(item)

        # If every item was skipped, still show feedback.
        if not self.list_frame.winfo_children():
            self._show_message("No active downloads")

    def _show_message(self, text):

        ctk.CTkLabel(
            self.list_frame,
            text=str(text),
            font=("Segoe UI", 15),
            text_color="#c5ccd6",
            justify="left",
            anchor="w",
        ).pack(
            anchor="w",
            fill="x",
            padx=18,
            pady=24,
        )

    def _add_download_row(self, item):

        row = ctk.CTkFrame(
            self.list_frame,
            fg_color="#15181d",
            corner_radius=10,
            border_width=1,
            border_color="#2a3038",
        )
        row.pack(fill="x", padx=10, pady=6)

        name = item.get("name") or "Unknown torrent"

        try:
            progress = float(item.get("progress", 0) or 0)
        except (TypeError, ValueError):
            progress = 0.0

        speed = format_speed(item.get("speed"))
        eta = format_eta(item.get("eta"))
        state = STATE_LABELS.get(
            item.get("state"),
            str(item.get("state") or "Unknown"),
        )

        ctk.CTkLabel(
            row,
            text=str(name),
            font=("Segoe UI", 14, "bold"),
            text_color="#ffffff",
            anchor="w",
            justify="left",
            wraplength=700,
        ).pack(
            anchor="w",
            fill="x",
            padx=14,
            pady=(12, 4),
        )

        ctk.CTkLabel(
            row,
            text=f"Progress: {progress:.1f}%",
            font=("Segoe UI", 12),
            text_color="#e5e7eb",
            anchor="w",
        ).pack(
            anchor="w",
            fill="x",
            padx=14,
            pady=(0, 2),
        )

        ctk.CTkLabel(
            row,
            text=f"Speed: {speed}",
            font=("Segoe UI", 12),
            text_color="#e5e7eb",
            anchor="w",
        ).pack(
            anchor="w",
            fill="x",
            padx=14,
            pady=(0, 2),
        )

        ctk.CTkLabel(
            row,
            text=f"ETA: {eta}",
            font=("Segoe UI", 12),
            text_color="#e5e7eb",
            anchor="w",
        ).pack(
            anchor="w",
            fill="x",
            padx=14,
            pady=(0, 2),
        )

        ctk.CTkLabel(
            row,
            text=f"Status: {state}",
            font=("Segoe UI", 12),
            text_color="#4ade80",
            anchor="w",
        ).pack(
            anchor="w",
            fill="x",
            padx=14,
            pady=(0, 6),
        )

        bar = ctk.CTkProgressBar(
            row,
            height=10,
            progress_color="#22c55e",
            fg_color="#2a3038",
        )
        bar.pack(
            fill="x",
            padx=14,
            pady=(0, 12),
        )
        bar.set(max(0.0, min(progress / 100.0, 1.0)))

    def close_window(self):

        self._closed = True

        if self._refresh_after_id is not None:
            try:
                self.after_cancel(self._refresh_after_id)
            except Exception:
                pass
            self._refresh_after_id = None

        self.destroy()
