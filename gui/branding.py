"""
Dragon Media Manager
Branding helpers
"""

from pathlib import Path

from PIL import Image
import customtkinter as ctk


PROJECT_ROOT = Path(__file__).resolve().parent.parent
ICONS_DIR = PROJECT_ROOT / "assets" / "icons"
DRAGON_ICON = ICONS_DIR / "dragon.png"


def dragon_icon_path(size: int | None = None) -> Path:
    """
    Return the best matching dragon icon path for a given size.
    """

    if size is None:
        return DRAGON_ICON

    preferred = ICONS_DIR / f"dragon_{size}.png"
    if preferred.is_file():
        return preferred

    return DRAGON_ICON


def load_dragon_image(size: int = 48) -> ctk.CTkImage | None:
    """
    Load the dragon branding image for CustomTkinter widgets.
    """

    path = dragon_icon_path()

    if not path.is_file():
        return None

    image = Image.open(path).convert("RGBA")
    return ctk.CTkImage(
        light_image=image,
        dark_image=image,
        size=(size, size),
    )
