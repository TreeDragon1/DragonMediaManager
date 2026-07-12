"""
Dragon Media Manager
Statistics Widget

Version: v0.1.3-alpha
Build 9.1
"""

import customtkinter as ctk


class StatisticCard(ctk.CTkFrame):

    def __init__(self, parent, title, value="0"):
        super().__init__(parent, width=220, height=120)

        self.grid_propagate(False)

        title_label = ctk.CTkLabel(
            self,
            text=title,
            font=("Arial", 18, "bold")
        )

        title_label.pack(pady=(20, 5))

        self.value_label = ctk.CTkLabel(
            self,
            text=value,
            font=("Arial", 32)
        )

        self.value_label.pack()

    def set_value(self, value):
        self.value_label.configure(text=str(value))


class StatisticsWidget(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)

        self.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.movies = StatisticCard(self, "🎬 Movies")
        self.categories = StatisticCard(self, "📂 Categories")
        self.posters = StatisticCard(self, "🖼 Posters")
        self.nfo = StatisticCard(self, "📄 NFO Files")

        self.movies.grid(row=0, column=0, padx=10, pady=10)
        self.categories.grid(row=0, column=1, padx=10, pady=10)
        self.posters.grid(row=0, column=2, padx=10, pady=10)
        self.nfo.grid(row=0, column=3, padx=10, pady=10)

    def update(self, stats):

        self.movies.set_value(stats["movies"])
        self.categories.set_value(stats["categories"])
        self.posters.set_value(stats["posters"])
        self.nfo.set_value(stats["nfo"])