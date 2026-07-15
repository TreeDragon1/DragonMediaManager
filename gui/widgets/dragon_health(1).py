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

        ctk.CTkLabel(
            self,
            text="🐉 Dragon Health",
            font=("Arial", 22, "bold"),
        ).pack(anchor="w", padx=20, pady=(15, 10))

        # -----------------------------
        # Services
        # -----------------------------

        for service, status in self.health.get("services", {}).items():
            self.create_row(service, status)

        self.separator()

        # -----------------------------
        # System
        # -----------------------------

        self.create_row(
            "💾 Movies Drive",
            self.health.get("movies", "--"),
        )

        self.create_row(
            "🧠 Memory",
            self.health.get("memory", "--"),
        )

        self.create_row(
            "🖥 CPU",
            self.health.get("cpu", "--"),
        )

        self.create_row(
            "💽 Disk",
            self.health.get("disk", "--"),
        )

        self.separator()

        status = self.health.get("status", "Unknown")

        if "Excellent" in status:
            colour = "lime green"
        elif "Good" in status:
            colour = "orange"
        else:
            colour = "red"

        ctk.CTkLabel(
            self,
            text="Dragon Status",
            font=("Arial", 18, "bold"),
        ).pack()

        ctk.CTkLabel(
            self,
            text=status.replace("🟢 ", "")
            .replace("🟡 ", "")
            .replace("🔴 ", ""),
            text_color=colour,
            font=("Arial", 20, "bold"),
        ).pack(pady=(0, 10))

        ctk.CTkLabel(
            self,
            text=f"Dragon Score: {self.health.get('score', 0)}%",
            font=("Arial", 18, "bold"),
        ).pack()

        hostname = self.health.get("hostname", "--")
        updated = self.health.get("last_updated", "--")

        ctk.CTkLabel(
            self,
            text=f"Host: {hostname}",
            font=("Arial", 12),
        ).pack(pady=(10, 0))

        ctk.CTkLabel(
            self,
            text=f"Updated: {updated}",
            font=("Arial", 11),
            text_color="gray70",
        ).pack(pady=(0, 15))

    def separator(self):
        ctk.CTkLabel(
            self,
            text="─" * 32,
        ).pack(fill="x", padx=20, pady=10)

    def create_row(self, title, value):
        row = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )
        row.pack(fill="x", padx=20, pady=4)

        ctk.CTkLabel(
            row,
            text=title,
            font=("Arial", 15),
        ).pack(side="left")

        # -----------------------------
        # Convert structured data
        # -----------------------------

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

        if "Online" in value or "Running" in value:
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