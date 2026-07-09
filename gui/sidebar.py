"""
Dragon Media Manager
Sidebar

Version: v0.1.3-alpha
Codename: Dragon's Eye
"""

import customtkinter as ctk


class Sidebar(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, width=220)

        self.configure(fg_color="#202225")
        self.pack_propagate(False)

        # Logo
        logo = ctk.CTkLabel(
            self,
            text="🐉",
            font=("Arial", 46)
        )
        logo.pack(pady=(20, 5))

        # Title
        title = ctk.CTkLabel(
            self,
            text="Dragon Media\nManager",
            font=("Arial", 20, "bold"),
            justify="center"
        )
        title.pack(pady=(0, 20))

        # Navigation buttons
        self.make_button("🏠 Dashboard")
        self.make_button("🎬 Movies")
        self.make_button("📺 TV Shows")
        self.make_button("⚙ Settings")

        # Version
        version = ctk.CTkLabel(
            self,
            text="v0.1.3-alpha",
            font=("Arial", 12)
        )
        version.pack(side="bottom", pady=20)

    def make_button(self, text):
        button = ctk.CTkButton(
            self,
            text=text,
            width=180,
            height=40
        )

        button.pack(pady=6, padx=20)