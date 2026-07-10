"""
Dragon Media Manager
Dragon AI Panel

Version: v0.1.3-alpha
Build 6
"""

import customtkinter as ctk
from core.dragon_ai import DragonAI


class DragonAIFrame(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.configure(corner_radius=12)

        title = ctk.CTkLabel(
            self,
            text="🤖 Dragon AI",
            font=("Arial", 22, "bold")
        )

        title.pack(anchor="w", padx=20, pady=(15, 10))

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