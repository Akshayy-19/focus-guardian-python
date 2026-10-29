"""Focus Guardian: a beginner-friendly Tkinter study timer."""

import tkinter as tk
from tkinter import messagebox


# Session length in seconds (25 minutes).
SESSION_LENGTH = 25 * 60


class FocusGuardian:
    """Build the interface and manage one countdown at a time."""

    def __init__(self, root):
        self.root = root
        self.root.title("Focus Guardian")
        self.root.geometry("520x650")
        self.root.minsize(520, 600)
        self.root.resizable(True, True)
        self.root.configure(bg="#101827")
        self.is_maximized = False
        self.previous_geometry = "520x650"

        # These values describe the current timer session.
        self.remaining_seconds = SESSION_LENGTH
        self.timer_status = "idle"  # idle, running, or paused
        self.after_id = None        # ID of the one scheduled Tkinter callback
        self.completed_sessions = 0

        self.subject = tk.StringVar(value="Python")
        self.subject.trace_add("write", self.update_subject_display)

        self.build_interface()
        self.update_timer_display()
        self.update_subject_display()

    def build_interface(self):
        """Create and arrange the dashboard widgets."""
        card = tk.Frame(self.root, bg="#1b2738", padx=38, pady=32)
        card.pack(fill="both", expand=True, padx=28, pady=28)

        # Window controls provide minimize and maximize/restore actions.
        window_controls = tk.Frame(card, bg="#1b2738")
        window_controls.pack(fill="x", pady=(0, 5))
        tk.Button(
            window_controls, text="—", command=self.root.iconify,
            bg="#26364b", fg="#f3f6fb", activebackground="#344963",
            activeforeground="#ffffff", font=("Segoe UI", 10, "bold"),
            relief="flat", width=3, cursor="hand2",
        ).pack(side="right", padx=(5, 0))
        self.maximize_button = tk.Button(
            window_controls, text="□", command=self.toggle_maximize,
            bg="#26364b", fg="#f3f6fb", activebackground="#344963",
            activeforeground="#ffffff", font=("Segoe UI", 10, "bold"),
            relief="flat", width=3, cursor="hand2",
        )
        self.maximize_button.pack(side="right")

        tk.Label(
            card, text="FOCUS GUARDIAN", bg="#1b2738", fg="#6ee7b7",
            font=("Segoe UI", 12, "bold"),
        ).pack(pady=(4, 5))

        tk.Label(
            card, text="Stay focused. One session at a time.",
            bg="#1b2738", fg="#bdc8d8", font=("Segoe UI", 11),
        ).pack(pady=(0, 25))

        # Subject selector and a label that reflects the current selection.
        tk.Label(
            card, text="STUDY SUBJECT", bg="#1b2738", fg="#91a2b8",
            font=("Segoe UI", 9, "bold"),
        ).pack(pady=(0, 7))

        subject_menu = tk.OptionMenu(
            card, self.subject, "Python", "Mathematics", "Programming", "Other"
        )
        subject_menu.configure(
            bg="#26364b", fg="#f3f6fb", activebackground="#344963",
            activeforeground="#ffffff", font=("Segoe UI", 11),
            relief="flat", highlightthickness=0, width=18,
        )
        subject_menu["menu"].configure(
            bg="#26364b", fg="#f3f6fb", activebackground="#10b981",
            activeforeground="#101827", font=("Segoe UI", 10),
        )
        subject_menu.pack()

        self.subject_label = tk.Label(
            card, text="Current session: Python", bg="#1b2738",
            fg="#6ee7b7", font=("Segoe UI", 10),
        )
        self.subject_label.pack(pady=(10, 24))

        # The large timer display is updated by update_timer_display().
        self.timer_label = tk.Label(
            card, text="25:00", bg="#1b2738", fg="#f3f6fb",
            font=("Segoe UI", 62, "bold"),
        )
        self.timer_label.pack(pady=(0, 8))

        self.status_label = tk.Label(
            card, text="Ready when you are", bg="#1b2738", fg="#91a2b8",
            font=("Segoe UI", 10),
        )
        self.status_label.pack(pady=(0, 25))

        # Buttons use the same functions for starting and resuming safely.
        buttons = tk.Frame(card, bg="#1b2738")
        buttons.pack(pady=(0, 25))

        self.start_button = tk.Button(
            buttons, text="Start", command=self.start_timer,
            bg="#10b981", fg="#08251e", activebackground="#34d399",
            font=("Segoe UI", 11, "bold"), relief="flat", width=10,
            cursor="hand2", padx=8, pady=10,
        )
        self.start_button.grid(row=0, column=0, padx=5)

        self.pause_button = tk.Button(
            buttons, text="Pause", command=self.pause_or_resume,
            bg="#26364b", fg="#f3f6fb", activebackground="#344963",
            activeforeground="#ffffff", font=("Segoe UI", 11, "bold"),
            relief="flat", width=10, cursor="hand2", padx=8, pady=10,
        )
        self.pause_button.grid(row=0, column=1, padx=5)

        tk.Button(
            buttons, text="Reset", command=self.reset_timer,
            bg="#26364b", fg="#f3f6fb", activebackground="#344963",
            activeforeground="#ffffff", font=("Segoe UI", 11, "bold"),
            relief="flat", width=10, cursor="hand2", padx=8, pady=10,
        ).grid(row=0, column=2, padx=5)

        tk.Frame(card, bg="#344258", height=1).pack(fill="x", pady=(0, 17))

        self.sessions_label = tk.Label(
            card, text="Completed sessions: 0", bg="#1b2738",
            fg="#f3f6fb", font=("Segoe UI", 12, "bold"),
        )
        self.sessions_label.pack(pady=(0, 10))

        tk.Label(
            card, text="Small steps add up. Give this session your best.",
            bg="#1b2738", fg="#91a2b8", font=("Segoe UI", 9),
            wraplength=350,
        ).pack()

    def toggle_maximize(self):
        """Maximize the window, or restore its previous size."""
        if not self.is_maximized:
            self.previous_geometry = self.root.geometry()
            try:
                self.root.state("zoomed")
            except tk.TclError:
                # Fallback for platforms that do not support the zoomed state.
                width = self.root.winfo_screenwidth()
                height = self.root.winfo_screenheight()
                self.root.geometry(f"{width}x{height}+0+0")
            self.is_maximized = True
            self.maximize_button.config(text="❐")
        else:
            try:
                self.root.state("normal")
            except tk.TclError:
                pass
            self.root.geometry(self.previous_geometry)
            self.is_maximized = False
            self.maximize_button.config(text="□")

    def update_subject_display(self, *_):
        """Show the selected subject above the timer."""
        if hasattr(self, "subject_label"):
            self.subject_label.config(text=f"Current session: {self.subject.get()}")

    def update_timer_display(self):
        """Format the remaining seconds as MM:SS."""
        minutes, seconds = divmod(self.remaining_seconds, 60)
        self.timer_label.config(text=f"{minutes:02d}:{seconds:02d}")

    def start_timer(self):
        """Start a fresh timer, or resume it if it was paused."""
        if self.timer_status == "running":
            return  # Do not create a second countdown loop.
        if self.remaining_seconds == 0:
            # A completed timer can be started again without pressing Reset.
            self.remaining_seconds = SESSION_LENGTH
            self.update_timer_display()
        self.timer_status = "running"
        self.status_label.config(text=f"Focusing on {self.subject.get()}…")
        self.pause_button.config(text="Pause")
        self.schedule_tick()

    def schedule_tick(self):
        """Schedule exactly one timer update with Tkinter's after()."""
        if self.timer_status == "running" and self.after_id is None:
            self.after_id = self.root.after(1000, self.update_timer)

    def update_timer(self):
        """Subtract one second, redraw, and schedule the next update."""
        self.after_id = None  # The scheduled callback is now being handled.
        if self.timer_status != "running":
            return

        if self.remaining_seconds > 0:
            self.remaining_seconds -= 1
            self.update_timer_display()

        if self.remaining_seconds == 0:
            self.complete_session()
        else:
            self.schedule_tick()

    def pause_or_resume(self):
        """Pause the current countdown or continue a paused countdown."""
        if self.timer_status == "running":
            self.timer_status = "paused"
            self.cancel_scheduled_tick()
            self.pause_button.config(text="Resume")
            self.status_label.config(text="Paused — take a breath")
        elif self.timer_status == "paused":
            self.start_timer()

    def cancel_scheduled_tick(self):
        """Cancel the pending callback, if one exists."""
        if self.after_id is not None:
            self.root.after_cancel(self.after_id)
            self.after_id = None

    def reset_timer(self):
        """Stop the current session and restore the original 25 minutes."""
        self.cancel_scheduled_tick()
        self.timer_status = "idle"
        self.remaining_seconds = SESSION_LENGTH
        self.update_timer_display()
        self.pause_button.config(text="Pause")
        self.status_label.config(text="Ready when you are")

    def complete_session(self):
        """Record a finished session and notify the user."""
        self.cancel_scheduled_tick()
        self.timer_status = "idle"
        self.completed_sessions += 1
        self.sessions_label.config(
            text=f"Completed sessions: {self.completed_sessions}"
        )
        self.pause_button.config(text="Pause")
        self.status_label.config(text="Session complete — well done!")
        messagebox.showinfo(
            "Focus session complete",
            f"Great job! You completed your focus session for {self.subject.get()}.",
            parent=self.root,
        )


def main():
    """Create the application window and start Tkinter's event loop."""
    root = tk.Tk()
    FocusGuardian(root)
    root.mainloop()


if __name__ == "__main__":
    main()
