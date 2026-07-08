import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class DragonMediaManager(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("🐉 Dragon Media Manager")
        self.geometry("1000x700")

        title = ctk.CTkLabel(
            self,
            text="🐉 Dragon Media Manager",
            font=("Arial", 28, "bold")
        )
        title.pack(pady=20)

        version = ctk.CTkLabel(
            self,
            text="Version 0.1.0-alpha",
            font=("Arial", 16)
        )
        version.pack()

        info = ctk.CTkLabel(
            self,
            text="Welcome to Dragon Media Manager!\n\n"
                 "This is the beginning of your custom media server management application.",
            justify="center"
        )
        info.pack(pady=40)

        scan_button = ctk.CTkButton(
            self,
            text="🔍 Scan Library",
            command=self.scan_library
        )
        scan_button.pack(pady=20)

        self.status = ctk.CTkLabel(
            self,
            text="Status: Ready"
        )
        self.status.pack(side="bottom", pady=20)

    def scan_library(self):
        self.status.configure(text="Status: Scanner coming in Version 0.1.1")


if __name__ == "__main__":
    app = DragonMediaManager()
    app.mainloop()