import customtkinter as ctk
from datetime import datetime, timedelta
from PIL import Image, ImageTk
import os
import json
from dateutil.relativedelta import relativedelta
#from tkinter import messagebox

# Default application settings
FONT_SETTINGS = {
    "default": ("Arial", 12),
    "title": ("Arial", 23, "bold"),
    "countdown": ("Arial", 18),
    "units": ("Arial", 18),
    "footer": ("Arial", 11, "italic"),
}

APP_SETTINGS = {
    "title": "Countdown",
    "window_size": "735x410",
    "SetIcon": True,
    "resizable": (False, False),
    "appearance_mode": "system",
    "color_theme": "blue",
    "ui_zoom_factor": 1.075,
    "refresh_interval": 1000
}

COLOR_SETTINGS = {
    "dark": {
        "text_color": "#FFFFFF",
        "background_color": "#2E2E2E",
        "highlight_color": "#db143c",
    },
    "light": {
        "text_color": "#333333",
        "background_color": "#F0F0F0",
        "highlight_color": "#E60000",
    }
}

FIELD_RANGES = {
    "year": (0,9999),
    "month": (1, 12),
    "day": (1, 31),
    "hour": (0, 23),
    "minute": (0, 59),
    "second": (0, 59),
}

# Function to convert lists to tuples for fonts
def convert_font_lists_to_tuples(font_settings):
    for key, value in font_settings.items():
        if isinstance(value, list):
            font_settings[key] = tuple(value)
    return font_settings

# Function to load settings from a JSON file
def load_settings_from_json(file_path):
    """
    Function: load_settings_from_json(file_path)
    Loads application settings from a JSON file into global variables.

    Args:
        file_path: Path to JSON settings file [r"Assets/Countdown/settingsV2.json"]

    Behavior:
    - Validates JSON version
    - Loads three setting categories:
    - FONT_SETTINGS (converted to tuples)
    - APP_SETTINGS (merged with existing)
    - COLOR_SETTINGS (merged with existing)
    - Falls back to default settings on errors

    Error Handling:
    - Version mismatch (unless IGNORE_VERSION_ERROR=True)
    - Missing file
    - JSON decode errors
    - Other unexpected errors

    Globals Modified:
    - FONT_SETTINGS
    - APP_SETTINGS 
    - COLOR_SETTINGS
    """
    global FONT_SETTINGS, APP_SETTINGS, COLOR_SETTINGS
    
    # JSON version required - if the version in the file is lower, the settings will not be loaded
    REQUIRED_JSON_VERSION = 1
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            settings = json.load(f)
        
        # Check the JSON version
        if "VERSION" in settings:
            json_version = settings["VERSION"]
            if json_version < REQUIRED_JSON_VERSION:
                if "IGNORE_VERSION_ERROR" in settings and settings["IGNORE_VERSION_ERROR"]:
                    print(f"[WARNING]: The JSON version ({json_version}) is lower than the required version ({REQUIRED_JSON_VERSION}), but the error is ignored. The settings will not be loaded.")
                else:
                    print(f"[ERROR]: JSON version ({json_version}) is lower than required ({REQUIRED_JSON_VERSION}). Default settings will be applied.")
                    #messagebox.showerror("Error", f"[ERROR]: JSON version ({json_version}) is lower than required ({REQUIRED_JSON_VERSION}). Default settings will be applied.")
                return
        else:
            print("[WARNING]: JSON version information missing. Default settings will be applied.")
            return
        
        # Load font settings (convert lists to tuples for immutability)
        if "FONT_SETTINGS" in settings:
            FONT_SETTINGS = convert_font_lists_to_tuples(settings["FONT_SETTINGS"])

        # Merge application settings with existing ones
        if "APP_SETTINGS" in settings:
            APP_SETTINGS.update(settings["APP_SETTINGS"])

        # Merge color settings with existing ones
        if "COLOR_SETTINGS" in settings:
            COLOR_SETTINGS.update(settings["COLOR_SETTINGS"])

        print("[INFO]: Loaded settings from file.")

    except FileNotFoundError:
        print(f"[WARNING]: File {file_path} not found. Using default settings.")
    except json.JSONDecodeError as e:
        print(f"[ERROR]: JSON decoding error: {e}")
        print("Using default settings.")
    except Exception as e:
        print(f"[ERROR]: Unexpected error: {e}")

