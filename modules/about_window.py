"""
Reusable AboutWindow for CustomTkinter-based applications.

This AboutWindow class provides a customizable about dialog for Python GUI apps using CustomTkinter.
It is designed to be easily imported and used in any project.

Usage:
    from modules.about_window import AboutWindow
    ...
    AboutWindow(master, app_settings, app_version, t_path)

Required arguments:
    - master: parent window
    - app_settings: dict with app info (title, etc.)
    - app_version: dict with version info (version, release_date, etc.)
    - t_path: translation function (or lambda for static text)

Optional:
    - icon paths can be customized via arguments or app_settings

"""
import sys
import platform
import webbrowser
try:
    from PIL import Image
except ImportError:
    Image = None
import customtkinter as ctk
from modules.utils import set_app_icon

class AboutWindow(ctk.CTkToplevel):
    def __init__(self, master, app_settings, app_version, t_path, icon_paths=None):
        super().__init__(master)
        self.title(app_settings.get("title", "About"))
        self.geometry("495x340")
        self.resizable(True, True)
        self.set_icon(app_settings)

        # Main container
        self.main_container = ctk.CTkFrame(self, border_width=1)
        self.main_container.pack(padx=5, pady=5, fill="both", expand=True)
        self.main_container.pack_propagate(False)
        
        # Content frame with two columns
        self.content_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.content_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        # Left side: logo/image
        self.left_panel = ctk.CTkFrame(self.content_frame, width=150, height=250, fg_color="transparent")
        self.left_panel.grid(row=0, column=0, padx=(0, 15), pady=10, sticky="nsew")
        
        # App icon
        app_icon_path = None
        if icon_paths and icon_paths.get("app_icon"):
            app_icon_path = icon_paths["app_icon"]
        else:
            app_icon_path = app_settings.get("icon_path", "Assets/Countdown/Icons/Countdown_dark_150.png")
        
        if Image and app_icon_path:
            try:
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
                    self.left_panel, text="Logo", width=150, height=150, corner_radius=10, fg_color="#f0f0f0", text_color="#333"
                )
                self.icon_label.pack(pady=10)
        else:
            self.icon_label = ctk.CTkLabel(
                self.left_panel, text="Logo", width=150, height=150, corner_radius=10, fg_color="#f0f0f0", text_color="#333"
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
            text=app_settings.get("title", "App Title"), 
            font=("Arial", 18, "bold")
        )
        self.title_label.pack(pady=(0, 0), anchor="w")
        
        # Program information
        program_info = f"""
        {t_path('about_window.program_info_description.program_name')}: {app_settings.get('title', '')}
        {t_path('about_window.program_info_description.version')}: {app_version.get('version', '')}
        {t_path('about_window.program_info_description.author')}: Niez | Nieznany237
        {t_path('about_window.program_info_description.release_date')}: {app_version.get('release_date', '')}
        {t_path('about_window.program_info_description.first_release')}: 19.11.2024
        {t_path('about_window.program_info_description.licence')}: MIT License
        
        Python: {self.get_python_version()}
        System: {self.get_system_info()}
        
        {t_path('about_window.program_info_description.description')}:
        {app_settings.get('description', 
        '''A simple countdown timer application built
        with Python and CustomTkinter. 
        This application allows users to set a target 
        date and time, displaying the remaining
        or elapsedtime in various formats.''')}
        """
        self.info_label = ctk.CTkLabel(
            self.right_panel, 
            font=("Arial", 14),
            text=program_info,  
            justify="left")
        self.info_label.pack(pady=(0,0), anchor="w")

    def set_icon(self, app_settings):
        """Set AboutWindow icon with Windows workaround (uses set_app_icon from utils)."""
        if app_settings.get("SetIcon", False):
            try:
                set_app_icon(self)
            except Exception as e:
                print(f"[AboutWindow] set_app_icon failed: {e}")

    def get_system_info(self):
        """Returns operating system information with try-except protection"""
        try:
            system = platform.system()
            version = ""
            if system == "Windows":
                version = platform.win32_ver()[1]
            elif system == "Linux":
                try:
                    version = platform.freedesktop_os_release().get('PRETTY_NAME', 'Linux')
                except:
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
        if Image:
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
        else:
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
