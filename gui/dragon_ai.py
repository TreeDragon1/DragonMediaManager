"""
Dragon Media Manager
Dragon AI Panel — troubleshooting and recovery presentation.
"""

import threading

import customtkinter as ctk

from core.dragon_ai import DragonAI
from core.dragon_ai_config import CHECK_INTERVAL_SECONDS
from core.version import APP_NAME
from gui.branding import load_dragon_image


class DragonAIFrame(ctk.CTkFrame):

    CHECK_INTERVAL_MS = CHECK_INTERVAL_SECONDS * 1000

    TEXT = "#e5e7eb"
    MUTED = "#8f98a3"
    GOOD = "#4ade80"
    WARN = "#f59e0b"
    BAD = "#f87171"
    PANEL = "#1a1d22"

    def __init__(self, master):
        super().__init__(master)

        self.configure(
            corner_radius=15,
            fg_color=self.PANEL,
            border_width=1,
            border_color="#2a3038",
        )

        self.core = DragonAI()
        self._after_id = None
        self._cycle_in_progress = False
        self._closed = False

        self._build_ui()
        self._schedule_cycle(initial=True)

        self.bind("<Destroy>", self._on_destroy, add="+")

    def _build_ui(self):

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=18, pady=(14, 8))

        title_row = ctk.CTkFrame(header, fg_color="transparent")
        title_row.pack(fill="x")

        dragon_logo = load_dragon_image(28)

        if dragon_logo is not None:
            logo = ctk.CTkLabel(
                title_row,
                text="",
                image=dragon_logo,
            )
            self._ai_dragon_image = dragon_logo
            logo.pack(side="left", padx=(0, 8))

        ctk.CTkLabel(
            title_row,
            text="Dragon AI",
            font=("Segoe UI", 20, "bold"),
            text_color=self.TEXT,
        ).pack(side="left")

        voice_controls = ctk.CTkFrame(title_row, fg_color="transparent")
        voice_controls.pack(side="right")

        self.voice_button = ctk.CTkButton(
            voice_controls,
            text=self._voice_button_text(),
            width=110,
            height=28,
            font=("Segoe UI", 11),
            command=self._toggle_voice,
        )
        self.voice_button.pack(side="left", padx=(0, 6))

        self.speak_status_button = ctk.CTkButton(
            voice_controls,
            text="Speak Status",
            width=110,
            height=28,
            font=("Segoe UI", 11),
            command=self._speak_status,
        )
        self.speak_status_button.pack(side="left")

        self.body = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            corner_radius=0,
        )
        self.body.pack(
            fill="both",
            expand=True,
            padx=12,
            pady=(0, 12),
        )

        self.headline_label = ctk.CTkLabel(
            self.body,
            text="SYSTEM PROTECTION",
            font=("Segoe UI", 13, "bold"),
            text_color=self.MUTED,
            anchor="w",
            justify="left",
        )
        self.headline_label.pack(anchor="w", fill="x", padx=6, pady=(4, 2))

        self.status_label = ctk.CTkLabel(
            self.body,
            text="● All systems healthy",
            font=("Segoe UI", 15, "bold"),
            text_color=self.GOOD,
            anchor="w",
            justify="left",
        )
        self.status_label.pack(anchor="w", fill="x", padx=6, pady=(0, 8))

        self.message_label = ctk.CTkLabel(
            self.body,
            text="No problems detected.",
            font=("Segoe UI", 13),
            text_color=self.TEXT,
            anchor="w",
            justify="left",
            wraplength=520,
        )
        self.message_label.pack(anchor="w", fill="x", padx=6, pady=(0, 10))

        self.meta_frame = ctk.CTkFrame(self.body, fg_color="transparent")
        self.meta_frame.pack(anchor="w", fill="x", padx=6, pady=(0, 8))

        self.recovery_label = ctk.CTkLabel(
            self.meta_frame,
            text="Automatic Recovery: ON",
            font=("Segoe UI", 12),
            text_color=self.MUTED,
            anchor="w",
        )
        self.recovery_label.grid(row=0, column=0, sticky="w", pady=2)

        self.storage_label = ctk.CTkLabel(
            self.meta_frame,
            text="Storage Monitoring: ON",
            font=("Segoe UI", 12),
            text_color=self.MUTED,
            anchor="w",
        )
        self.storage_label.grid(row=1, column=0, sticky="w", pady=2)

        self.check_label = ctk.CTkLabel(
            self.meta_frame,
            text="Last Check: Starting...",
            font=("Segoe UI", 12),
            text_color=self.MUTED,
            anchor="w",
        )
        self.check_label.grid(row=2, column=0, sticky="w", pady=2)

        self.repair_label = ctk.CTkLabel(
            self.meta_frame,
            text="Last Repair: None required",
            font=("Segoe UI", 12),
            text_color=self.MUTED,
            anchor="w",
        )
        self.repair_label.grid(row=3, column=0, sticky="w", pady=2)

        self.history_title = ctk.CTkLabel(
            self.body,
            text="Recent Events",
            font=("Segoe UI", 12, "bold"),
            text_color=self.MUTED,
            anchor="w",
        )

        self.history_frame = ctk.CTkFrame(
            self.body,
            fg_color="#15181d",
            corner_radius=10,
            border_width=1,
            border_color="#2a3038",
        )

        self._history_labels: list[ctk.CTkLabel] = []

        self._apply_state(self.core.state)

    def _schedule_cycle(self, initial=False):

        if self._closed:
            return

        if self._after_id is not None:
            try:
                self.after_cancel(self._after_id)
            except Exception:
                pass
            self._after_id = None

        delay = 250 if initial else self.CHECK_INTERVAL_MS
        self._after_id = self.after(delay, self._run_cycle)

    def _run_cycle(self):

        if self._closed:
            return

        self._after_id = None

        if self._cycle_in_progress:
            self._schedule_cycle()
            return

        self._cycle_in_progress = True

        def worker():

            try:
                state = self.core.run_cycle()
            except Exception as error:
                from core.dragon_ai import DragonAIState

                state = DragonAIState(
                    mode="error",
                    headline="SYSTEM PROTECTION",
                    status_line="● Dragon AI monitoring paused",
                    message=(
                        "Dragon AI encountered an internal error but "
                        f"{APP_NAME} remains operational."
                    ),
                    last_check="Error",
                    error=str(error),
                )

            if self._closed:
                return

            self.after(0, lambda: self._finish_cycle(state))

        threading.Thread(target=worker, daemon=True).start()

    def _finish_cycle(self, state):

        self._cycle_in_progress = False

        try:
            self._apply_state(state)
        except Exception:
            pass

        self._schedule_cycle()

    def _apply_state(self, state):

        # Keep the approved SYSTEM PROTECTION headline style.
        headline_color = self.MUTED
        status_color = self.GOOD

        if state.mode == "recovery":
            status_color = (
                self.GOOD
                if state.active_recovery and state.active_recovery.get("resolved")
                else self.BAD
            )
        elif state.mode == "attention":
            status_color = self.BAD
        elif state.mode == "error":
            status_color = self.WARN

        self.headline_label.configure(
            text=state.headline or "SYSTEM PROTECTION",
            text_color=headline_color,
        )
        self.status_label.configure(
            text=state.status_line,
            text_color=status_color,
        )
        self.message_label.configure(text=state.message)
        self.recovery_label.configure(
            text=f"Automatic Recovery: {state.automatic_recovery}"
        )
        self.storage_label.configure(
            text=f"Storage Monitoring: {state.storage_monitoring}"
        )
        self.check_label.configure(
            text=f"Last Check: {state.last_check}"
        )
        self.repair_label.configure(
            text=f"Last Repair: {state.last_repair}"
        )

        self._render_history(state.history)

    def _render_history(self, history):

        if not history:
            self.history_title.pack_forget()
            self.history_frame.pack_forget()
            return

        self.history_title.pack(anchor="w", fill="x", padx=6, pady=(8, 4))
        self.history_frame.pack(fill="x", padx=6, pady=(0, 6))

        for label in self._history_labels:
            try:
                label.destroy()
            except Exception:
                pass

        self._history_labels.clear()

        for entry in reversed(history[-5:]):
            outcome = str(entry.get("outcome", ""))
            color = self.MUTED

            if outcome == "RESOLVED":
                color = self.GOOD
            elif outcome in (
                "ATTENTION REQUIRED",
                "RECOVERY FAILED",
                "CRITICAL",
                "EMERGENCY",
                "WARNING",
            ):
                color = (
                    self.BAD
                    if outcome in ("ATTENTION REQUIRED", "RECOVERY FAILED", "EMERGENCY")
                    else self.WARN
                )

            text = (
                f"{entry.get('timestamp', '--')}\n"
                f"{entry.get('problem', '')}\n"
                f"{entry.get('action', '')}\n"
                f"{entry.get('result', '')}\n"
                f"{outcome}"
            )

            label = ctk.CTkLabel(
                self.history_frame,
                text=text,
                font=("Segoe UI", 11),
                text_color=color,
                anchor="w",
                justify="left",
                wraplength=500,
            )
            label.pack(anchor="w", fill="x", padx=12, pady=8)
            self._history_labels.append(label)

    def _voice_button_text(self) -> str:

        if self.core.voice.enabled:
            return "🔊 Voice: ON"
        return "🔇 Voice: OFF"

    def _toggle_voice(self):

        try:
            self.core.voice.toggle()
            self.voice_button.configure(text=self._voice_button_text())
        except Exception:
            pass

    def _speak_status(self):

        try:
            from core.dragon_voice import build_status_summary

            summary = build_status_summary(self.core.state)
            self.core.voice.speak_status_summary(summary)
        except Exception:
            pass

    def _on_destroy(self, _event=None):

        self._closed = True

        if self._after_id is not None:
            try:
                self.after_cancel(self._after_id)
            except Exception:
                pass
            self._after_id = None

        try:
            self.core.shutdown()
        except Exception:
            pass
