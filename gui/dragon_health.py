"""
Dragon Media Manager
Dragon Health Panel

Version: v0.1.3-alpha
Build 9.1
"""

import customtkinter as ctk

from core.dragon_health import DragonHealthCore


class DragonHealth(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.configure(corner_radius=12)

        self.health = DragonHealthCore().get_health()

        self.build_ui()

    # --------------------------------------------------
    # Build Interface
    # --------------------------------------------------

    def build_ui(self):

        ctk.CTkLabel(
            self,
            text="🐉 Dragon Health",
            font=("Arial", 22, "bold"),
        ).pack(anchor="w", padx=20, pady=(15, 10))

        #
        # Services
        #

        for service, status in self.health.get("services", {}).items():
            self.create_row(service, status)

        self.separator()

        #
        # System
        #

        cpu = self.health.get("cpu", {})
        memory = self.health.get("memory", {})
        disk = self.health.get("disk", {})

        self.create_row(
            "🖥 CPU Usage",
            f"{cpu.get('percent', '--')}%"
        )

        self.create_row(
            "🧠 Memory",
            f"{memory.get('available_gb', '--')} GB Available ({memory.get('percent', '--')}%)"
        )

        self.create_row(
            "💽 Disk Usage",
            f"{disk.get('free_tb', '--')} TB Free ({disk.get('percent', '--')}%)"
        )

        self.create_row(
            "💾 Movies Drive",
            self.health.get("movies", "--")
        )

        self.separator()

        #
        # Dragon Status
        #

        ctk.CTkLabel(
            self,
            text="Dragon Status",
            font=("Arial", 18, "bold"),
        ).pack()

        status = self.health.get("status", "Unknown")

        if "Excellent" in status:
            colour = "lime green"
        elif "Good" in status:
            colour = "orange"
        else:
            colour = "red"

        ctk.CTkLabel(
            self,
            text=status.replace("🟢 ", "").replace("🟡 ", "").replace("🔴 ", ""),
            text_color=colour,
            font=("Arial", 20, "bold"),
        ).pack(pady=(0, 10))

        ctk.CTkLabel(
            self,
            text=f"Dragon Score: {self.health.get('score', 0)}%",
            font=("Arial", 18, "bold"),
        ).pack()

        self.separator()

        self.create_row(
            "🖥 Hostname",
            self.health.get("hostname", "--")
        )

        self.create_row(
            "🕒 Last Updated",
            self.health.get("last_updated", "--")
        )

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    def separator(self):

        ctk.CTkLabel(
            self,
            text="─" * 34,
        ).pack(fill="x", padx=20, pady=10)

    def create_row(self, title, value):

        row = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )

        row.pack(
            fill="x",
            padx=20,
            pady=4,
        )

        ctk.CTkLabel(
            row,
            text=title,
            font=("Arial", 15),
        ).pack(side="left")

        #
        # Convert dictionaries from Build 9.1
        #

        if isinstance(value, dict):

            if "available_gb" in value:
                value = (
                    f"{value['available_gb']} GB Available "
                    f"({value['percent']}%)"
                )

            elif "free_tb" in value:
                value = (
                    f"{value['free_tb']} TB Free "
                    f"({value['percent']}%)"
                )

            elif "percent" in value:
                value = f"{value['percent']}%"

            else:
                value = str(value)

        value = str(value)

        clean = (
            value.replace("🟢 ", "")
                 .replace("🟡 ", "")
                 .replace("🔴 ", "")
        )

        if "Running" in value or "Online" in value:
            colour = "lime green"
        elif "Offline" in value:
            colour = "red"
        else:
            colour = "orange"

        ctk.CTkLabel(
            row,
            text=clean,
            text_color=colour,
            font=("Arial", 15, "bold"),
        ).pack(side="right")