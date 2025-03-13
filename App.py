'''
Version 1.5b as of 26.02.2025

Patch A
- Added singular and plural variety system in texts for Polish language (It also supports English!). (function: pluralize_unit)
- Set the Main Frame of the application statically (self.main_frame)

Patch B
- Added application icon
-- Icon colors dependent on app theme
- Slightly modified some UI elements
- Added UI scaling (ui_scaling). Note: height may behave unexpectedly; I will fix it later.
'''

import customtkinter as ctk
from datetime import datetime, timedelta
from PIL import Image, ImageTk
import os

# Application settings

ui_scaling = 1

FONT_SETTINGS = {
    "default": ("Arial", int(12 * ui_scaling )),
    "title": ("Arial", int(23 * ui_scaling ), "bold"),
    "countdown": ("Arial", int(18 * ui_scaling )),
    "units": ("Arial", int(18 * ui_scaling )),
    "footer": ("Arial Bold", int(11 * ui_scaling ), "italic"),
}

# Determine the initial window size
window_width = 740
window_height = 415

# UI scaling
scaled_width = int(window_width * ui_scaling )
scaled_height = int(window_height * ui_scaling )

APP_SETTINGS = {
    "title": "Countdown",
    "window_size": f"{scaled_width}x{scaled_height}",
    "SetIcon": True,
    "resizable": (False, False),
    "appearance_mode": "dark", # dark, light, system
    "color_theme": "blue",
    "refresh_interval": 1000,
}

FIELD_RANGES = {
    "month": (1, 12),
    "day": (1, 31),
    "hour": (0, 23),
    "minute": (0, 59),
    "second": (0, 59),
}

def set_window_icon(app):
    # Determine what the current application theme is
    appearance_mode = ctk.get_appearance_mode()
    
    # Selecting the appropriate icon by theme
    if appearance_mode == "Dark":
        icon_path = "Assets/Countdown/Icons/white_icon1.png"
    else:
        icon_path = "Assets/Countdown/Icons/dark_icon1.png"
    
    # Flag to check if the icon has been loaded
    icon_loaded = False
    
    # Checking if the icon file exists
    if os.path.exists(icon_path):
        try:
            icon_image = Image.open(icon_path)
            icon_photo = ImageTk.PhotoImage(icon_image)
            app.root.iconphoto(False, icon_photo)  # Setting the icon on the main window
            icon_loaded = True
        except Exception as e:
            print(f"[ERROR] Failed to load icon: {e}")
    else:
        print(f"[WARNING] File {icon_path} not found.")
    
    # Set icon only if loaded correctly
    if icon_loaded:
        app.root.wm_iconbitmap()

def pluralize_unit(value, unit_singular, unit_plural, unit_genitive_plural):
    if value == 1:
        return f"{value} {unit_singular}"
    elif 2 <= value <= 4:
        return f"{value} {unit_plural}"
    else:
        return f"{value} {unit_genitive_plural}"

def generate_time_texts(years, months, weeks, days, hours, minutes, seconds):
    return (
        pluralize_unit(years, "year", "years", "years"),
        pluralize_unit(months, "month", "months", "months"),
        pluralize_unit(weeks, "week", "weeks", "weeks"),
        pluralize_unit(days, "day", "days", "days"),
        pluralize_unit(hours, "hour", "hours", "hours"),
        pluralize_unit(minutes, "minute", "minutes", "minutes"),
        pluralize_unit(seconds, "second", "seconds", "seconds")
    )



