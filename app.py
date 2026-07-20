import customtkinter as ctk
from PIL import Image, ImageTk

from gui.branding import DRAGON_ICON
from gui.dashboard import Dashboard

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


def main():
    app = Dashboard()

    try:
        if DRAGON_ICON.is_file():
            icon = ImageTk.PhotoImage(Image.open(DRAGON_ICON).convert("RGBA"))
            app.iconphoto(True, icon)
            app._window_icon = icon
    except Exception:
        pass

    app.mainloop()


if __name__ == "__main__":
    main()
