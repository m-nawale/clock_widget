import tkinter as tk
import datetime as dt
import zoneinfo

class ClockWidget(tk.Tk):
    TIMEZONES = {
        "UTC": "UTC",
        "Europe/Berlin": "Berlin",
        "Europe/London": "London",
        "Asia/Kolkata": "India (Kolkata)",
        "America/New_York": "New York",
        "America/Los_Angeles": "Los Angeles",
        "Asia/Tokyo": "Tokyo",
        "Asia/Dubai": "Dubai",
        "Australia/Sydney": "Sydney",
        "Africa/Johannesburg": "Johannesburg"
    }

    def __init__(self):
        super().__init__()

        # Set defaults
        self._offset_x = 0
        self._offset_y = 0
        self.timezone = "Europe/Berlin"

        # Window setup
        self.attributes("-topmost", True)
        self.configure(bg="#222222")

        # Container frame
        self.container = tk.Frame(self, bg="#222222")
        self.container.pack()

        # Time label
        self.time_label = tk.Label(
            self.container,
            font=("Helvetica", 16),
            fg="#ffffff",
            bg="#222222",
            padx=10,
            pady=5
        )
        self.time_label.pack()

        # Timezone selector
        self.timezone_var = tk.StringVar()
        self.timezone_var.set(self.timezone)
        self.dropdown = tk.OptionMenu(
            self.container,
            self.timezone_var,
            *self.TIMEZONES.keys(),
            command=self._on_timezone_change
        )
        self.dropdown.config(
            font=("Helvetica", 10),
            bg="#333333",
            fg="#ffffff",
            activebackground="#444444",
            activeforeground="#ffffff",
            highlightthickness=0
        )
        self.dropdown.pack(pady=(5, 0))

        # Bind dragging
        for widget in (self, self.container, self.time_label, self.dropdown):
            widget.bind("<ButtonPress-1>", self._start_move)
            widget.bind("<B1-Motion>", self._on_move)

        # Start clock
        self.update_clock()

        # Delay overrideredirect
        self.after(500, self._apply_overrideredirect)

    def _on_timezone_change(self, selected_timezone):
        self.timezone = selected_timezone
        self.update_clock()

    def update_clock(self):
        tz = zoneinfo.ZoneInfo(self.timezone)
        current_time = dt.datetime.now(tz).strftime("%H:%M:%S")
        self.time_label.config(text=current_time)
        self.after(1000, self.update_clock)

    def _start_move(self, event):
        self._offset_x = event.x
        self._offset_y = event.y

    def _on_move(self, event):
        x = self.winfo_pointerx() - self._offset_x
        y = self.winfo_pointery() - self._offset_y
        self.geometry(f"+{x}+{y}")

    def _apply_overrideredirect(self):
        print("Applying overrideredirect")
        self.overrideredirect(True)
