"""
Dragon Media Manager
Dragon Health Panel

Version: v0.1.3-alpha
Build 9.1
"""

import math
import platform
import time
import tkinter as tk

import customtkinter as ctk
import psutil

from core.dragon_health import DragonHealthCore


class DragonHealth(ctk.CTkFrame):

    ACCENT = "#3b82f6"
    GOOD = "#22c55e"
    WARN = "#f59e0b"
    BAD = "#f87171"
    MUTED = "#8f98a3"
    TEXT = "#e5e7eb"
    CARD = "#12151a"
    PANEL = "#1a1d22"
    RING_BG = "#2a3038"

    def __init__(self, master):
        super().__init__(master)

        self.configure(
            corner_radius=15,
            fg_color=self.PANEL,
            border_width=1,
            border_color="#2a3038",
        )

        self.core = DragonHealthCore()
        self.health = self.core.get_health()

        self.build_ui()

    # --------------------------------------------------
    # Build Interface
    # --------------------------------------------------

    def build_ui(self):

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=18, pady=(14, 6))

        ctk.CTkLabel(
            header,
            text="🐉  Dragon Health",
            font=("Segoe UI", 20, "bold"),
            text_color=self.TEXT,
        ).pack(side="left")

        self.body = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            corner_radius=0,
        )
        self.body.pack(
            fill="both",
            expand=True,
            padx=8,
            pady=(0, 4),
        )

        self._build_resources_section()
        self._build_middle_sections()
        self._build_overall_status()

    # --------------------------------------------------
    # System Resources (circular gauges)
    # --------------------------------------------------

    def _build_resources_section(self):

        section = self._section("System Resources")

        gauges = ctk.CTkFrame(section, fg_color="transparent")
        gauges.pack(fill="x", padx=4, pady=(0, 6))

        for column in range(3):
            gauges.grid_columnconfigure(column, weight=1)

        cpu = self.health.get("cpu", {})
        memory = self.health.get("memory", {})
        disk = self.health.get("disk", {})

        self._create_gauge(
            gauges,
            0,
            "CPU Usage",
            self._percent(cpu),
            None,
        )

        self._create_gauge(
            gauges,
            1,
            "Memory Usage",
            self._percent(memory),
            self._format_memory_used(memory),
        )

        self._create_gauge(
            gauges,
            2,
            "Disk Usage",
            self._percent(disk),
            self._format_disk_used(disk),
        )

    def _create_gauge(self, parent, column, title, percent, detail):

        card = ctk.CTkFrame(
            parent,
            fg_color="transparent",
        )
        card.grid(
            row=0,
            column=column,
            sticky="nsew",
            padx=6,
            pady=4,
        )

        size = 108
        canvas = tk.Canvas(
            card,
            width=size,
            height=size,
            bg=self.PANEL,
            highlightthickness=0,
            bd=0,
        )
        canvas.pack()

        if percent is None:
            colour = self.MUTED
            progress = 0.0
            value_text = "N/A"
        else:
            colour = self._usage_colour(percent)
            progress = max(0.0, min(percent / 100.0, 1.0))
            if float(percent).is_integer():
                value_text = f"{int(percent)}%"
            else:
                value_text = f"{percent}%"

        self._draw_ring(canvas, size, progress, colour)

        canvas.create_text(
            size / 2,
            size / 2,
            text=value_text,
            fill=self.TEXT,
            font=("Segoe UI", 16, "bold"),
        )

        ctk.CTkLabel(
            card,
            text=title,
            font=("Segoe UI", 12, "bold"),
            text_color=self.TEXT,
        ).pack(pady=(6, 0))

        if detail:
            ctk.CTkLabel(
                card,
                text=detail,
                font=("Segoe UI", 11),
                text_color=self.MUTED,
            ).pack(pady=(0, 2))

    def _draw_ring(self, canvas, size, progress, colour):

        pad = 10
        width = 10

        canvas.create_oval(
            pad,
            pad,
            size - pad,
            size - pad,
            outline=self.RING_BG,
            width=width,
        )

        if progress <= 0:
            return

        extent = -360 * progress

        canvas.create_arc(
            pad,
            pad,
            size - pad,
            size - pad,
            start=90,
            extent=extent,
            style=tk.ARC,
            outline=colour,
            width=width,
        )

        # Soft end-cap highlight for a cleaner ring look
        angle = math.radians(90 + extent)
        radius = (size / 2) - pad
        cx = size / 2
        cy = size / 2
        x = cx + radius * math.cos(angle)
        y = cy - radius * math.sin(angle)
        canvas.create_oval(
            x - 2,
            y - 2,
            x + 2,
            y + 2,
            fill=colour,
            outline=colour,
        )

    # --------------------------------------------------
    # Services + System Information (side by side)
    # --------------------------------------------------

    def _build_middle_sections(self):

        middle = ctk.CTkFrame(self.body, fg_color="transparent")
        middle.pack(fill="both", expand=True, pady=(4, 4))

        middle.grid_columnconfigure(0, weight=1)
        middle.grid_columnconfigure(1, weight=1)
        middle.grid_rowconfigure(0, weight=1)

        services_panel = ctk.CTkFrame(
            middle,
            fg_color=self.CARD,
            corner_radius=12,
            border_width=1,
            border_color="#2a3038",
        )
        services_panel.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(8, 6),
            pady=4,
        )

        info_panel = ctk.CTkFrame(
            middle,
            fg_color=self.CARD,
            corner_radius=12,
            border_width=1,
            border_color="#2a3038",
        )
        info_panel.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(6, 8),
            pady=4,
        )

        self._build_services_section(services_panel)
        self._build_system_info_section(info_panel)

    def _build_services_section(self, parent):

        ctk.CTkLabel(
            parent,
            text="Services",
            font=("Segoe UI", 14, "bold"),
            text_color=self.TEXT,
        ).pack(anchor="w", padx=14, pady=(12, 8))

        services = self.health.get("services", {})

        if not services:
            self.create_row("Services", "N/A", parent=parent)
            return

        for service, status in services.items():
            self._service_row(
                parent,
                service,
                self._service_display(status),
            )

        ctk.CTkLabel(
            parent,
            text="",
            height=8,
        ).pack()

    def _service_row(self, parent, title, status):

        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", padx=12, pady=3)

        clean_title = (
            str(title)
            .replace("🐳 ", "")
            .replace("🎬 ", "")
            .replace("🎞️ ", "")
            .replace("📺 ", "")
            .replace("🔍 ", "")
            .replace("💬 ", "")
            .replace("⬇️ ", "")
        )

        ctk.CTkLabel(
            row,
            text=clean_title,
            font=("Segoe UI", 13),
            text_color="#c5ccd6",
        ).pack(side="left")

        right = ctk.CTkFrame(row, fg_color="transparent")
        right.pack(side="right")

        if status == "Running":
            dot = "●"
            colour = self.GOOD
        elif status == "Offline":
            dot = "●"
            colour = self.BAD
        else:
            dot = "●"
            colour = self.MUTED
            status = "N/A"

        ctk.CTkLabel(
            right,
            text=f"{dot}  {status}",
            font=("Segoe UI", 13, "bold"),
            text_color=colour,
        ).pack(side="right")

    def _build_system_info_section(self, parent):

        ctk.CTkLabel(
            parent,
            text="System Information",
            font=("Segoe UI", 14, "bold"),
            text_color=self.TEXT,
        ).pack(anchor="w", padx=14, pady=(12, 8))

        memory = self.health.get("memory", {})
        total_memory = (
            memory.get("total_gb") if isinstance(memory, dict) else None
        )

        docker_status = self.health.get("docker")
        if docker_status is None and isinstance(self.health.get("services"), dict):
            docker_status = self.health["services"].get("🐳 Docker")

        info_rows = [
            ("Hostname", self._display(self.health.get("hostname"))),
            ("Uptime", self._get_uptime()),
            ("CPU Model", self._get_cpu_model()),
            (
                "Total Memory",
                f"{total_memory} GB" if total_memory is not None else "N/A",
            ),
            ("OS", self._get_os_name()),
            ("Docker", self._service_display(docker_status)),
            ("Last Updated", self._display(self.health.get("last_updated"))),
        ]

        for title, value in info_rows:
            self.create_row(title, value, parent=parent)

        ctk.CTkLabel(
            parent,
            text="",
            height=8,
        ).pack()

    # --------------------------------------------------
    # Overall Status
    # --------------------------------------------------

    def _build_overall_status(self):

        label, colour = self._overall_indicator()

        if label == "Healthy":
            text = "✓  Overall Status: Healthy"
            fg = self.GOOD
            text_colour = "#04140a"
        elif label == "Good":
            text = "●  Overall Status: Good"
            fg = self.WARN
            text_colour = "#1a1200"
        elif label == "Needs Attention":
            text = "!  Overall Status: Needs Attention"
            fg = self.BAD
            text_colour = "#1a0505"
        else:
            text = "Overall Status: N/A"
            fg = self.RING_BG
            text_colour = self.MUTED

        bar = ctk.CTkFrame(
            self,
            fg_color=fg,
            corner_radius=10,
            height=42,
        )
        bar.pack(fill="x", padx=14, pady=(4, 14))
        bar.pack_propagate(False)

        ctk.CTkLabel(
            bar,
            text=text,
            font=("Segoe UI", 15, "bold"),
            text_color=text_colour,
        ).pack(expand=True)

    def _overall_indicator(self):

        status = str(self.health.get("status", ""))
        score = self.health.get("score", None)

        if "Excellent" in status or (
            isinstance(score, (int, float)) and score >= 90
        ):
            return "Healthy", self.GOOD

        if "Good" in status or (
            isinstance(score, (int, float)) and score >= 70
        ):
            return "Good", self.WARN

        if status and status not in ("", "N/A", "--"):
            return "Needs Attention", self.BAD

        return "N/A", self.MUTED

    # --------------------------------------------------
    # Helpers (public methods preserved)
    # --------------------------------------------------

    def separator(self):

        ctk.CTkLabel(
            self.body if hasattr(self, "body") else self,
            text="─" * 34,
            text_color="#2a3038",
        ).pack(fill="x", padx=12, pady=8)

    def create_row(self, title, value, parent=None):

        container = parent if parent is not None else (
            self.body if hasattr(self, "body") else self
        )

        row = ctk.CTkFrame(
            container,
            fg_color="transparent",
        )

        row.pack(
            fill="x",
            padx=12,
            pady=3,
        )

        ctk.CTkLabel(
            row,
            text=title,
            font=("Segoe UI", 12),
            text_color=self.MUTED,
        ).pack(side="left")

        if isinstance(value, dict):

            if "available_gb" in value:
                value = (
                    f"{value['available_gb']} GB Available "
                    f"({value.get('percent', 'N/A')}%)"
                )

            elif "free_tb" in value:
                value = (
                    f"{value['free_tb']} TB Free "
                    f"({value.get('percent', 'N/A')}%)"
                )

            elif "percent" in value:
                value = f"{value['percent']}%"

            else:
                value = str(value)

        if value is None or value == "" or value == "--":
            value = "N/A"

        value = str(value)

        clean = (
            value.replace("🟢 ", "")
                 .replace("🟡 ", "")
                 .replace("🔴 ", "")
        )

        if "Running" in value or "Online" in value or clean == "Healthy":
            colour = self.GOOD
        elif "Offline" in value or "Needs Attention" in value:
            colour = self.BAD
        elif "Good" in value:
            colour = self.WARN
        elif clean == "N/A":
            colour = self.MUTED
        else:
            colour = self.TEXT

        ctk.CTkLabel(
            row,
            text=clean,
            text_color=colour,
            font=("Segoe UI", 12, "bold"),
        ).pack(side="right")

    # --------------------------------------------------
    # Internal helpers
    # --------------------------------------------------

    def _section(self, title):

        frame = ctk.CTkFrame(
            self.body,
            fg_color="transparent",
        )
        frame.pack(fill="x", pady=(2, 4))

        ctk.CTkLabel(
            frame,
            text=title,
            font=("Segoe UI", 14, "bold"),
            text_color=self.TEXT,
        ).pack(anchor="w", padx=12, pady=(2, 4))

        return frame

    def _percent(self, data):

        if isinstance(data, dict) and "percent" in data:
            try:
                return float(data["percent"])
            except (TypeError, ValueError):
                return None

        if isinstance(data, (int, float)):
            return float(data)

        return None

    def _usage_colour(self, percent):

        if percent < 70:
            return self.GOOD
        if percent < 85:
            return self.WARN
        return self.BAD

    def _display(self, value):

        if value is None or value == "" or value == "--":
            return "N/A"
        return str(value)

    def _service_display(self, status):

        if status is None or status == "" or status == "--":
            return "N/A"

        text = str(status)

        if "Online" in text or "Running" in text:
            return "Running"

        if "Offline" in text:
            return "Offline"

        return self._display(
            text.replace("🟢 ", "")
                .replace("🟡 ", "")
                .replace("🔴 ", "")
        )

    def _format_memory_used(self, memory):

        if not isinstance(memory, dict):
            return "N/A"

        available = memory.get("available_gb")
        total = memory.get("total_gb")

        if total is None:
            return "N/A"

        if available is None:
            return f"{total} GB"

        used = round(max(total - available, 0), 1)
        return f"{used} GB / {total} GB"

    def _format_disk_used(self, disk):

        if not isinstance(disk, dict):
            return self._display(self.health.get("movies"))

        free = disk.get("free_tb")
        total = disk.get("total_tb")

        if total is None:
            return self._display(self.health.get("movies"))

        if free is None:
            return f"{total} TB"

        used = round(max(total - free, 0), 2)
        return f"{used} TB / {total} TB"

    def _get_uptime(self):

        try:
            seconds = int(time.time() - psutil.boot_time())

            if seconds < 0:
                return "N/A"

            days, rem = divmod(seconds, 86400)
            hours, rem = divmod(rem, 3600)
            minutes, _ = divmod(rem, 60)

            if days > 0:
                return f"{days}d {hours}h {minutes}m"

            return f"{hours}h {minutes}m"

        except Exception:
            return "N/A"

    def _get_cpu_model(self):

        try:
            with open("/proc/cpuinfo", "r", encoding="utf-8") as handle:
                for line in handle:
                    if line.startswith("model name"):
                        model = line.split(":", 1)[1].strip()
                        if model:
                            return model
        except Exception:
            pass

        try:
            model = platform.processor()
            if model:
                return model
        except Exception:
            pass

        return "N/A"

    def _get_os_name(self):

        try:
            data = {}

            with open("/etc/os-release", "r", encoding="utf-8") as handle:
                for line in handle:
                    line = line.strip()

                    if not line or "=" not in line:
                        continue

                    key, value = line.split("=", 1)
                    data[key] = value.strip().strip('"')

            pretty = data.get("PRETTY_NAME")
            if pretty:
                return pretty

        except Exception:
            pass

        try:
            system = platform.system()
            release = platform.release()

            if system and release:
                return f"{system} {release}"

            if system:
                return system

        except Exception:
            pass

        return "N/A"
