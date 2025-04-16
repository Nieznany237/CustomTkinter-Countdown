import json
import os
import platform
import subprocess
import sys
import webbrowser
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from functools import lru_cache
from PIL import Image, ImageTk
import customtkinter as ctk
from tkinter import messagebox, filedialog
from CTkMenuBar import *
REQUIRED_JSON_VERSION = 9

current_file_path = ""

# Application version and release date
APP_VERSION = {
    "version": "1.7.0",
    "release_date": "15.04.2025"
}

RESOURCE_FILE_PATHS = {
    "json_config": "Assets/Countdown/settingsV2.json"
}

# Default application settings
FONT_SETTINGS = {
    "default": ("Arial", 14),
    "title": ("Arial", 23, "bold"),
    "countdown": ("Arial", 18),
    "units": ("Arial", 18),
    "footer": ("Arial", 11),
}

APP_SETTINGS = {
    "title": "Countdown",
    "window_size": "735x420",
    "SetIcon": True,
    "resizable": [False, False],
    "Language": "en",
    "appearance_mode": "dark",
    "color_theme": "blue",
    "ui_zoom_factor": 1.075,
    "refresh_interval": 1000
}

COLOR_SETTINGS = {
    "dark": {
      "text_color": "#FFFFFF",
      "background_color": "#2E2E2E",
      "date_frame_color": "#282828",
      "highlight_color": "#db143c"
    },
    "light": {
      "text_color": "#333333",
      "background_color": "#dbdbdb",
      "date_frame_color": "#cecece",
      "highlight_color": "#E60000"
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

# Setting global program path for nuitka and pyinstaller have been archived because they do it already
'''
def set_global_program_path():
    # Check if the program is compiled
    is_nuitka = "__compiled__" in globals()
    is_pyinstaller = getattr(sys, 'frozen', False)
    
    if is_nuitka:
        if '--onefile' in sys.argv or os.path.basename(sys.executable).lower() == sys.argv[0].lower():
            # Onefile mode - use original script location
            program_dir = os.path.dirname(os.path.abspath(__file__))
        else:
            # Standalone (onedir) mode
            program_dir = os.path.dirname(sys.executable)
    elif is_pyinstaller:
        program_dir = os.path.dirname(sys.executable)
    else:
        # For .py script
        program_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        
    os.chdir(program_dir)
    return program_dir

# Force setting the working directory to the script's/executable's location
set_global_program_path()
'''

def get_program_path(show_messagebox=False):
    # Print the current working directory (for debug purposes)
    print("\n=== Debug: Program Path ===")
    print("Current program directory:", os.getcwd())
    print("Frozen? (PyInstaller)",getattr(sys, 'frozen', False))
    print("Compiled? (Nuitka)", "__compiled__" in globals())
    print("=== Debug: Program Path ===\n")
    if show_messagebox:
        messagebox.showinfo(
            "Program Path", 
            f"Current program directory: {os.getcwd()}\n\n"
            f"Frozen? (PyInstaller) - {getattr(sys, 'frozen', False)}\n"
            f"Compiled? (Nuitka) - {'__compiled__' in globals()}"
            )

get_program_path()

# Function to convert lists to tuples for fonts
def convert_font_lists_to_tuples(font_settings):
    for key, value in font_settings.items():
        if isinstance(value, list):
            font_settings[key] = tuple(value)
    return font_settings

# Function to load settings from a JSON file
def load_settings_from_json(file_path = RESOURCE_FILE_PATHS["json_config"]):
    """
    Function: load_settings_from_json(file_path)
    Loads application settings from a JSON file into global variables.

    Args:
        file_path: Path to JSON settings file RESOURCE_FILE_PATHS["json_config"]

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
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            settings = json.load(f)
        
        # Check the JSON version
        if "VERSION" in settings:
            json_version = settings["VERSION"]
            if json_version != REQUIRED_JSON_VERSION:
                if "IGNORE_VERSION_ERROR" in settings and settings["IGNORE_VERSION_ERROR"]:
                    print(f"[WARNING]: The JSON version ({json_version}) does not match the required version ({REQUIRED_JSON_VERSION}), but the error is ignored. The settings will not be loaded.")
                else:
                    print(f"[ERROR]: JSON version ({json_version}) does not match required version ({REQUIRED_JSON_VERSION}). Default settings will be applied.")
                    messagebox.showerror("Error", f"[ERROR]: JSON version ({json_version}) does not match required version ({REQUIRED_JSON_VERSION}). Default settings will be applied.")
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
load_settings_from_json()

# JSON DEBUG
'''
print("FONT_SETTINGS:", FONT_SETTINGS)
print("APP_SETTINGS:", APP_SETTINGS)
print("COLOR_SETTINGS:", COLOR_SETTINGS)
'''
print(APP_SETTINGS["Language"])

if APP_SETTINGS["Language"] == "pl":
    # Load Polish translations
    from translation import TRANSLATIONS_PL as TRANSLATIONS
else:
    # Load English translations
    from translation import TRANSLATIONS_EN as TRANSLATIONS

@lru_cache(maxsize=None)
def t_path(path):

    """
    Retrieves a translation value from the TRANSLATIONS dictionary using a dot-separated path.
    This is a helper function to easily access nested translation values.
    Args:
        path (str): Dot-separated path to the translation (e.g., "menubar.file.file")
    Returns:
        str: The translated string if found, or a placeholder string in format "[path]" if not found
    Example:
        >>> t_path("menubar.file.file")
        "File"
        >>> t_path("invalid.path")
        "[invalid.path]"
        
    Note:
        The function is a shortened version of get_translation_by_path (as suggested by the name)
    """
    keys = path.split(".")
    value = TRANSLATIONS
    try:
        for key in keys:
            value = value[key]
        return value
    except KeyError:
        return f"[{path}]"

def get_cache_info():
    print(t_path.cache_info())


def open_settings_file_for_editing(settings_path = RESOURCE_FILE_PATHS["json_config"]):
    """
    Opens the settingsV2.json file in the default system editor.
    Supports different operating systems and displays error messages in the messagebox.
    """

    """  
    print("Exists:", os.path.exists(settings_path))
    print("Is file:", os.path.isfile(settings_path))
    print("Absolute path:", os.path.abspath(settings_path))
    """
    try:
        if not os.path.exists(settings_path) or not os.path.isfile(settings_path):
            raise FileNotFoundError(f"Invalid file path: {settings_path}")

        # Validate the JSON
        with open(settings_path, 'r', encoding='utf-8') as f:
            json.load(f)

        # Open the file depending on your operating system
        system = platform.system()
        if system == 'Windows':
            os.startfile(os.path.normpath(settings_path)) # For some reasons starfile likes to use backslash instead of forward slash
        elif system == 'Darwin':
            subprocess.run(['open', settings_path], check=True)
        elif system == 'Linux':
            subprocess.run(['xdg-open', settings_path], check=True)
        else:
            raise OSError("Unsupported operating system")

    except json.JSONDecodeError as e:
        messagebox.showerror("Error", f"The JSON file is corrupted:\n{e}")
    except FileNotFoundError as e:
        messagebox.showerror("Error", f"Settings file not found:\n{e}")
    except OSError as e:
        messagebox.showerror("Error", f"Problem with opening a file:\n{e}")
    except Exception as e:
        messagebox.showerror("Error", f"Unexpected error:\n{e}")

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
            print(f"[ERROR] Failed to load icon: {e}")
    else:
        print(f"[WARNING] File {icon_path} has not been found.")
    
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
        pluralize_time_unit(int(years), *t_path('main_window.plural_forms.year')),
        pluralize_time_unit(int(months), *t_path("main_window.plural_forms.month")),
        pluralize_time_unit(int(weeks), *t_path("main_window.plural_forms.week")),
        pluralize_time_unit(int(days), *t_path("main_window.plural_forms.day")),
        pluralize_time_unit(hours, *t_path("main_window.plural_forms.hour")),
        pluralize_time_unit(minutes, *t_path("main_window.plural_forms.minute")),
        pluralize_time_unit(seconds, *t_path("main_window.plural_forms.second"))
    )

def change_ui_scale(scale=0):
    APP_SETTINGS["ui_zoom_factor"] += scale
    
    APP_SETTINGS["ui_zoom_factor"] = round(APP_SETTINGS["ui_zoom_factor"], 3)
    print(f"UI zoom factor: {APP_SETTINGS['ui_zoom_factor']}")
    ctk.set_window_scaling(APP_SETTINGS["ui_zoom_factor"])
    ctk.set_widget_scaling(APP_SETTINGS["ui_zoom_factor"])

# =============== Loading and Saving Files ===============

def load_file_dialog(self):
    file_path = filedialog.askopenfilename(filetypes=[("Countdown Files", "*.countdown")])
    if file_path:
        load_file(self, file_path)
    else:
        print("[INFO]: File dialog canceled by the user.")

def load_file(self, file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read().strip()
            
            # Parsing the date and updating the fields
            dt = datetime.strptime(content, "%Y-%m-%d %H:%M:%S")
            update_entries(self, dt)
            # Storing the path of the loaded file
            global current_file_path
            current_file_path = file_path
            print(f"Loaded: {dt} - {file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"File loading error:\n{e}")
    #print(current_file_path)

def load_file_dialog(self):
    file_path = filedialog.askopenfilename(filetypes=[("Countdown Files", "*.countdown")])
    if file_path:
        print(f"[debug_file] Selected file: {file_path}")  # Debug print
        load_file(self, file_path)
    else:
        print("[INFO]: File dialog canceled by the user.")

def load_file(self, file_path):
    print(f"[debug_file] Attempting to load file: {file_path}")  # Debug print
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read().strip()
            print(f"[debug_file] File content: '{content}'")  # Debug print
            
            # Parsing the date and updating the fields
            dt = datetime.strptime(content, "%Y-%m-%d %H:%M:%S")
            print(f"[debug_file] Parsed datetime: {dt}")  # Debug print
            update_entries(self, dt)
            
            # Storing the path of the loaded file
            global current_file_path
            current_file_path = file_path
            print(f"[debug_file] Updated current_file_path to: {current_file_path}")  # Debug print
            print(f"Loaded: {dt} - {file_path}")
    except Exception as e:
        print(f"[debug_file] Error loading file: {e}")  # Debug print
        messagebox.showerror("Error", f"File loading error:\n{e}")

def update_entries(self, dt):
    debug_info = [
        "---------[update_entries]---------",
        f"Updating entries with datetime: {dt}",
        f"{dt.strftime('%Y')}.{dt.strftime('%m')}.{dt.strftime('%d')} {dt.strftime('%H')}:{dt.strftime('%M')}:{dt.strftime('%S')}",
        "----------------------------------",
    ]
    print('\n'.join(debug_info))
    
    self.target_year.delete(0, ctk.END)
    self.target_year.insert(0, dt.strftime("%Y"))

    self.target_month.delete(0, ctk.END)
    self.target_month.insert(0, str(int(dt.strftime("%m"))))

    self.target_day.delete(0, ctk.END)
    self.target_day.insert(0, str(int(dt.strftime("%d"))))

    self.target_hour.delete(0, ctk.END)
    self.target_hour.insert(0, dt.strftime("%H"))

    self.target_minute.delete(0, ctk.END)
    self.target_minute.insert(0, dt.strftime("%M"))

    self.target_second.delete(0, ctk.END)
    self.target_second.insert(0, dt.strftime("%S"))

def save_file(self, save_as=False):
    print(f"[save_file] save_as flag: {save_as}")  # Debug print
    global current_file_path
    try:
        # If it's not "Save As" and we have a path, use it
        if not save_as and current_file_path:
            file_path = current_file_path
            print(f"[save_file] Using existing file path: {file_path}")  # Debug print
        else:
            print("[save_file_as] Prompting for new file path")  # Debug print
            file_path = filedialog.asksaveasfilename(
                defaultextension=".countdown", 
                filetypes=[("Countdown Files", "*.countdown")]
            )
            if not file_path:
                print("[save_file_as] Save dialog canceled")  # Debug print
                return
        
        # Format the date string
        date_str = (f"{self.target_year.get()}-{int(self.target_month.get()):02d}-"
                    f"{int(self.target_day.get()):02d} {int(self.target_hour.get()):02d}:"
                    f"{int(self.target_minute.get()):02d}:{int(self.target_second.get()):02d}")
        print(f"[debug_file] Formatted date string: {date_str}")  # Debug print
        
        # Save to file
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(date_str)
        
        # Update the current file path
        current_file_path = file_path
        print(f"[debug_file] Updated current_file_path to: {current_file_path}")  # Debug print
        print(f"Saved: {date_str} - {file_path}")
        
    except Exception as e:
        print(f"[debug_file] Error saving file: {e}")  # Debug print
        messagebox.showerror("Error", f"Failed to save file\n{e}")

def save_file_as(self):
    save_file(self,save_as=True)

# =============== - ===============

class CountdownApp:
    def __init__(self, root):
        ctk.set_appearance_mode(APP_SETTINGS["appearance_mode"])
        ctk.set_default_color_theme(APP_SETTINGS["color_theme"])

        self.root = root
        self.root.title(APP_SETTINGS["title"])
        self.root.geometry(APP_SETTINGS["window_size"])
        self.root.resizable(*APP_SETTINGS["resizable"])
        self.set_theme_colors()

        # Better scaling of UI elements
        change_ui_scale()

        # Setting the app icon
        if APP_SETTINGS["SetIcon"]:
            set_window_icon(self)

        self.menu = CTkMenuBar(root, padx=0)

        # Sekcja File
        file_button = self.menu.add_cascade(t_path("menubar.file.file"))
        file_dropdown = CustomDropdownMenu(widget=file_button)
        file_dropdown.add_option(option=t_path("menubar.file.load_file"), command=lambda: load_file_dialog(self))
        file_dropdown.add_option(option=t_path("menubar.file.save_file"), command=lambda: save_file(self))
        file_dropdown.add_separator()
        file_dropdown.add_option(option=t_path("menubar.file.save_as"), command=lambda: save_file_as(self))
        file_dropdown.add_separator()
        file_dropdown.add_option(option=t_path("menubar.file.exit"), command=lambda: self.root.quit())

        # Sekcja Appearance
        appearance_button = self.menu.add_cascade(t_path("menubar.appearance.appearance"))
        appearance_dropdown = CustomDropdownMenu(widget=appearance_button)
        appearance_dropdown.add_option(option=t_path("menubar.appearance.dark_mode"), command=lambda: self.set_app_appearance_mode("dark"))
        appearance_dropdown.add_option(option=t_path("menubar.appearance.light_mode"), command=lambda: self.set_app_appearance_mode("light"))
        appearance_dropdown.add_separator()
        appearance_dropdown.add_option(option=t_path("menubar.appearance.zoom_in"), command=lambda: change_ui_scale(0.1))
        appearance_dropdown.add_option(option=t_path("menubar.appearance.zoom_out"), command=lambda: change_ui_scale(-0.1))

        # Sekcja Config 
        settings_button = self.menu.add_cascade(t_path("menubar.settings.settings"))
        settings_dropdown = CustomDropdownMenu(widget=settings_button)
        settings_dropdown.add_option(option=t_path("menubar.settings.open_config_file"), command=lambda: open_settings_file_for_editing())
        #settings_dropdown.add_option(option=t_path("menubar.settings.update"), command=lambda: print("Update"))

        # Sekcja About
        about_button = self.menu.add_cascade(t_path("menubar.about.about"))
        about_dropdown = CustomDropdownMenu(widget=about_button)
        about_dropdown.add_option(option=t_path("menubar.about.about_this_app"), command=lambda: AboutWindow(root))
        about_dropdown.add_separator()
        about_dropdown.add_option(option=t_path("menubar.about.get_program_path_debug"), command=lambda: get_program_path(True))
        about_dropdown.add_option(option=t_path("menubar.about.get_cache_info"), command=lambda: get_cache_info())

        now = datetime.now() + timedelta(
            days=0,
            hours=1,
            seconds=1
        )

        self.main_frame = ctk.CTkFrame(
            root, 
            #width=665,
            #height=375, # Legacy
            #height = int(APP_SETTINGS["window_size"].split("x")[1]) - 27,
            fg_color=self.background_color, 
            border_width=1,
            #border_color="red"
        )
        self.main_frame.pack_propagate(False)
        self.main_frame.pack(padx=(5), pady=(5,5), fill="both", expand=True)

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
        self.total_time_label.pack(pady=(0,0))

        self.warning_label = ctk.CTkLabel(
            self.main_frame, 
            text=t_path("main_window.warning_label"), 
            font=FONT_SETTINGS["footer"],
            text_color=self.text_color,
        )
        self.warning_label.pack(pady=(2,0))

        self.date_frame = ctk.CTkFrame(
            self.main_frame, 
            fg_color = self.date_frame_color
            )
        self.date_frame.pack(side="bottom", pady=(0,10), anchor="s")

        self.calculate_date = ctk.CTkLabel(
            self.main_frame, 
            text=t_path("main_window.calculate_date"),
            font=FONT_SETTINGS["title"],
            text_color=self.highlight_color
        )
        self.calculate_date.pack(pady=(0,10), side="bottom", anchor="s")

        '''
        Creates datetime input fields (year, month, day, hour, minute, second)
        Each field consists of:
        - Top: Entry field with default current time value
        - Bottom: Descriptive label
        Fields are initialized with stripped/zero-padded values where appropriate
        '''
        self.target_year = self.create_target_entry(self.date_frame, now.strftime("%Y"), 0, t_path("main_window.target_entry.year"), "year")
        self.target_month = self.create_target_entry(self.date_frame, now.strftime("%m").lstrip('0'), 1, t_path("main_window.target_entry.month"), "month")
        self.target_day = self.create_target_entry(self.date_frame, now.strftime("%d").lstrip('0'), 2, t_path("main_window.target_entry.day"), "day")
        self.target_hour = self.create_target_entry(self.date_frame, now.strftime("%H"), 3, t_path("main_window.target_entry.hour"), "hour")
        self.target_minute = self.create_target_entry(self.date_frame, now.strftime("%M"), 4, t_path("main_window.target_entry.minute"), "minute")
        self.target_second = self.create_target_entry(self.date_frame, now.strftime("%S"), 5, t_path("main_window.target_entry.second"), "second")
        
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

        # Check if the program was launched with a file
        if len(sys.argv) > 1:
            print("\nProgram launched with a file.\n")
            try:
                load_file(self, sys.argv[1])
            except Exception as e:
                print(f"Error while loading the file: {e}")
        else:
            print("\nProgram launched without a file.\n")

    def set_theme_colors(self):
            """
            Sets widget colors based on current appearance mode (dark/light).
            Updates text, background and highlight colors from global COLOR_SETTINGS.
            """
            # Get the current theme mode
            current_theme = ctk.get_appearance_mode().lower()

            print(f"Current theme: {current_theme}\nSettings theme:", APP_SETTINGS["appearance_mode"])
            
            if current_theme == "dark":
                self.text_color = COLOR_SETTINGS["dark"]["text_color"]
                self.background_color = COLOR_SETTINGS["dark"]["background_color"]
                self.date_frame_color = COLOR_SETTINGS["dark"]["date_frame_color"]
                self.highlight_color = COLOR_SETTINGS["dark"]["highlight_color"]
                #ctk.set_appearance_mode("dark")

            else:
                self.text_color = COLOR_SETTINGS["light"]["text_color"]
                self.background_color = COLOR_SETTINGS["light"]["background_color"]
                self.date_frame_color = COLOR_SETTINGS["light"]["date_frame_color"]
                self.highlight_color = COLOR_SETTINGS["light"]["highlight_color"]
                #ctk.set_appearance_mode("light")

    def set_app_appearance_mode(self, theme):
        ctk.set_appearance_mode(theme)
        self.set_theme_colors()

        self.main_frame.configure(fg_color = self.background_color)
        self.current_date_label.configure(text_color = self.text_color)
        self.time_left_label.configure(text_color = self.text_color)
        self.total_time_label.configure(text_color = self.text_color)
        self.warning_label.configure(text_color = self.text_color)
        self.date_frame.configure(fg_color = self.date_frame_color)
        self.calculate_date.configure(text_color=self.highlight_color)
        if APP_SETTINGS["SetIcon"]:
            set_window_icon(self)


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
        self.current_date_label.configure(text=f"{t_path('main_window.current_date_label')} {now.strftime('%d.%m.%Y %H:%M:%S')}")
        
        # Check that all fields are filled in before converting to int
        try:
            year = self.target_year.get()
            month = self.target_month.get()
            day = self.target_day.get()
            hour = self.target_hour.get()
            minute = self.target_minute.get()
            second = self.target_second.get()

            if not all([year, month, day, hour, minute, second]):
                raise ValueError(t_path("main_window.empty_input"))

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
            self.time_left_label.configure(text=t_path("main_window.invalid_date"))
            self.total_time_label.configure(text=error_msg)

        self.root.after(APP_SETTINGS["refresh_interval"], self.update_time)

    # This function is a bit chaotic, but it gets the job done. Needs refactoring and optimization later.
    def display_time(self, now, target_date, mode="remaining"):

        # Calculating the difference
        if mode == "remaining":
            diff = relativedelta(target_date, now)
            total_days = (target_date - now).total_seconds() / 86400  # Calculate total days including fractional days
            weeks = int(total_days // 7)  # Calculate full weeks
            days = total_days % 7  # Remaining days after full weeks
            total_seconds = (target_date - now).total_seconds()
        else:
            diff = relativedelta(now, target_date)
            total_seconds = (now - target_date).total_seconds()

        total_days = (target_date - now).days if mode == "remaining" else (now - target_date).days
        weeks = total_days // 7
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
                text=f"{t_path('main_window.remaining_text')} {year_text}, {months_text}, {weeks_text}, {days_text}, {hours_text}, {minutes_text} {t_path('main_window.and')} {seconds_text}"
            )
        else:
            self.time_left_label.configure(
                text=f"{t_path('main_window.elapsed_text')} {year_text}, {months_text}, {weeks_text}, {days_text}, {hours_text}, {minutes_text} {t_path('main_window.and')} {seconds_text}"
            )

        total_days = total_seconds / 86400 # 1 Day (24 * 60 * 60)
        
        # Alternative calculations using relativedelta for accurate month calculation
        diff = relativedelta(target_date, now) if mode == "remaining" else relativedelta(now, target_date)
        approx_months = diff.years * 12 + diff.months
        remaining_days_after_months = diff.days
        total_weeks_approx = (total_days / 7)
        remaining_days_after_weeks = (total_days % 7)
        total_hours_approx = int(total_seconds // 3600)
        remaining_minutes_after_hours = int((total_seconds // 60) % 60)
        total_minutes_approx = int(total_seconds // 60)
        remaining_seconds_after_minutes = int(total_seconds % 60)

        # Set the “total_time_label” with the correct variation and formatting
        self.total_time_label.configure(
            text=( 
                f"{t_path('main_window.in_other_words')} {t_path('main_window.remaining_text') if mode == 'remaining' else t_path('main_window.elapsed_text')}\n"
                
                # x years, x months, x weeks, x days
                f"{pluralize_time_unit(years, *t_path('main_window.plural_forms.year'))}, "
                f"{pluralize_time_unit(months, *t_path('main_window.plural_forms.month'))}, "
                f"{pluralize_time_unit(weeks, *t_path('main_window.plural_forms.week'))}, "
                f"{pluralize_time_unit(days, *t_path('main_window.plural_forms.day'))}\n"

                # x months, x days
                f"{pluralize_time_unit(int(approx_months), *t_path('main_window.plural_forms.month'))}, "
                f"{pluralize_time_unit(remaining_days_after_months, *t_path('main_window.plural_forms.day'))}\n"

                # x weeks, x days
                f"{pluralize_time_unit(total_weeks_approx, *t_path('main_window.plural_forms.week'))}, "
                f"{pluralize_time_unit(int(remaining_days_after_weeks), *t_path('main_window.plural_forms.day'))}\n"

                # x days, x hours
                f"{pluralize_time_unit(int(total_days), *t_path('main_window.plural_forms.day'))}, "
                f"{pluralize_time_unit(hours, *t_path('main_window.plural_forms.hour'))}\n"

                # x hours, x minutes
                f"{pluralize_time_unit(total_hours_approx, *t_path('main_window.plural_forms.hour'))}, "
                f"{pluralize_time_unit(remaining_minutes_after_hours, *t_path('main_window.plural_forms.minute'))}\n"

                # x minutes, x seconds
                f"{pluralize_time_unit(total_minutes_approx, *t_path('main_window.plural_forms.minute'))}, "
                f"{pluralize_time_unit(remaining_seconds_after_minutes, *t_path('main_window.plural_forms.second'))}\n"
                
                # x seconds
                f"{pluralize_time_unit(int(total_seconds), *t_path('main_window.plural_forms.second'))}"
            )
        )
        
class AboutWindow(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title(t_path("about_window.about_window_title"))
        self.geometry("495x340")
        self.resizable(True, True)

        # Main container
        self.main_container = ctk.CTkFrame(
            self, 
            border_width=1,
        )
        self.main_container.pack(padx=5, pady=5, fill="both", expand=True)
        self.main_container.pack_propagate(False)
        
        # Content frame with two columns
        self.content_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.content_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        # Left side: logo/image
        self.left_panel = ctk.CTkFrame(self.content_frame, width=150, height=250, fg_color="transparent")
        self.left_panel.grid(row=0, column=0, padx=(0, 15), pady=10, sticky="nsew")
        
        try:
            app_icon_path = "Assets/Countdown/Icons/Countdown_dark_150.png"
            app_icon_image = Image.open(app_icon_path)
            
            self.app_icon = ctk.CTkImage(
                light_image=app_icon_image,
                dark_image=app_icon_image,
                size=(110, 110)
            )
            
            self.icon_label = ctk.CTkLabel(self.left_panel, image=self.app_icon, text="")
            self.icon_label.pack(pady=10)
            
        except Exception as e:
            print(f"Image loading error: {e}")
            self.icon_label = ctk.CTkLabel(
                self.left_panel, 
                text="Logo", 
                width=150, 
                height=150, 
                corner_radius=10, 
                fg_color="#f0f0f0", 
                text_color="#333"
            )
            self.icon_label.pack(pady=10)

        # GitHub icon and link

        self.github_profile_label = self._create_clickable_link(
            " Nieznany237", 
            "https://github.com/Nieznany237"
        )

        self.github_repo_label = self._create_clickable_link(
            " GitHub Repository", 
            "https://github.com/Nieznany237/CustomTkinter-Countdown"
        )
        '''
        self.other_link_label = self._create_clickable_link(
            " Placeholder", 
            "https://example.com",
            "OtherIconLight.png",  # Ścieżki do alternatywnych ikon
            "OtherIconDark.png"
        )
        '''
        # Right side: information
        self.right_panel = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.right_panel.grid(row=0, column=1, padx=(10, 0), pady=10, sticky="nsew")
        
        # Header
        self.title_label = ctk.CTkLabel(
            self.right_panel, 
            text=APP_SETTINGS["title"], 
            font=("Arial", 18, "bold")
        )
        self.title_label.pack(pady=(0, 0), anchor="w")
        
        # Program information
        program_info = f"""
        {t_path("about_window.program_info_description.program_name")}: {APP_SETTINGS["title"]}
        {t_path("about_window.program_info_description.version")}: {APP_VERSION["version"]}
        {t_path("about_window.program_info_description.author")}: Niez | Nieznany237
        {t_path("about_window.program_info_description.release_date")}: {APP_VERSION["release_date"]}
        {t_path("about_window.program_info_description.first_release")}: 8.11.2024
        {t_path("about_window.program_info_description.licence")}: MIT
        
        Python: {self.get_python_version()}
        System: {self.get_system_info()}
        
        {t_path("about_window.program_info_description.description")}:
        A simple countdown timer application built
        with Python and CustomTkinter. 
        This application allows users to set a target 
        date and time, displaying the remaining
        or elapsedtime in various formats.
        """
        self.info_label = ctk.CTkLabel(
            self.right_panel, 
            font=FONT_SETTINGS["default"],
            text=program_info, 
            text_color=(
                COLOR_SETTINGS["light"]["text_color"], 
                COLOR_SETTINGS["dark"]["text_color"]), 
            justify="left")
        self.info_label.pack(pady=(0,0), anchor="w")
    
    def get_system_info(self):
        """Returns operating system information with try-except protection"""
        try:
            system = platform.system()
            version = ""
            if system == "Windows":
                version = platform.win32_ver()[1]
            elif system == "Linux":
                try:
                    # For newer Linux systems
                    version = platform.freedesktop_os_release().get('PRETTY_NAME', 'Linux')
                except:
                    # Fallback for older systems
                    version = platform.linux_distribution()[0] or 'Linux'
            elif system == "Darwin":
                version = f"macOS {platform.mac_ver()[0]}"
            else:
                version = ""
                
            return f"{system} {version}".strip()
            
        except Exception as e:
            print(f"Error getting system information: {e}")
            return platform.system() or "Unknown system"
    
    def get_python_version(self):
        """Returns Python version with try-except protection"""
        try:
            return sys.version.split()[0]
        except Exception as e:
            print(f"Error getting Python version: {e}")
            return "Unknown Python version"
    
    def _create_clickable_link(self, text, url, icon_light_path="Assets/Countdown/Icons/GitHubV2Dark.png", icon_dark_path="Assets/Countdown/Icons/GitHubV2White.png"):
        """Helper function to create clickable link label with optional icon"""
        try:
            icon_light = Image.open(icon_light_path)
            icon_dark = Image.open(icon_dark_path)
            icon = ctk.CTkImage(
                light_image=icon_light,
                dark_image=icon_dark,
                size=(22, 22)
            )
            
            label = ctk.CTkLabel(
                self.left_panel,
                text=text,
                font=("Arial", 13, "bold"),
                image=icon,
                compound="left",
                cursor="hand2",
                text_color=("#E60000", "#db143c")
                #("#1a73e8", "#8ab4f8") # Legacy
            )
        except Exception as e:
            print(f"Icon loading error: {e}")
            label = ctk.CTkLabel(
                self.left_panel,
                text=text,
                font=("Arial", 13),
                cursor="hand2",
                text_color=("#E60000","#db143c")
            )
    
        label.pack(padx=(0, 0), pady=(0, 0), anchor="w")
        label.bind("<Button-1>", lambda e: webbrowser.open_new_tab(url))
        return label

# Run the application
root = ctk.CTk()
app = CountdownApp(root)
root.mainloop()
