# Created by Niez
# Have a nice day :]

import customtkinter as ctk
from customtkinter import CTkLabel
from datetime import datetime, timedelta

# Application settings
FONT_SETTINGS = {
    "default": ("Arial", 12),        # Default font
    "title": ("Arial", 23, "bold"),  # Font for titles
    "countdown": ("Arial", 18),      # Font for countdown timer
    "units": ("Arial", 18),          # Font for time units
    "color": "#333333"               # Text color
}

class CountdownApp:
    def __init__(self, root):
        # Customtkinter settings
        ctk.set_appearance_mode("light")  # Set to light mode
        ctk.set_default_color_theme("blue")  # Set theme color (can be changed)

        self.root = root
        self.root.title("Countdown")
        self.root.geometry("545x375")
        self.root.resizable(False, False)

        # Center the main container
        self.main_frame = ctk.CTkFrame(root)
        self.main_frame.pack(expand=True, padx=20, pady=20)

        # Label displaying the current date and time
        self.current_date_label = ctk.CTkLabel(
            self.main_frame, 
            text="", 
            font=FONT_SETTINGS["title"],
            text_color=FONT_SETTINGS["color"]
        )
        self.current_date_label.pack(pady=10)

        # Label displaying the time remaining or elapsed from the target date
        self.time_left_label = ctk.CTkLabel(
            self.main_frame, 
            text="", 
            font=FONT_SETTINGS["countdown"],
            text_color=FONT_SETTINGS["color"]
        )
        self.time_left_label.pack(pady=5)

        # Label displaying time in different units
        self.total_time_label = ctk.CTkLabel(
            self.main_frame, 
            text="", 
            font=FONT_SETTINGS["units"],
            text_color=FONT_SETTINGS["color"]
        )
        self.total_time_label.pack(pady=5)

        ctk.CTkLabel(
            self.main_frame, 
            text="Calculate date",
            font=FONT_SETTINGS["title"],
            text_color=FONT_SETTINGS["color"]
        ).pack(pady=10)

        # Default target date: current time + 1 hour
        now = datetime.now() + timedelta(hours=1)

        # Container for target date and time input fields
        self.date_frame = ctk.CTkFrame(self.main_frame)
        self.date_frame.pack(pady=10)

        # Fields for entering the target date
        self.target_year = ctk.CTkEntry(
            self.date_frame, 
            width=55, 
            font=FONT_SETTINGS["units"], 
            justify="center"
        )
        self.target_year.insert(0, now.strftime("%Y"))
        self.target_year.grid(row=0, column=0, padx=5)
        ctk.CTkLabel(self.date_frame, text="Year", font=FONT_SETTINGS["units"]).grid(row=1, column=0)

        self.target_month = ctk.CTkEntry(
            self.date_frame, 
            width=50, 
            font=FONT_SETTINGS["units"], 
            justify="center"
        )
        self.target_month.insert(0, now.strftime("%m"))
        self.target_month.grid(row=0, column=1, padx=5)
        ctk.CTkLabel(self.date_frame, text="Month", font=FONT_SETTINGS["units"]).grid(row=1, column=1)

        self.target_day = ctk.CTkEntry(
            self.date_frame, 
            width=50, 
            font=FONT_SETTINGS["units"], 
            justify="center"
        )
        self.target_day.insert(0, now.strftime("%d"))
        self.target_day.grid(row=0, column=2, padx=5)
        ctk.CTkLabel(self.date_frame, text="Day", font=FONT_SETTINGS["units"]).grid(row=1, column=2)

        self.target_hour = ctk.CTkEntry(
            self.date_frame, 
            width=50, 
            font=FONT_SETTINGS["units"], 
            justify="center"
        )
        self.target_hour.insert(0, now.strftime("%H"))
        self.target_hour.grid(row=0, column=3, padx=5)
        ctk.CTkLabel(self.date_frame, text="Hour", font=FONT_SETTINGS["units"]).grid(row=1, column=3)

        self.target_minute = ctk.CTkEntry(
            self.date_frame, 
            width=50, 
            font=FONT_SETTINGS["units"], 
            justify="center"
        )
        self.target_minute.insert(0, now.strftime("%M"))
        self.target_minute.grid(row=0, column=4, padx=5)
        ctk.CTkLabel(self.date_frame, text="Minute", font=FONT_SETTINGS["units"]).grid(row=1, column=4)

        self.target_second = ctk.CTkEntry(
            self.date_frame, 
            width=50, 
            font=FONT_SETTINGS["units"], 
            justify="center"
        )
        self.target_second.insert(0, now.strftime("%S"))
        self.target_second.grid(row=0, column=5, padx=5)
        ctk.CTkLabel(self.date_frame, text="Second", font=FONT_SETTINGS["units"]).grid(row=1, column=5)

        self.version_label = CTkLabel(
                    master=self.root, 
                    text="By @Nieznany237 | Version 1.0 [03.11.2024]", 
                    text_color="#7E7E7E", 
                    anchor="se", 
                    justify="right", 
                    font=("Arial Bold", 10)
                )
        self.version_label.pack(side="bottom", anchor="se", padx=0, pady=0)

        # Start updating the time
        self.update_time()

    def update_time(self):
        now = datetime.now()
        self.current_date_label.configure(text=f"Current date: {now.strftime('%d.%m.%Y %H:%M:%S')}")

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
                # Calculate and display time remaining
                total_days = time_difference.days
                weeks, days = divmod(total_days, 7)
                hours, remainder = divmod(time_difference.seconds, 3600)
                minutes, seconds = divmod(remainder, 60)

                self.time_left_label.configure(text=f"Remaining: {weeks} weeks, {days} days, {hours} hours, {minutes} minutes, {seconds} seconds")
                self.total_time_label.configure(text=f"Total weeks: {total_days // 7}\n"
                                                    f"Total days: {total_days}\n"
                                                    f"Total hours: {seconds_difference // 3600}\n"
                                                    f"Total minutes: {seconds_difference // 60}\n"
                                                    f"Total seconds: {seconds_difference}")
            else:
                # Calculate and display time passed since target date
                abs_time_difference = abs(time_difference)
                total_days = abs_time_difference.days
                weeks, days = divmod(total_days, 7)
                hours, remainder = divmod(abs_time_difference.seconds, 3600)
                minutes, seconds = divmod(remainder, 60)

                self.time_left_label.configure(text=f"Elapsed: {weeks} weeks, {days} days, {hours} hours, {minutes} minutes, {seconds} seconds")
                self.total_time_label.configure(text=f"Total elapsed weeks: {total_days // 7}\n"
                                                    f"Total elapsed days: {total_days}\n"
                                                    f"Total elapsed hours: {int(abs_time_difference.total_seconds()) // 3600}\n"
                                                    f"Total elapsed minutes: {int(abs_time_difference.total_seconds()) // 60}\n"
                                                    f"Total elapsed seconds: {int(abs_time_difference.total_seconds())}")
        except ValueError:
            self.time_left_label.configure(text="Invalid date or time")
            self.total_time_label.configure(text="")

        # Refresh every second
        self.root.after(1000, self.update_time)

# Run the application
root = ctk.CTk()
app = CountdownApp(root)
root.mainloop()