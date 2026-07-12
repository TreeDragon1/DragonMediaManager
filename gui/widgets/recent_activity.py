"""
Dragon Media Manager
Build 9.0.3

Recent Activity Panel
"""

import customtkinter as ctk


class RecentActivity(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            self,
            text="📋 Recent Activity",
            font=("Arial", 18, "bold"),
        )
        title.grid(
            row=0,
            column=0,
            sticky="w",
            padx=15,
            pady=(15, 10),
        )

        self.activity_box = ctk.CTkTextbox(
            self,
            height=170,
        )

        self.activity_box.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=15,
            pady=(0, 15),
        )

        self.activity_box.insert("end", "🐉 Dragon Started\n")
        self.activity_box.insert("end", "❤️ Dragon Health Ready\n")
        self.activity_box.insert("end", "🤖 Dragon AI Ready\n")
        self.activity_box.insert("end", "📥 Downloads Ready\n")

        self.activity_box.configure(state="disabled")

    def add(self, message):

        self.activity_box.configure(state="normal")

        lines = self.activity_box.get("1.0", "end").splitlines()

        lines.append(message)

        lines = lines[-10:]

        self.activity_box.delete("1.0", "end")

        for line in lines:
            self.activity_box.insert("end", line + "\n")

        self.activity_box.see("end")

        self.activity_box.configure(state="disabled")

    def clear(self):

        self.activity_box.configure(state="normal")

        self.activity_box.delete("1.0", "end")

        self.activity_box.configure(state="disabled")