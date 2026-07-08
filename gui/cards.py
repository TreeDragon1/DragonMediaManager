cards.py
import customtkinter as ctk


class InfoCard(ctk.CTkFrame):
    """
    Reusable dashboard card.
    """

    def __init__(
        self,
        master,
        title,
        value="0",
        subtitle="",
        width=220,
        height=140
    ):

        super().__init__(
            master,
            width=width,
            height=height,
            corner_radius=15
        )

        self.grid_propagate(False)

        self.title_label = ctk.CTkLabel(
            self,
            text=title,
            font=("Arial", 18, "bold")
        )

        self.title_label.pack(pady=(15, 5))

        self.value_label = ctk.CTkLabel(
            self,
            text=value,
            font=("Arial", 34, "bold")
        )

        self.value_label.pack()

        self.subtitle_label = ctk.CTkLabel(
            self,
            text=subtitle,
            font=("Arial", 13)
        )

        self.subtitle_label.pack(pady=(5, 10))

    def set_value(self, value):
        """Update the main value."""
        self.value_label.configure(text=str(value))

    def set_subtitle(self, subtitle):
        """Update the subtitle."""
        self.subtitle_label.configure(text=str(subtitle))