import customtkinter as ctk
from customtkinter import CTkLabel
from datetime import datetime, timedelta

# Application settings
FONT_SETTINGS = {
    "default": ("Arial", 12),        # Default font
    "title": ("Arial", 23, "bold"),  # Font for titles
    "countdown": ("Arial", 18),      # Font for countdown
    "units": ("Arial", 18),          # Font for time units
    "footer": ("Arial Bold", 11)     # Font for footer
}

APP_SETTINGS = {
    "title": "Countdown",             # Window title
    "window_size": "599x397",         # Window size
    "resizable": (False, False),      # Resizability of the window
    "appearance_mode": "dark",        # Light/Dark mode
    "color_theme": "blue",            # Theme color
    "refresh_interval": 1000          # Refresh interval in milliseconds
}

FIELD_RANGES = {
    "month": (1, 12),
    "day": (1, 31),
    "hour": (0, 23),
    "minute": (0, 59),
    "second": (0, 59)
}

class CountdownApp:
    def __init__(self, root):
        # Customtkinter settings
        ctk.set_appearance_mode(APP_SETTINGS["appearance_mode"])  # Set light/dark mode
        ctk.set_default_color_theme(APP_SETTINGS["color_theme"])  # Set theme color

        self.root = root
        self.root.title(APP_SETTINGS["title"])
        self.root.geometry(APP_SETTINGS["window_size"])
        self.root.resizable(*APP_SETTINGS["resizable"])

        # Theme colors
        self.set_theme_colors()

        # Main container
        self.main_frame = ctk.CTkFrame(root, fg_color=self.background_color)
        self.main_frame.pack(expand=True, padx=20, pady=20)

        # Current date and time label
        self.current_date_label = ctk.CTkLabel(
            self.main_frame, 
            text="", 
            font=FONT_SETTINGS["title"], 
            text_color=self.text_color
        )
        self.current_date_label.pack(pady=10)

        # Time left or elapsed label
        self.time_left_label = ctk.CTkLabel(
            self.main_frame, 
            text="", 
            font=FONT_SETTINGS["countdown"], 
            text_color=self.text_color
        )
        self.time_left_label.pack(pady=5)

        # Time in different units label
        self.total_time_label = ctk.CTkLabel(
            self.main_frame, 
            text="", 
            font=FONT_SETTINGS["units"], 
            text_color=self.text_color
        )
        self.total_time_label.pack(pady=5)

        ctk.CTkLabel(
            self.main_frame, 
            text="Calculate Date", 
            font=FONT_SETTINGS["title"], 
            text_color=self.highlight_color
        ).pack(pady=10)

        # Default target date: current time + 1 hour
        now = datetime.now() + timedelta(hours=1)

        # Target date input fields
        self.date_frame = ctk.CTkFrame(self.main_frame)
        self.date_frame.pack(pady=10)

        # Create input fields for target date and time
        self.target_year = self.create_target_entry(self.date_frame, now.strftime("%Y"), 0, "Year")
        self.target_month = self.create_target_entry(self.date_frame, now.strftime("%m"), 1, "Month", "month")
        self.target_day = self.create_target_entry(self.date_frame, now.strftime("%d"), 2, "Day", "day")
        self.target_hour = self.create_target_entry(self.date_frame, now.strftime("%H"), 3, "Hour", "hour")
        self.target_minute = self.create_target_entry(self.date_frame, now.strftime("%M"), 4, "Minute", "minute")
        self.target_second = self.create_target_entry(self.date_frame, now.strftime("%S"), 5, "Second", "second")

        # Footer label
        self.version_label = CTkLabel(
            master=self.root, 
            text="By @Nieznany237 | Version 1.3 Released on 18.11.2024 | Initial Release 08.11.2024", 
            text_color="#7E7E7E", 
            anchor="se", 
            justify="right", 
            font=FONT_SETTINGS["footer"]
        )
        self.version_label.pack(side="bottom", anchor="se", padx=0, pady=0)

        # Start time update
        self.update_time()

    def set_theme_colors(self):
        """Set colors based on light/dark mode."""
        if APP_SETTINGS["appearance_mode"] == "dark":
            self.text_color = "#FFFFFF"
            self.background_color = "#2E2E2E"
            self.highlight_color = "#4C9ED9"
        else:
            self.text_color = "#333333"
            self.background_color = "#F0F0F0"
            self.highlight_color = "#007BFF"

    def create_target_entry(self, frame, default_value, column, label_text, field_type=None):
        """Create an input field with validation for the target date and time."""
        entry = ctk.CTkEntry(
            frame, 
            width=58, 
            font=FONT_SETTINGS["units"], 
            justify="center",
            validate="key",
            validatecommand=(self.root.register(lambda val: self.validate_range(val, field_type)), '%P')
        )
        entry.insert(0, default_value)
        entry.grid(row=0, column=column, padx=5)
        ctk.CTkLabel(frame, text=label_text, font=FONT_SETTINGS["units"]).grid(row=1, column=column)
        return entry

    def validate_range(self, value, field_type):
        """Validate the range of input values."""
        if not value.isdigit() and value != "":
            return False
        if field_type and value:
            min_val, max_val = FIELD_RANGES.get(field_type, (0, 9999))
            return min_val <= int(value) <= max_val
        return True

    def update_time(self):
        now = datetime.now()
        self.current_date_label.configure(text=f"Current Date: {now.strftime('%d.%m.%Y %H:%M:%S')}")

        try:
            target_date = datetime(
                int(self.target_year.get()), 
                int(self.target_month.get()), 
                int(self.target_day.get()), 
                int(self.target_hour.get()), 
                int(self.target_minute.get()), 
                int(self.target_second.get())
            )
            time_difference = target_date - now
            seconds_difference = int(time_difference.total_seconds())

            if seconds_difference >= 0:
                self.display_time_remaining(time_difference, seconds_difference)
            else:
                self.display_time_elapsed(time_difference)

        except ValueError:
            self.time_left_label.configure(text="Invalid Date or Time")
            self.total_time_label.configure(text="")

        self.root.after(APP_SETTINGS["refresh_interval"], self.update_time)

    def display_time_remaining(self, time_difference, seconds_difference):
        """Calculate and display remaining time."""
        total_days = time_difference.days
        years, days_remaining = divmod(total_days, 365)
        weeks, days = divmod(days_remaining, 7)
        hours, remainder = divmod(time_difference.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        self.time_left_label.configure(
            text=f"Remaining: {years} years, {weeks} weeks, {days} days, "
                 f"{hours} hours, {minutes} minutes, {seconds} seconds"
        )
        self.total_time_label.configure(
            text=f"Total Years: {total_days // 365}\n"
                 f"Total Weeks: {total_days // 7}\n"
                 f"Total Days: {total_days}\n"
                 f"Total Hours: {seconds_difference // 3600}\n"
                 f"Total Minutes: {seconds_difference // 60}\n"
                 f"Total Seconds: {seconds_difference}"
        )

    def display_time_elapsed(self, time_difference):
        """Calculate and display elapsed time."""
        abs_time_difference = abs(time_difference)
        total_days = abs_time_difference.days
        years, days_remaining = divmod(total_days, 365)
        weeks, days = divmod(days_remaining, 7)
        hours, remainder = divmod(abs_time_difference.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        self.time_left_label.configure(
            text=f"Elapsed: {years} years, {weeks} weeks, {days} days, "
                 f"{hours} hours, {minutes} minutes, {seconds} seconds"
        )
        self.total_time_label.configure(
            text=f"Total Elapsed Years: {total_days // 365}\n"
                 f"Total Elapsed Weeks: {total_days // 7}\n"
                 f"Total Elapsed Days: {total_days}\n"
                 f"Total Elapsed Hours: {int(abs_time_difference.total_seconds()) // 3600}\n"
                 f"Total Elapsed Minutes: {int(abs_time_difference.total_seconds()) // 60}\n"
                 f"Total Elapsed Seconds: {int(abs_time_difference.total_seconds())}"
        )


# Run the application
root = ctk.CTk()
app = CountdownApp(root)
root.mainloop()
