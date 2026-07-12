"""
Dragon Media Manager
Build 9.0.3

Downloads Panel
"""

import customtkinter as ctk

from core.dragon_downloads import DragonDownloads


class DownloadsPanel(ctk.CTkFrame):

    REFRESH_MS = 5000

    def __init__(self, master):
        super().__init__(master)

        self.engine = DragonDownloads()

        self.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            self,
            text="📥 Active Downloads",
            font=("Arial", 18, "bold")
        )
        title.grid(
            row=0,
            column=0,
            sticky="w",
            padx=15,
            pady=(15, 10)
        )

        self.status = ctk.CTkLabel(
            self,
            text="✔ No Active Downloads",
            font=("Arial", 16, "bold")
        )
        self.status.grid(
            row=1,
            column=0,
            sticky="w",
            padx=20
        )

        self.message = ctk.CTkLabel(
            self,
            text="Waiting for downloads...",
            text_color="gray"
        )
        self.message.grid(
            row=2,
            column=0,
            sticky="w",
            padx=20,
            pady=(0, 10)
        )

        self.progress = ctk.CTkProgressBar(self)
        self.progress.grid(
            row=3,
            column=0,
            sticky="ew",
            padx=20,
            pady=(0, 15)
        )

        self.progress.set(0)

        self.after(1000, self.refresh_downloads)

    def set_idle(self):
        self.status.configure(
            text="✔ No Active Downloads"
        )

        self.message.configure(
            text="Waiting for downloads..."
        )

        self.progress.set(0)

    def set_offline(self):
        self.status.configure(
            text="❌ qBittorrent Offline"
        )

        self.message.configure(
            text="Unable to connect."
        )

        self.progress.set(0)

    def refresh_downloads(self):

        try:
            data = self.engine.get_downloads()

            if not data["connected"]:
                self.set_offline()

            elif data["active"] == 0:
                self.set_idle()

            else:

                download = data["downloads"][0]

                progress = float(download["progress"])
                speed = int(download["speed"] / 1024)
                eta = int(download["eta"])

                if eta < 0:
                    eta_text = "∞"

                elif eta >= 3600:
                    hours = eta // 3600
                    minutes = (eta % 3600) // 60
                    eta_text = f"{hours}h {minutes}m"

                elif eta >= 60:
                    minutes = eta // 60
                    seconds = eta % 60
                    eta_text = f"{minutes}m {seconds}s"

                else:
                    eta_text = f"{eta}s"

                self.status.configure(
                    text=download["name"]
                )

                self.message.configure(
                    text=f"{progress:.1f}% • {speed} KB/s • ETA {eta_text}"
                )

                self.progress.set(progress / 100)

        except Exception as e:

            self.status.configure(
                text="❌ Download Error"
            )

            self.message.configure(
                text=str(e)
            )

            self.progress.set(0)

        finally:
            self.after(
                self.REFRESH_MS,
                self.refresh_downloads
            )