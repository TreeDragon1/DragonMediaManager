"""
Dragon Media Manager
Build 9.0.2 - Dragon Command Center

Status Bar

Dragon Development Team
Founder: Peter Boulton
"""

import customtkinter as ctk

from core.version import VERSION_DISPLAY


class StatusBar(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.status_label = ctk.CTkLabel(
            self,
            text="🟢 Ready",
            anchor="w"
        )

        self.scan_label = ctk.CTkLabel(
            self,
            text="Last Scan: Never",
            anchor="center"
        )

        self.download_label = ctk.CTkLabel(
            self,
            text="Downloads: 0",
            anchor="center"
        )

        self.version_label = ctk.CTkLabel(
            self,
            text=VERSION_DISPLAY,
            anchor="e"
        )

        self.status_label.grid(
            row=0,
            column=0,
            padx=10,
            pady=8,
            sticky="w"
        )

        self.scan_label.grid(
            row=0,
            column=1,
            padx=10,
            pady=8
        )

        self.download_label.grid(
            row=0,
            column=2,
            padx=10,
            pady=8
        )

        self.version_label.grid(
            row=0,
            column=3,
            padx=10,
            pady=8,
            sticky="e"
        )

    def set_status(self, text):
        self.status_label.configure(text=text)

    def set_last_scan(self, text):
        self.scan_label.configure(text=f"Last Scan: {text}")

    def set_downloads(self, count):
        self.download_label.configure(
            text=f"Downloads: {count}"
        )