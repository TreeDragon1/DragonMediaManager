"""
Dragon Media Manager
Dashboard

Version: v0.1.3-alpha
Codename: Dragon's Eye
"""

import customtkinter as ctk
from core.scanner import LibraryScanner


class Dashboard(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("🐉 Dragon Media Manager")
        self.geometry("1200x750")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.build_ui()

    def build_ui(self):

        # ------------------------------
        # Header
        # ------------------------------

        header = ctk.CTkFrame(self)
        header.pack(fill="x", padx=20, pady=(20, 10))

        title = ctk.CTkLabel(
            header,
            text="🐉 Dragon Media Manager",
            font=("Arial", 30, "bold")
        )
        title.pack(anchor="w", padx=20, pady=(15, 0))

        subtitle = ctk.CTkLabel(
            header,
            text="Organize. Protect. Enjoy.",
            font=("Arial", 16)
        )
        subtitle.pack(anchor="w", padx=20, pady=(0, 15))

        # ------------------------------
        # Statistics
        # ------------------------------

        stats = ctk.CTkFrame(self)
        stats.pack(fill="x", padx=20)

        self.movie_card = self.create_card(stats, "🎬 Movies", "0")
        self.category_card = self.create_card(stats, "📂 Categories", "0")
        self.poster_card = self.create_card(stats, "🖼 Posters", "0")
        self.nfo_card = self.create_card(stats, "📄 NFO Files", "0")

        self.movie_card.grid(row=0, column=0, padx=10, pady=10)
        self.category_card.grid(row=0, column=1, padx=10, pady=10)
        self.poster_card.grid(row=0, column=2, padx=10, pady=10)
        self.nfo_card.grid(row=0, column=3, padx=10, pady=10)

        # ------------------------------
        # Scan Button
        # ------------------------------

        self.scan_button = ctk.CTkButton(
            self,
            text="🔍 Scan Library",
            width=250,
            height=45,
            command=self.scan_library
        )

        self.scan_button.pack(pady=20)

        # ------------------------------
        # Activity Log
        # ------------------------------

        self.log = ctk.CTkTextbox(self, height=280)

        self.log.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20)
        )

        self.write_log("🐉 Dragon Media Manager started")
        self.write_log("System ready.")

    def create_card(self, parent, title, value):

        frame = ctk.CTkFrame(
            parent,
            width=240,
            height=120
        )

        frame.grid_propagate(False)

        label = ctk.CTkLabel(
            frame,
            text=title,
            font=("Arial", 18, "bold")
        )

        label.pack(pady=(20, 5))

        value_label = ctk.CTkLabel(
            frame,
            text=value,
            font=("Arial", 32)
        )

        value_label.pack()

        frame.value_label = value_label

        return frame

    def write_log(self, message):
        self.log.insert("end", message + "\n")
        self.log.see("end")

    def scan_library(self):

        self.write_log("🔍 Scanning library...")

        self.scan_button.configure(state="disabled")

        self.update()

        scanner = LibraryScanner(
            "/media/treedragon/Movies1"
        )

        stats = scanner.scan()

        self.movie_card.value_label.configure(
            text=str(stats["movies"])
        )

        self.category_card.value_label.configure(
            text=str(stats["categories"])
        )

        self.poster_card.value_label.configure(
            text=str(stats["posters"])
        )

        self.nfo_card.value_label.configure(
            text=str(stats["nfo"])
        )

        self.write_log("✅ Scan complete")
        self.write_log(f"🎬 Movies: {stats['movies']}")
        self.write_log(f"📂 Categories: {stats['categories']}")
        self.write_log(f"🖼 Posters: {stats['posters']}")
        self.write_log(f"📄 NFO Files: {stats['nfo']}")
        self.write_log(f"💬 Subtitles: {stats['subtitles']}")

        self.scan_button.configure(state="normal")