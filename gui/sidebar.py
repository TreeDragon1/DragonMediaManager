sidebar.py
import customtkinter as ctk


class Sidebar(ctk.CTkFrame):
    """
    Left navigation panel for Dragon Media Manager.
    """

    def __init__(self, master):
        super().__init__(
            master,
            width=220,
            corner_radius=0
        )

        self.configure(fg_color="#1F1F1F")

        self.build_sidebar()

    def build_sidebar(self):

        # --------------------------------------------------
        # Logo
        # --------------------------------------------------

        logo = ctk.CTkLabel(
            self,
            text="🐉",
            font=("Arial", 46)
        )

        logo.pack(pady=(20, 0))

        title = ctk.CTkLabel(
            self,
            text="Dragon Media\nManager",
            font=("Arial", 24, "bold"),
            justify="center"
        )

        title.pack(pady=(0, 20))

        # --------------------------------------------------
        # Navigation Buttons
        # --------------------------------------------------

        self.dashboard_btn = self.make_button("🏠 Dashboard")
        self.movies_btn = self.make_button("🎬 Movies")
        self.tv_btn = self.make_button("📺 TV Shows")
        self.downloads_btn = self.make_button("⬇ Downloads")
        self.docker_btn = self.make_button("🐳 Docker")
        self.jellyfin_btn = self.make_button("🎬 Jellyfin")
        self.ai_btn = self.make_button("🤖 Dragon AI")
        self.reports_btn = self.make_button("📊 Reports")
        self.settings_btn = self.make_button("⚙ Settings")
        self.about_btn = self.make_button("ℹ About")

        # --------------------------------------------------
        # Footer
        # --------------------------------------------------

        footer = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        footer.pack(
            side="bottom",
            fill="x",
            pady=20
        )

        version = ctk.CTkLabel(
            footer,
            text="Dragon's Eye\nv0.1.3-alpha",
            font=("Arial", 12)
        )

        version.pack()

    def make_button(self, text):

        button = ctk.CTkButton(
            self,
            text=text,
            width=180,
            height=40,
            corner_radius=10,
            anchor="w"
        )

        button.pack(
            padx=20,
            pady=5
        )

        return button