# Loading settings
# If you don't want to load settings from JSON, then comment out the function call
load_settings_from_json(r"Assets/Countdown/settingsV2.json")

# JSON DEBUG
'''
print("FONT_SETTINGS:", FONT_SETTINGS)
print("APP_SETTINGS:", APP_SETTINGS)
print("COLOR_SETTINGS:", COLOR_SETTINGS)
'''

def set_window_icon(app):
    """
    Function: set_window_icon(app)

    Sets the application window icon based on the current system appearance mode (dark/light).
    The function automatically selects the appropriate version of the icon (white for dark mode, dark for light mode).

    Error Handling:
    - Prints warning if icon file is not found
    - Prints error if icon loading fails
    - Silently continues if icon cannot be set (The default CTk icon will be used instead)
    """

    # Determine the appearance mode of the application
    appearance_mode = ctk.get_appearance_mode()
    
    # Selecting the appropriate icon
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
            print(f"[ERROR] Nie udało się załadować ikony: {e}")
    else:
        print(f"[WARNING] Plik {icon_path} nie został znaleziony.")
    
    # Set icon only if loaded correctly
    if icon_loaded:
        app.root.wm_iconbitmap()

def pluralize_time_unit(value, singular, plural, genitive):
    """
    Helper function for inflecting time units in Polish language.
    
    :param value: numeric value
    :param singular: singular form | forma pojedyncza (np. "rok")
    :param plural: plural form | forma mnoga (np. "lata")
    :param genitive: genitive form | forma dopełniacza (np. "lat")
    :return: formatted string with value and correct word form
    """
    value = int(value)
    formatted_value = "{:,}".format(value).replace(",", " ")
    if value == 1: # singular form | forma pojedyncza
        return f"{formatted_value} {singular}"
    elif 2 <= value <= 4: # plural form | forma mnoga
        return f"{formatted_value} {plural}" 
    else: # genitive form | forma dopełniacza
        return f"{formatted_value} {genitive}"

def generate_time_texts(years, months, weeks, days, hours, minutes, seconds):
    """
    Generates text forms for time units.
    
    :param years: lata
    :param months: miesiące
    :param weeks: tygodnie
    :param days: dni
    :param hours: godziny
    :param minutes: minuty
    :param seconds: sekundy
    :return: a tuple with formatted strings for each time unit
    """
    return (
        pluralize_time_unit(int(years), "year", "years", "years"),
        pluralize_time_unit(int(months), "month", "months", "months"),
        pluralize_time_unit(int(weeks), "week", "weeks", "weeks"),
        pluralize_time_unit(int(days), "day", "days", "days"),
        pluralize_time_unit(hours, "hour", "hours", "hours"),
        pluralize_time_unit(minutes, "minute", "minutes", "minutes"),
        pluralize_time_unit(seconds, "second", "seconds", "seconds")
    )

