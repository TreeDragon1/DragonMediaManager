"""
Dragon Media Manager
Central GUI scaling and responsive window helpers.

Scaling is based on available screen resolution and DPI — not physical display size.
"""

from __future__ import annotations

import os
import tkinter as tk
from typing import Literal

import customtkinter as ctk

ScaleMode = Literal["auto", "small", "normal", "large"]

# Reference design resolution (layout target, not a hard-coded window size).
REF_WIDTH = 1920
REF_HEIGHT = 1080

MODE_MULTIPLIERS: dict[str, float] = {
    "small": 0.9,
    "normal": 1.0,
    "large": 1.15,
}

MIN_SCALE = 0.85
MAX_SCALE = 1.25

BASE_MIN_WIDTH = 1100
BASE_MIN_HEIGHT = 680

_current: "UIScale | None" = None


def get_scale_mode() -> ScaleMode:
    mode = os.environ.get("DMM_UI_SCALE", "auto").strip().lower()
    if mode in MODE_MULTIPLIERS:
        return mode  # type: ignore[return-value]
    if mode == "auto":
        return "auto"
    return "auto"


class UIScale:
    """Resolution/DPI-aware scaling helper for the dashboard."""

    def __init__(self, root: tk.Misc | None = None):
        if root is not None:
            self.screen_width = int(root.winfo_screenwidth())
            self.screen_height = int(root.winfo_screenheight())
            self.dpi = float(root.winfo_fpixels("1i"))
        else:
            probe = tk.Tk()
            probe.withdraw()
            self.screen_width = int(probe.winfo_screenwidth())
            self.screen_height = int(probe.winfo_screenheight())
            self.dpi = float(probe.winfo_fpixels("1i"))
            probe.destroy()

        self.mode = get_scale_mode()
        self.factor = self._compute_factor()

    def _compute_factor(self) -> float:
        if self.mode != "auto":
            return max(MIN_SCALE, min(MAX_SCALE, MODE_MULTIPLIERS[self.mode]))

        width_ratio = self.screen_width / REF_WIDTH
        height_ratio = self.screen_height / REF_HEIGHT
        resolution_factor = min(width_ratio, height_ratio)

        dpi_ratio = min(max(self.dpi / 96.0, 1.0), 1.2)
        dpi_adjustment = 1.0 + (dpi_ratio - 1.0) * 0.25

        factor = resolution_factor * dpi_adjustment
        return max(MIN_SCALE, min(MAX_SCALE, factor))

    def px(self, value: float) -> int:
        return max(1, int(round(value * self.factor)))

    def font(self, family: str, size: int, weight: str = "normal"):
        scaled = self.px(size)
        if weight and weight != "normal":
            return (family, scaled, weight)
        return (family, scaled)

    def sidebar_width(self) -> int:
        return max(180, min(240, self.px(200)))

    def content_row_minsize(self) -> int:
        return max(260, self.px(360))

    def gauge_size(self) -> int:
        return max(88, min(128, self.px(108)))

    def initial_geometry(self) -> tuple[int, int]:
        margin = 40
        width = min(
            max(BASE_MIN_WIDTH, int(self.screen_width * 0.95)),
            self.screen_width - margin,
        )
        height = min(
            max(BASE_MIN_HEIGHT, int(self.screen_height * 0.92)),
            self.screen_height - margin,
        )
        return width, height

    def minimum_window_size(self) -> tuple[int, int]:
        width = min(BASE_MIN_WIDTH, int(self.screen_width * 0.92))
        height = min(BASE_MIN_HEIGHT, int(self.screen_height * 0.88))
        return max(960, width), max(600, height)

    def detail_window_size(
        self,
        max_width: int = 900,
        max_height: int = 620,
    ) -> tuple[int, int]:
        width = min(
            max(640, int(self.screen_width * 0.55)),
            max_width,
        )
        height = min(
            max(420, int(self.screen_height * 0.58)),
            max_height,
        )
        return width, height


def init_ui_scale(root: tk.Misc) -> UIScale:
    """Create, register, and apply global CustomTkinter scaling."""
    global _current
    ui = UIScale(root)
    _current = ui
    ctk.set_widget_scaling(ui.factor)
    ctk.set_window_scaling(ui.factor)
    return ui


def get_ui_scale() -> UIScale:
    if _current is None:
        return UIScale()
    return _current


def configure_initial_window(root: tk.Misc, ui: UIScale | None = None) -> UIScale:
    """Apply responsive startup geometry and sensible minimum window size."""
    if ui is None:
        ui = init_ui_scale(root)
    else:
        global _current
        _current = ui
        ctk.set_widget_scaling(ui.factor)
        ctk.set_window_scaling(ui.factor)

    min_w, min_h = ui.minimum_window_size()
    root.minsize(min_w, min_h)

    try:
        root.state("zoomed")
    except tk.TclError:
        width, height = ui.initial_geometry()
        root.geometry(f"{width}x{height}")

    return ui
