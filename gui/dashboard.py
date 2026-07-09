"""
Dragon Media Manager
Dashboard

Version: v0.1.3-alpha
Codename: Dragon's Eye
"""

import customtkinter as ctk
from core.scanner import LibraryScanner
from gui.sidebar import Sidebar


class Dashboard(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("🐉 Dragon Media Manager")
        self.geometry("1400x800")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.build_ui()

    def build_ui(self):

        # -----------------------------
        # Sidebar
        # -----------------------------

        self.sidebar = Sidebar(self)
        self.sidebar.grid(row=0, column=0, sticky="ns")

        # -----------------------------
        # Main Content
        # -----------------------------

        main = ctk.CTkFrame(self)
        main.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        title = ctk.CTkLabel(
            main,
            text="🐉 Dragon Media Manager",
            font=("Arial", 30, "bold")
        )
        title.pack(pady=(20, 5))

        subtitle = ctk.CTkLabel(
            main,
            text="Organize. Protect. Enjoy.",
            font=("Arial", 16)
        )
        subtitle.pack(pady=(0, 20))

        stats = ctk.CTkFrame(main)
        stats.pack(fill="x", padx=20)

        self.movie_card = self.create_card(stats, "🎬 Movies", "0")
        self.category_card = self.create_card(stats, "📂 Categories", "0")
        self.poster_card = self.create_card(stats, "🖼 Posters", "0")
        self.nfo_card = self.create_card(stats, "📄 NFO Files", "0")

        self.movie_card.grid(row=0, column=0, padx=10, pady=10)
        self.category_card.grid(row=0, column=1, padx=10, pady=10)
        self.poster_card.grid(row=0, column=2, padx=10, pady=10)
        self.nfo_card.grid(row=0, column=3, padx=10, pady=10)

        self.scan_button = ctk.CTkButton(
            main,
            text="🔍 Scan Library",
            width=250,
            command=self.scan_library
        )
        self.scan_button.pack(pady=20)

        self.log = ctk.CTkTextbox(main, height=250)
        self.log.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.write_log("🐉 Dragon Media Manager started")
        self.write_log("Dragon's Eye Build 2 loaded")

    def create_card(self, parent, title, value):

        frame = ctk.CTkFrame(parent, width=220, height=120)
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

        self.update()

        scanner = LibraryScanner("/media/treedragon/Movies1")
        stats = scanner.scan()

        self.movie_card.value_label.configure(text=str(stats["movies"]))
        self.category_card.value_label.configure(text=str(stats["categories"]))
        self.poster_card.value_label.configure(text=str(stats["posters"]))
        self.nfo_card.value_label.configure(text=str(stats["nfo"]))

        self.write_log("✅ Scan Complete")