class CountdownApp:
    def __init__(self, root):
        self.set_theme_colors()

        #ctk.set_appearance_mode(APP_SETTINGS["appearance_mode"]) # Legacy
        ctk.set_default_color_theme(APP_SETTINGS["color_theme"])

        self.root = root
        self.root.title(APP_SETTINGS["title"])
        self.root.geometry(APP_SETTINGS["window_size"])
        self.root.resizable(*APP_SETTINGS["resizable"])
        

        # Better scaling of UI elements
        ctk.set_window_scaling(APP_SETTINGS["ui_zoom_factor"]) # For the application window
        ctk.set_widget_scaling(APP_SETTINGS["ui_zoom_factor"]) # For UI elements
        
        # Setting the app icon
        if APP_SETTINGS["SetIcon"]:
            set_window_icon(self)

        now = datetime.now() + timedelta(
            days=0,
            hours=1,
            seconds=1
        )

        self.main_frame = ctk.CTkFrame(
            root, 
            #width=665,
            #height=375, # Legacy
            height = int(APP_SETTINGS["window_size"].split("x")[1]) - 26,
            fg_color=self.background_color, 
            border_width=1,
            #border_color="red"
        )
        self.main_frame.pack_propagate(False)
        self.main_frame.pack(padx=(10), pady=(10,0), fill="x", expand=True)

        self.current_date_label = ctk.CTkLabel(
            self.main_frame, 
            text="current_date_label", 
            font=FONT_SETTINGS["title"],
            text_color=self.text_color
        )
        self.current_date_label.pack(pady=(10,0))

        self.time_left_label = ctk.CTkLabel(
            self.main_frame, 
            text="time_left_label", 
            font=FONT_SETTINGS["countdown"],
            text_color=self.text_color
        )
        self.time_left_label.pack(padx=5, pady=(5,5))

        self.total_time_label = ctk.CTkLabel(
            self.main_frame, 
            text="total_time_label", 
            font=FONT_SETTINGS["units"],
            text_color=self.text_color,
        )
        self.total_time_label.pack(pady=(10,0))

        self.date_frame = ctk.CTkFrame(self.main_frame)
        self.date_frame.pack(side="bottom", pady=(0,10), anchor="s")

        ctk.CTkLabel(
            self.main_frame, 
            text="Calculate Date",
            font=FONT_SETTINGS["title"],
            text_color=self.highlight_color
        ).pack(pady=(0,10), side="bottom", anchor="s")

        '''
        Creates datetime input fields (year, month, day, hour, minute, second)
        Each field consists of:
        - Top: Entry field with default current time value
        - Bottom: Descriptive label
        Fields are initialized with stripped/zero-padded values where appropriate
        '''
        self.target_year = self.create_target_entry(self.date_frame, now.strftime("%Y"), 0, "Year", "year")
        self.target_month = self.create_target_entry(self.date_frame, now.strftime("%m").lstrip('0'), 1, "Month", "month")
        self.target_day = self.create_target_entry(self.date_frame, now.strftime("%d").lstrip('0'), 2, "Day", "day")
        self.target_hour = self.create_target_entry(self.date_frame, now.strftime("%H"), 3, "Hour", "hour")
        self.target_minute = self.create_target_entry(self.date_frame, now.strftime("%M"), 4, "Minute", "minute")
        self.target_second = self.create_target_entry(self.date_frame, now.strftime("%S"), 5, "Second", "second")

        self.version_label = ctk.CTkLabel(
            master=self.root, 
            text="Author: @Nieznany237 | Version 1.6.7 Released 30.03.2025 | First release 08.11.2024", 
            text_color="#7E7E7E", 
            anchor="se", 
            justify="right", 
            font=FONT_SETTINGS["footer"]
        )
        self.version_label.pack(side="bottom", anchor="se", padx=(0,3), pady=(0,1))

        self.update_time()

        '''
        # For Debug
        def print_app_settings():
            print("==============================================================================")
            # View basic application settings
            print(f"UI scaling: {APP_SETTINGS['ui_zoom_factor']}")

            # Displaying font settings
            for style, settings in FONT_SETTINGS.items():
                font_name = settings[0]
                font_size = settings[1]
                if len(settings) == 3:
                    font_weight = settings[2]
                    print(f"Font: {font_name}, Size: {font_size}, Weight: {font_weight} ({style})")
                else:
                    print(f"Font: {font_name}, Size: {font_size} ({style})")

            # Displaying application size
            print(f"App:        Width: {self.root.winfo_width()}, Height: {self.root.winfo_height()}")
            print(f"Main Frame: Width: {self.main_frame.winfo_width()}, Height: {self.main_frame.winfo_height()}")

            # Displaying color settings
            print("\nColor Settings:")
            for mode, colors in COLOR_SETTINGS.items():
                print(f"{mode.capitalize()} mode:")
                for color_type, color_value in colors.items():
                    print(f"  {color_type.capitalize()}: {color_value}")
            print("==============================================================================")

        # DEBUG
        print_app_settings()
        '''

    def set_theme_colors(self):
        """
        Sets widget colors based on current appearance mode (dark/light).
        Updates text, background and highlight colors from global COLOR_SETTINGS.
        """
        # Get the current theme mode
        ctk.set_appearance_mode(APP_SETTINGS["appearance_mode"])
        current_theme = ctk.get_appearance_mode().lower()

        print(f"Current theme: {current_theme}\nSettings theme:", APP_SETTINGS["appearance_mode"])
        
        if current_theme == "dark":
            self.text_color = COLOR_SETTINGS["dark"]["text_color"]
            self.background_color = COLOR_SETTINGS["dark"]["background_color"]
            self.highlight_color = COLOR_SETTINGS["dark"]["highlight_color"]
            #ctk.set_appearance_mode("dark")

        else:
            self.text_color = COLOR_SETTINGS["light"]["text_color"]
            self.background_color = COLOR_SETTINGS["light"]["background_color"]
            self.highlight_color = COLOR_SETTINGS["light"]["highlight_color"]
            #ctk.set_appearance_mode("light")

    def create_target_entry(self, frame, default_value, column, label_text, field_type=None):
        """Creates a validated datetime entry field with label.
        
        Args:
            frame: Parent widget for placement
            default_value: Initial value in entry field
            column: Grid column position
            label_text: Description shown below field
            field_type: Used for range validation (matches FIELD_RANGES keys)
        
        Validation:
            Uses validate_range() to ensure proper numeric input format
        """
        
        entry = ctk.CTkEntry(
            frame, 
            width=58, 
            font=FONT_SETTINGS["units"], 
            justify="center",
            validate="key",
            validatecommand=(self.root.register(lambda val: self.validate_range(val, field_type)), '%P')
        )
        entry.insert(0, default_value)
        entry.grid(row=0, column=column, padx=(5,5), pady=(5,0))
        ctk.CTkLabel(frame, text=label_text, font=FONT_SETTINGS["units"]).grid(row=1,pady=(0,3), column=column)
        return entry

    def validate_range(self, value, field_type):
        """
        Validates if value is either empty or within field_type's allowed range.
        """
        if not value.isdigit():
            return value == ""

        if field_type and value:
            min_val, max_val = FIELD_RANGES.get(field_type, (0, 9999))
            return min_val <= int(value) <= max_val

        return True
    
    def update_time(self):
        """
        Updates current time display and calculates time difference to target.
        Shows remaining time (future) or elapsed time (past).
        Auto-refreshes at configured interval.
        Handles invalid inputs with error messages.
        """
        now = datetime.now()
        self.current_date_label.configure(text=f"Current date: {now.strftime('%d.%m.%Y %H:%M:%S')}")

        # Check that all fields are filled in before converting to int
        try:
            year = self.target_year.get()
            month = self.target_month.get()
            day = self.target_day.get()
            hour = self.target_hour.get()
            minute = self.target_minute.get()
            second = self.target_second.get()

            if not all([year, month, day, hour, minute, second]):
                raise ValueError("All fields must be filled in")

            # Conversion to int
            target_date = datetime(
                int(year), int(month), int(day),
                int(hour), int(minute), int(second)
            )

            # Checking whether the date is in the future or in the past
            if now < target_date:
                self.display_time(now, target_date, mode="remaining")
            else:
                self.display_time(now, target_date, mode="elapsed")

        except ValueError as error_msg:
            self.time_left_label.configure(text="Incorrect date or time")
            self.total_time_label.configure(text=error_msg)

        self.root.after(APP_SETTINGS["refresh_interval"], self.update_time)

    # This function is a bit chaotic, but it gets the job done. Needs refactoring and optimization later.
    def display_time(self, now, target_date, mode="remaining"):

        # Calculating the difference
        if mode == "remaining":
            diff = relativedelta(target_date, now)
            total_seconds = (target_date - now).total_seconds()
        else:
            diff = relativedelta(now, target_date)
            total_seconds = (now - target_date).total_seconds()

        # Converting values to int
        years = int(diff.years)
        months = int(diff.months)
        weeks = diff.days // 7
        days = diff.days % 7
        hours = int(diff.hours)
        minutes = int(diff.minutes)
        seconds = int(diff.seconds)

        # Text generation for 'time_left_label'
        year_text, months_text, weeks_text, days_text, hours_text, minutes_text, seconds_text = generate_time_texts(
            years, months, weeks, days, hours, minutes, seconds
        )

        # Setting the label “time_left_label”
        if mode == "remaining":
            self.time_left_label.configure(
                text=f"Remaining: {year_text}, {months_text}, {weeks_text}, {days_text}, {hours_text}, {minutes_text} and {seconds_text}"
            )
        else:
            self.time_left_label.configure(
                text=f"Elapsed: {year_text}, {months_text}, {weeks_text}, {days_text}, {hours_text}, {minutes_text} and {seconds_text}"
            )

        # Calculating the total number of days
        total_days = total_seconds / (24 * 60 * 60)
        
        # Alternative calculations
        approx_months = round(total_days / 30.437)
        remaining_days_after_months = round(total_days % 30.437)
        total_weeks_approx = round(total_days / 7)
        remaining_days_after_weeks = round(total_days % 7)
        total_hours_approx = int(total_seconds // 3600)
        remaining_minutes_after_hours = int((total_seconds // 60) % 60)
        total_minutes_approx = int(total_seconds // 60)
        remaining_seconds_after_minutes = int(total_seconds % 60)

        # Set the “total_time_label” with the correct variation and formatting
        self.total_time_label.configure(
            text=( 
                f"In other words, total time {'remaining' if mode == 'remaining' else 'elapsed'}:\n"
                f"{pluralize_time_unit(years, 'year', 'years', 'years')}, {pluralize_time_unit(months, 'month', 'months', 'months')}, "
                f"{pluralize_time_unit(weeks, 'week', 'weeks', 'weeks')}, {pluralize_time_unit(days, 'day', 'days', 'days')}\n"
                f"{pluralize_time_unit(approx_months, 'month', 'months', 'months')}, {pluralize_time_unit(remaining_days_after_months, 'day', 'days', 'days')}\n"
                f"{pluralize_time_unit(total_weeks_approx, 'week', 'weeks', 'weeks')}, {pluralize_time_unit(remaining_days_after_weeks, 'day', 'days', 'days')}\n"
                f"{pluralize_time_unit(int(total_days), 'day', 'days', 'days')}, {pluralize_time_unit(hours, 'hour', 'hours', 'hours')}\n"
                f"{pluralize_time_unit(total_hours_approx, 'hour', 'hours', 'hours')}, "
                f"{pluralize_time_unit(remaining_minutes_after_hours, 'minute', 'minutes', 'minutes')}\n"
                f"{pluralize_time_unit(total_minutes_approx, 'minute', 'minutes', 'minutes')}, "
                f"{pluralize_time_unit(remaining_seconds_after_minutes, 'second', 'seconds', 'seconds')}\n"
                f"{pluralize_time_unit(int(total_seconds), 'second', 'seconds', 'seconds')}"
            )
        )

# Run the application
root = ctk.CTk()
app = CountdownApp(root)
root.mainloop()
