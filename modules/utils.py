import os
import sys
from tkinter import messagebox
from PIL import Image, ImageTk
import platform
import customtkinter as ctk

def get_program_path(show_messagebox=False, status_flag=None):
    """
    v1.0.1 (2025-05-30)
    Prints and optionally shows a messagebox with debug info about the current program path and environment.
    Args:
        show_messagebox (bool): If True, shows a messagebox with the info.
        status_flag (str, optional): Status string to display (e.g., JSON loaded status). If None, omits this line.
    """
    print("\n=== Debug: Program Path ===")
    print("Current program directory:", os.getcwd())
    if status_flag is not None:
        print(f"JSON status: {status_flag}")
    else:
        print("JSON status: Not provided")
    print("Frozen? (PyInstaller)", getattr(sys, 'frozen', False))
    print("Compiled? (Nuitka)", "__compiled__" in globals())
    print("=== Debug: Program Path ===\n")
    if show_messagebox:
        msg = f"Current program directory: {os.getcwd()}\n\n"
        if status_flag is not None:
            msg += f"JSON status: {status_flag}\n"
        msg += f"Frozen? (PyInstaller) - {getattr(sys, 'frozen', False)}\n"
        msg += f"Compiled? (Nuitka) - {'__compiled__' in globals()}"
        messagebox.showinfo("Program Path", msg)

def set_app_icon(app, icon_dark_path="Assets/Countdown/Icons/white_icon1.png", icon_light_path="Assets/Countdown/Icons/dark_icon1.png"):
    """
    v1.1.1 (2025-05-30)
    Sets the application window icon based on the current system appearance mode (dark/light).
    Automatically selects the appropriate icon version. On Windows, works around CustomTkinter bug by resetting icon after 200ms.
    Args:
        app: The application or window instance. If it has .root, uses app.root, else uses app itself.
        icon_dark_path (str): Path to the icon for dark mode
        icon_light_path (str): Path to the icon for light mode
    ! https://github.com/TomSchimansky/CustomTkinter/issues/1163
    """
    appearance_mode = ctk.get_appearance_mode()
    icon_path = icon_dark_path if appearance_mode == "Dark" else icon_light_path
    icon_loaded = False
    # Use .root if present, else use app itself
    window = getattr(app, 'root', app)
    if os.path.exists(icon_path):
        try:
            icon_image = Image.open(icon_path)
            icon_photo = ImageTk.PhotoImage(icon_image)
            window.iconphoto(False, icon_photo)
            icon_loaded = True
        except Exception as e:
            print(f"[ERROR] Failed to load icon: {e}")
    else:
        print(f"[WARNING] File {icon_path} has not been found.")
    # Workaround for CustomTkinter Windows bug
    if icon_loaded and platform.system().lower().startswith("win"):
        def reset_icon():
            try:
                window.iconphoto(False, icon_photo)
            except Exception as e:
                print(f"[ERROR] Failed to reset icon after delay: {e}")
        window.after(200, reset_icon)