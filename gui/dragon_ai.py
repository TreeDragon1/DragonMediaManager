"""
Dragon Media Manager
Dragon AI Panel

Version: v0.1.3-alpha
Build 6
"""

import customtkinter as ctk

from core.dragon_ai import DragonAI
from gui.branding import load_dragon_image


class DragonAIFrame(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.configure(corner_radius=12)

        title_row = ctk.CTkFrame(self, fg_color="transparent")
        title_row.pack(anchor="w", fill="x", padx=20, pady=(15, 10))

        dragon_logo = load_dragon_image(28)

        if dragon_logo is not None:
            logo = ctk.CTkLabel(
                title_row,
                text="",
                image=dragon_logo,
            )
            self._ai_dragon_image = dragon_logo
            logo.pack(side="left", padx=(0, 8))

        ctk.CTkLabel(
            title_row,
            text="Dragon AI",
            font=("Arial", 22, "bold")
        ).pack(side="left")

        dragon = DragonAI()
        message = dragon.get_message()

        self.textbox = ctk.CTkTextbox(
            self,
            height=180,
            wrap="word"
        )

        self.textbox.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20)
        )

        self.textbox.insert("1.0", message)
        self.textbox.configure(state="disabled")
