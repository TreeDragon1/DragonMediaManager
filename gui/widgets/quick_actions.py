import customtkinter as ctk

from core.actions import DragonActions


class QuickActionsPanel(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)

        self.actions = DragonActions()

        self.build_ui()

    ############################################################

    def build_ui(self):

        ctk.CTkLabel(
            self,
            text="🐉 Quick Actions",
            font=("Arial", 20, "bold")
        ).pack(anchor="w", padx=15, pady=(15, 10))

        self.status = ctk.CTkLabel(
            self,
            text="Status: Ready",
            text_color="lightgreen"
        )

        self.status.pack(anchor="w", padx=15, pady=(0, 15))

        button_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        button_frame.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 10)
        )

        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)

        buttons = [

            ("💾 Backup Now", self.backup_now),
            ("🎬 Restart Jellyfin", self.restart_jellyfin),

            ("📺 Restart Sonarr", self.restart_sonarr),
            ("🎥 Restart Radarr", self.restart_radarr),

            ("🔍 Restart Prowlarr", self.restart_prowlarr),
            ("💬 Restart Bazarr", self.restart_bazarr),

            ("⬇ Restart qBittorrent", self.restart_qbittorrent),
            ("🎞 Restart Jellyseerr", self.restart_jellyseerr),

            ("🔄 Restart Media Stack", self.restart_stack),
            ("🎬 Scan Jellyfin", self.not_ready),

        ]

        row = 0

        for i in range(0, len(buttons), 2):

            left_text, left_cmd = buttons[i]

            ctk.CTkButton(
                button_frame,
                text=left_text,
                command=left_cmd,
                height=40
            ).grid(
                row=row,
                column=0,
                padx=5,
                pady=5,
                sticky="ew"
            )

            if i + 1 < len(buttons):

                right_text, right_cmd = buttons[i + 1]

                ctk.CTkButton(
                    button_frame,
                    text=right_text,
                    command=right_cmd,
                    height=40
                ).grid(
                    row=row,
                    column=1,
                    padx=5,
                    pady=5,
                    sticky="ew"
                )

            row += 1

    ############################################################

    def update_status(self, success, message):

        if success:

            self.status.configure(
                text=f"✅ {message}",
                text_color="lightgreen"
            )

        else:

            self.status.configure(
                text=f"❌ {message}",
                text_color="red"
            )

    ############################################################

    def restart_jellyfin(self):
        self.update_status(*self.actions.restart_jellyfin())

    def restart_sonarr(self):
        self.update_status(*self.actions.restart_sonarr())

    def restart_radarr(self):
        self.update_status(*self.actions.restart_radarr())

    def restart_prowlarr(self):
        self.update_status(*self.actions.restart_prowlarr())

    def restart_bazarr(self):
        self.update_status(*self.actions.restart_bazarr())

    def restart_qbittorrent(self):
        self.update_status(*self.actions.restart_qbittorrent())

    def restart_jellyseerr(self):
        self.update_status(*self.actions.restart_jellyseerr())

    def restart_stack(self):
        self.update_status(*self.actions.restart_media_stack())

    def backup_now(self):
        self.update_status(*self.actions.backup_now())

    ############################################################

    def not_ready(self):

        self.status.configure(
            text="🚧 Coming Soon",
            text_color="orange"
        )