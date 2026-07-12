"""
Dragon Media Manager
Build 9.0.2 – Dragon Command Center

Widget:
Action Bar

Dragon Development Team
Founder: Peter Boulton
"""

import customtkinter as ctk


class ActionBar(ctk.CTkFrame):
    def __init__(
        self,
        master,
        scan_callback=None,
        refresh_callback=None,
        settings_callback=None,
    ):
        super().__init__(master)

        self.grid_columnconfigure((0, 1, 2), weight=1)

        title = ctk.CTkLabel(
            self,
            text="Quick Actions",
            font=("Arial", 18, "bold"),
        )
        title.grid(
            row=0,
            column=0,
            columnspan=3,
            sticky="w",
            padx=15,
            pady=(10, 5),
        )

        self.scan_button = ctk.CTkButton(
            self,
            text="🔍 Scan Library",
            height=40,
            command=scan_callback,
        )

        self.refresh_button = ctk.CTkButton(
            self,
            text="🔄 Refresh",
            height=40,
            command=refresh_callback,
        )

        self.settings_button = ctk.CTkButton(
            self,
            text="⚙ Settings",
            height=40,
            command=settings_callback,
        )

        self.scan_button.grid(
            row=1,
            column=0,
            padx=10,
            pady=10,
            sticky="ew",
        )

        self.refresh_button.grid(
            row=1,
            column=1,
            padx=10,
            pady=10,
            sticky="ew",
        )

        self.settings_button.grid(
            row=1,
            column=2,
            padx=10,
            pady=10,
            sticky="ew",
        )