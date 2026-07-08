import customtkinter as ctk
from core.scanner import LibraryScanner


class Dashboard(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("🐉 Dragon Media Manager")
        self.geometry("1100x700")

        self.build_ui()

    def build_ui(self):

        title = ctk.CTkLabel(
            self,
            text="🐉 Dragon Media Manager",
            font=("Arial", 30, "bold")
        )
        title.pack(pady=(20, 5))

        subtitle = ctk.CTkLabel(
            self,
            text="Organize. Protect. Enjoy.",
            font=("Arial", 16)
        )
        subtitle.pack(pady=(0, 20))

        cards = ctk.CTkFrame(self)
        cards.pack(fill="x", padx=20)

        self.movie_card = self.create_card(cards, "🎬 Movies", "0")
        self.category_card = self.create_card(cards, "📂 Categories", "0")
        self.poster_card = self.create_card(cards, "🖼 Posters", "0")
        self.nfo_card = self.create_card(cards, "📄 NFO Files", "0")

        self.movie_card.grid(row=0, column=0, padx=10, pady=10)
        self.category_card.grid(row=0, column=1, padx=10, pady=10)
        self.poster_card.grid(row=0, column=2, padx=10, pady=10)
        self.nfo_card.grid(row=0, column=3, padx=10, pady=10)

        self.scan_button = ctk.CTkButton(
            self,
            text="🔍 Scan Library",
            width=250,
            command=self.scan_library
        )

        self.scan_button.pack(pady=20)

        self.log = ctk.CTkTextbox(
            self,
            height=250
        )

        self.log.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        self.log.insert("end", "🐉 Dragon Media Manager started...\n")
        self.log.insert("end", "Status: Ready\n")

    def create_card(self, parent, title, value):

        frame = ctk.CTkFrame(
            parent,
            width=220,
            height=120
        )

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

    def scan_library(self):

        self.log.insert(
            "end",
            "\n🔍 Scanning library...\n"
        )

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

        self.log.insert("end", "✅ Scan Complete\n")
        self.log.insert("end", f"🎬 Movies: {stats['movies']}\n")
        self.log.insert("end", f"📂 Categories: {stats['categories']}\n")
        self.log.insert("end", f"🖼 Posters: {stats['posters']}\n")
        self.log.insert("end", f"📄 NFO Files: {stats['nfo']}\n")
        self.log.insert("end", f"💬 Subtitles: {stats['subtitles']}\n")

        self.log.see("end")