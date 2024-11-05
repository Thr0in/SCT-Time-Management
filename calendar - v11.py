# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 11:55:07 2024

@author: jnath

Kalendar Widget mit 
    - Start und Endtime seperat loggen (auch manuell eingebbar)
    - Automatischer Start Stop Button
    - Automatisch aktueller Tag ausgewählt (auch anderer Tag auswählbar)
    - ausgewählter tag ist farblich makiert
    - Clear
    - Export
    - Edit
    - Import Funktionen
    - Vorheriger und Nächster Monat
    
05.11.24
angefangen Farben und Formatierungen zu ändern    

Documentation and Turorials
    https://www.geeksforgeeks.org/python-gui-tkinter/
    https://docs.python.org/3/library/tk.html
    https://www.geeksforgeeks.org/tkinter-colors/
    https://matplotlib.org/stable/gallery/color/named_colors.html
    Youtube: 
        NeuralNine, 
        Code First with Hala, 
        Codemy.com
"""

import tkinter as tk
import calendar
import csv
from tkinter import messagebox, filedialog
from datetime import datetime

class CalendarApp:
    def __init__(self, master):
        #Window
        self.master = master
        #Window name
        self.master.title("SFC Timesheet Calendar")
        
        #Heading
        self.name = tk.Label(master, text="SFC Timesheet", font=('Helvetica', 32, "bold"))
        self.name.pack(expand=1, fill='both', pady=16)

        # Create a label for the month and year
        # Text and font and for month
        self.month_label = tk.Label(master, text="", bg="light blue", font=('Helvetica', 32))
        # Position and padding for month
        self.month_label.pack(expand=1, fill='both', pady=16)

        # Create a frame to hold the day buttons
        self.day_frame = tk.Frame(master)
        self.day_frame.pack()

        # Navigation buttons for month switching
        self.nav_frame = tk.Frame(master)
        self.nav_frame.pack(pady=16)

        self.prev_button = tk.Button(self.nav_frame, text="Previous Month", width=32, command=self.prev_month)
        self.prev_button.pack(side=tk.LEFT, padx=16)

        self.next_button = tk.Button(self.nav_frame, text="Next Month", width=32, command=self.next_month)
        self.next_button.pack(side=tk.LEFT, padx=16)

        # Label and Entry for start and end times
        self.log_frame = tk.Frame(master)
        self.log_frame.pack(pady=10)

        self.start_label = tk.Label(self.log_frame, text="Start Time (HH:MM):")
        self.start_label.pack(side=tk.LEFT)

        self.start_entry = tk.Entry(self.log_frame, width=10)
        self.start_entry.pack(side=tk.LEFT)

        self.current_start_button = tk.Button(self.log_frame, text="Current Start", command=self.set_current_start)
        self.current_start_button.pack(side=tk.LEFT)

        self.log_start_button = tk.Button(self.log_frame, text="Log Start", command=self.log_start_time)
        self.log_start_button.pack(side=tk.LEFT)

        self.end_label = tk.Label(self.log_frame, text="End Time (HH:MM):")
        self.end_label.pack(side=tk.LEFT)

        self.end_entry = tk.Entry(self.log_frame, width=10)
        self.end_entry.pack(side=tk.LEFT)

        self.current_end_button = tk.Button(self.log_frame, text="Current End", command=self.set_current_end)
        self.current_end_button.pack(side=tk.LEFT)

        self.log_end_button = tk.Button(self.log_frame, text="Log End", command=self.log_end_time)
        self.log_end_button.pack(side=tk.LEFT)

        self.clear_button = tk.Button(self.log_frame, text="Clear Entry", command=self.clear_hours)
        self.clear_button.pack(side=tk.LEFT)

        self.edit_button = tk.Button(self.log_frame, text="Edit Entry", command=self.edit_hours)
        self.edit_button.pack(side=tk.LEFT)

        self.export_button = tk.Button(self.log_frame, text="Export Timesheet", command=self.export_timesheet)
        self.export_button.pack(side=tk.LEFT)

        self.load_button = tk.Button(self.log_frame, text="Load Timesheet", command=self.load_timesheet)
        self.load_button.pack(side=tk.LEFT)

        # Initialize the month and year
        self.year = 2024
        self.month = 11  # November
        self.selected_day = None
        self.hours_logged = {}

        # Dictionary to store references to buttons for each day
        self.day_buttons = {}

        # Get today's date to highlight current day
        self.today = datetime.today()
        self.current_day = self.today.day
        self.current_month = self.today.month
        self.current_year = self.today.year

        # Create the calendar for the specified month
        self.show_calendar(self.year, self.month)


    def show_calendar(self, year, month):
        # Clear the frame
        for widget in self.day_frame.winfo_children():
            widget.destroy()

        # Update the month label
        month_name = calendar.month_name[month]
        self.month_label.config(text=f"{month_name} {year}")

        # Weekday labels
        weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for idx, day in enumerate(weekdays):
            label = tk.Label(self.day_frame, text=day, font=('Helvetica', 12))
            label.grid(row=0, column=idx)

        # Get the month calendar as a matrix (list of weeks)
        month_days = calendar.monthcalendar(year, month)

        # Create buttons for each day in the month
        for week_idx, week in enumerate(month_days, start=1):
            for day_idx, day in enumerate(week):
                if day == 0:
                    # If day is 0, it's an empty space
                    day_button = tk.Button(self.day_frame, text="", width=4, state='disabled')
                else:
                    # Create a button for the day with logged hours if any
                    date_key = f"{year}-{month:02d}-{day:02d}"
                    hours_info = self.hours_logged.get(date_key, [])
                    hours_display = "\n".join([f"{start} - {end}" for start, end in hours_info])
                    day_button = tk.Button(self.day_frame, text=f"{day}\n{hours_display}", width=10,
                                           command=lambda d=day: self.select_day(d))

                    # Store the button reference
                    self.day_buttons[day] = day_button
                
                day_button.grid(row=week_idx, column=day_idx, padx=5, pady=5)

        # Highlight current day if no day is selected
        if self.selected_day is None and self.current_year == self.year and self.current_month == self.month:
            self.select_day(self.current_day)

    def select_day(self, day):
        self.selected_day = day
        self.start_entry.delete(0, tk.END)  # Clear the start time entry
        self.end_entry.delete(0, tk.END)    # Clear the end time entry
        
        # Load existing hours if available
        date_key = f"{self.year}-{self.month:02d}-{day:02d}"
        if date_key in self.hours_logged:
            # For simplicity, just use the first entry for now
            if self.hours_logged[date_key]:
                start, end = self.hours_logged[date_key][0]
                self.start_entry.insert(0, start)
                self.end_entry.insert(0, end)

        # Update button colors
        for day_btn in self.day_buttons.values():
            day_btn.config(bg="SystemButtonFace")  # Reset all buttons to default color

        # Highlight the selected day in red
        if day in self.day_buttons:
            self.day_buttons[day].config(bg='light blue')

    def log_start_time(self):
        start_time = self.start_entry.get()
        if self.validate_time(start_time):
            self.log_time(start_time, is_start=True)
            self.start_entry.delete(0, tk.END)  # Clear entry after logging
        else:
            print("Please enter a valid start time in HH:MM format.")

    def log_end_time(self):
        end_time = self.end_entry.get()
        if self.validate_time(end_time):
            self.log_time(end_time, is_start=False)
            self.end_entry.delete(0, tk.END)  # Clear entry after logging
        else:
            print("Please enter a valid end time in HH:MM format.")

    def log_time(self, time_str, is_start):
        date_key = f"{self.year}-{self.month:02d}-{self.selected_day:02d}" if self.selected_day else datetime.now().strftime("%Y-%m-%d")
        
        if date_key not in self.hours_logged:
            self.hours_logged[date_key] = []

        if is_start:
            if len(self.hours_logged[date_key]) == 0 or self.hours_logged[date_key][-1][1] is not None:
                self.hours_logged[date_key].append((time_str, None))
                print(f"Logged start time for {date_key}: {time_str}")
        else:
            if self.hours_logged[date_key] and self.hours_logged[date_key][-1][1] is None:
                self.hours_logged[date_key][-1] = (self.hours_logged[date_key][-1][0], time_str)
                print(f"Logged end time for {date_key}: {time_str}")

        self.show_calendar(self.year, self.month)  # Refresh calendar display

    def set_current_start(self):
        current_time = datetime.now().strftime("%H:%M")
        self.start_entry.delete(0, tk.END)
        self.start_entry.insert(0, current_time)
        self.log_time(current_time, is_start=True)

    def set_current_end(self):
        current_time = datetime.now().strftime("%H:%M")
        self.end_entry.delete(0, tk.END)
        self.end_entry.insert(0, current_time)
        self.log_time(current_time, is_start=False)

    def edit_hours(self):
        if self.selected_day is not None:
            date_key = f"{self.year}-{self.month:02d}-{self.selected_day:02d}"
            if date_key in self.hours_logged and self.hours_logged[date_key]:
                start_time = self.start_entry.get()
                end_time = self.end_entry.get()
                
                # Check if a start time is entered
                if start_time and self.validate_time(start_time):
                    self.hours_logged[date_key][0] = (start_time, self.hours_logged[date_key][0][1])  # Update start time
                
                # Check if an end time is entered
                if end_time and self.validate_time(end_time):
                    self.hours_logged[date_key][0] = (self.hours_logged[date_key][0][0], end_time)  # Update end time

                print(f"Edited hours for {date_key}: {start_time} - {end_time}")
                self.show_calendar(self.year, self.month)  # Refresh calendar display
            else:
                print("No hours logged for this date.")

    def clear_hours(self):
        if self.selected_day is not None:
            date_key = f"{self.year}-{self.month:02d}-{self.selected_day:02d}"
            if date_key in self.hours_logged:
                del self.hours_logged[date_key]
                print(f"Cleared hours for {date_key}")
                self.show_calendar(self.year, self.month)  # Refresh calendar display
            else:
                print("No hours logged for this date.")

    def validate_time(self, time_str):
        try:
            hour, minute = map(int, time_str.split(':'))
            return 0 <= hour < 24 and 0 <= minute < 60
        except ValueError:
            return False

    def export_timesheet(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, 'w', newline='') as csvfile:
                fieldnames = ['Date', 'Start Time', 'End Time']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()
                for date, hours in self.hours_logged.items():
                    for start, end in hours:
                        writer.writerow({'Date': date, 'Start Time': start, 'End Time': end})

            messagebox.showinfo("Export Successful", f"Timesheet exported to {file_path}")

    def load_timesheet(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.hours_logged.clear()  # Clear existing data
            try:
                with open(file_path, 'r') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        date = row['Date']
                        start_time = row['Start Time']
                        end_time = row['End Time']
                        if date not in self.hours_logged:
                            self.hours_logged[date] = []
                        self.hours_logged[date].append((start_time, end_time))
                messagebox.showinfo("Load Successful", f"Timesheet loaded from {file_path}")
                self.show_calendar(self.year, self.month)  # Refresh calendar display
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load timesheet: {e}")

    def prev_month(self):
        if self.month == 1:
            self.month = 12
            self.year -= 1
        else:
            self.month -= 1
        self.show_calendar(self.year, self.month)

    def next_month(self):
        if self.month == 12:
            self.month = 1
            self.year += 1
        else:
            self.month += 1
        self.show_calendar(self.year, self.month)


if __name__ == "__main__":
    root = tk.Tk()
    app = CalendarApp(root)
    
    # Window background color
    #root.config (background = "darkslateblue")
    # Window size
    #root.geometry("1440x900")
    
    root.mainloop()
