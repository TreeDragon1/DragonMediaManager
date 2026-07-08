import customtkinter as ctk
from gui.dashboard import Dashboard

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


def main():
    app = Dashboard()
    app.mainloop()


if __name__ == "__main__":
    main()