class CountdownApp:
    def __init__(self, root):
        ctk.set_appearance_mode(APP_SETTINGS["appearance_mode"])
        ctk.set_default_color_theme(APP_SETTINGS["color_theme"])

        self.root = root
        self.root.title(APP_SETTINGS["title"])
        self.root.geometry(APP_SETTINGS["window_size"])
        self.root.resizable(*APP_SETTINGS["resizable"])

        self.set_theme_colors()
        
        if APP_SETTINGS["SetIcon"]:
            set_window_icon(self)

        self.main_frame = ctk.CTkFrame(
            root, 
            width=695 * ui_scaling, 
            height=370 * ui_scaling, 
            fg_color=self.background_color, 
            border_width=1,  # Width of the main frame border
            #border_color="red"  # Border color  #Alternative --> #B0B0B0
        )
        self.main_frame.pack_propagate(False)
        self.main_frame.pack(padx=20, pady=15)

        self.current_date_label = ctk.CTkLabel(
            self.main_frame, 
            text="", 
            font=FONT_SETTINGS["title"],
            text_color=self.text_color
        )
        self.current_date_label.pack(pady=10)

        self.time_left_label = ctk.CTkLabel(
            self.main_frame, 
            text="", 
            font=FONT_SETTINGS["countdown"],
            text_color=self.text_color
        )
        self.time_left_label.pack(padx=5, pady=5)

        self.total_time_label = ctk.CTkLabel(
            self.main_frame, 
            text="", 
            font=FONT_SETTINGS["units"],
            text_color=self.text_color
        )
        self.total_time_label.pack(pady=5)

        now = datetime.now() + timedelta(hours=1)

        self.date_frame = ctk.CTkFrame(self.main_frame)
        self.date_frame.pack(side="bottom", pady=10, anchor="s")

        ctk.CTkLabel(
            self.main_frame, 
            text="Calculate Date",
            font=FONT_SETTINGS["title"],
            text_color=self.highlight_color
        ).pack(pady=10, side="bottom", anchor="s")


        self.target_year = self.create_target_entry(self.date_frame, now.strftime("%Y"), 0, "Year")
        self.target_month = self.create_target_entry(self.date_frame, now.strftime("%m"), 1, "Month", "month")
        self.target_day = self.create_target_entry(self.date_frame, now.strftime("%d"), 2, "Day", "day")
        self.target_hour = self.create_target_entry(self.date_frame, now.strftime("%H"), 3, "Hour", "hour")
        self.target_minute = self.create_target_entry(self.date_frame, now.strftime("%M"), 4, "Minute", "minute")
        self.target_second = self.create_target_entry(self.date_frame, now.strftime("%S"), 5, "Second", "second")

        self.version_label = ctk.CTkLabel(
            master=self.root, 
            text="Author: @Nieznany237 | Version 1.5b released 26.02.2025 | First release 08.11.2024", 
            text_color="#7E7E7E", 
            anchor="se", 
            justify="right", 
            font=FONT_SETTINGS["footer"]
        )
        self.version_label.pack(side="bottom", anchor="se", padx=0, pady=0)

        self.update_time()

        # ==============================================================================
        # Print current font sizes, DEBUG
        print("====================================================================")
        print(f"UI scalling: {ui_scaling}")
        for style, settings in FONT_SETTINGS.items():
            font_name = settings[0]
            font_size = settings[1]
            if len(settings) == 3:
                font_weight = settings[2]
                print(f"Font: {font_name}, Size: {font_size}, Weight: {font_weight} ({style})")
            else:
                print(f"Font: {font_name}, Size: {font_size} ({style})")
        print(f"App:        Width: {self.root.winfo_width()}, Height: {self.root.winfo_height()}")
        print(f"Main Frame: Width: {self.main_frame.winfo_width()}, Height: {self.main_frame.winfo_height()}")
        # ==============================================================================

    def set_theme_colors(self):
        if APP_SETTINGS["appearance_mode"] == "dark":
            self.text_color = "#FFFFFF"
            self.background_color = "#2E2E2E"
            self.highlight_color = "#db143c" #LEGACY blue #4C9ED9
        else:
            self.text_color = "#333333"
            self.background_color = "#F0F0F0"
            self.highlight_color = "#E60000" #LEGACY blue #007BFF

    def create_target_entry(self, frame, default_value, column, label_text, field_type=None):
        entry = ctk.CTkEntry(
            frame, 
            width=58*ui_scaling , 
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
        total_days = time_difference.days
        years, days_remaining = divmod(total_days, 365)
        months, days = divmod(days_remaining, 30)
        weeks, days = divmod(days, 7)
        hours, remainder = divmod(time_difference.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        year_text, months_text, weeks_text, days_text, hours_text, minutes_text, seconds_text = generate_time_texts(
            years, months, weeks, days, hours, minutes, seconds
        )

        self.time_left_label.configure(
            text=f"Remaining: {year_text}, {months_text}, {weeks_text}, {days_text}, {hours_text}, {minutes_text} and {seconds_text}"
        )

        self.total_time_label.configure(
            text=f"Total Years: {total_days // 365}\n"
                f"Total Months: {total_days // 30}\n"
                f"Total Weeks: {total_days // 7}\n"
                f"Total Days: {total_days}\n"
                f"Total Hours: {seconds_difference // 3600}\n"
                f"Total Minutes: {seconds_difference // 60}\n"
                f"Total Seconds: {seconds_difference}"
        )

    def display_time_elapsed(self, time_difference):
        abs_time_difference = abs(time_difference)
        total_days = abs_time_difference.days
        years, days_remaining = divmod(total_days, 365)
        months, days = divmod(days_remaining, 30)
        weeks, days = divmod(days, 7)
        hours, remainder = divmod(abs_time_difference.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        year_text, months_text, weeks_text, days_text, hours_text, minutes_text, seconds_text = generate_time_texts(
            years, months, weeks, days, hours, minutes, seconds
        )

        self.time_left_label.configure(
            text=f"Elapsed: {year_text}, {months_text}, {weeks_text}, {days_text}, {hours_text}, {minutes_text} and {seconds_text}"
        )

        self.total_time_label.configure(
            text=f"Total Elapsed Years: {total_days // 365}\n"
                f"Total Elapsed Months: {total_days // 30}\n"
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
