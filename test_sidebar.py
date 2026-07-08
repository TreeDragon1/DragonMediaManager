import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class TestWindow(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Dragon Sidebar Test")
        self.geometry("1000x700")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = Sidebar(self)
        self.sidebar.grid(row=0, column=0, sticky="ns")

        content = ctk.CTkFrame(self)
        content.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=20,
            pady=20
        )

        label = ctk.CTkLabel(
            content,
            text="🐉 Dragon Dashboard Area",
            font=("Arial", 28, "bold")
        )

        label.pack(expand=True)


if __name__ == "__main__":
    app = TestWindow()
    app.mainloop()