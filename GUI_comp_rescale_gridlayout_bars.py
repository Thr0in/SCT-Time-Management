# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 11:45:51 2024

@author: games
"""

import tkinter as tk
import re

from datetime_functions import DatetimeFunctions as dtf
import gui_constants

class Day_Widget(tk.Frame):
    def __init__(self, parent, width_ratio, height_ratio, bg_frame="lightgreen"):
        super().__init__(master=parent, bg=bg_frame)
        self.parent = parent
        self.width_ratio = width_ratio
        self.height_ratio = height_ratio

        # StringVars labels
        self.var_day = tk.StringVar(value=f"{0:02}")
        self.var_start_time = tk.StringVar(value=gui_constants.NO_TIME_DATA)
        self.var_end_time = tk.StringVar(value=gui_constants.NO_TIME_DATA)
        self.var_break_time = tk.StringVar(value=gui_constants.NO_TIME_DATA)
        self.var_total_time = tk.StringVar(value=gui_constants.NO_TIME_DATA)

        # Create a Frame for the composite widget
        #self.frame = tk.Frame(parent, bg=bg_frame)
        self.grid_propagate(False)

        vcmd = (self.register(self.on_validate_input), '%P')
        vcmd_end = (self.register(self.on_validate_end), '%P')

        # Create and place labels and entries
        self.label_day = tk.Label(self, textvariable=self.var_day, anchor="center")
        self.entry_start = tk.Entry(self, textvariable=self.var_start_time, justify="center", validate="all", validatecommand=vcmd)
        self.entry_end = tk.Entry(self, textvariable=self.var_end_time, justify="center", validate="all", validatecommand=vcmd_end)
        self.entry_break = tk.Entry(self, textvariable=self.var_break_time, justify="center", validate="all", validatecommand=vcmd)
        self.label_total = tk.Label(self, textvariable=self.var_total_time, anchor="center")

        self.entry_start.insert(0, "start")
        self.entry_end.insert(0, "end")
        self.entry_break.insert(0, "break")

        # Place labels using relative positioning
        self.label_day.place(relwidth=0.2, relheight=0.2, anchor="nw")
        self.entry_start.place(relx=0.05, rely=0.25, relwidth=0.425, relheight=0.2)
        self.entry_end.place(relx=0.05, rely=0.5, relwidth=0.425, relheight=0.2)
        self.entry_break.place(relx=0.525, rely=0.4, relwidth=0.425, relheight=0.2)
        self.label_total.place(relx=0.05, rely=0.75, relwidth=0.9, relheight=0.2)

    def update_size(self, width, height):
        composite_width = int(width * self.width_ratio)
        composite_height = int(height * self.height_ratio)
        self.config(width=composite_width, height=composite_height)

        # Calculate font size based on composite height
        font_size = max(8, int(composite_height * 0.1))
        font = ("Arial", font_size)

        # Update font for each label and entry
        self.label_day.config(font=font)
        self.entry_start.config(font=font)
        self.entry_end.config(font=font)
        self.entry_break.config(font=font)
        self.label_total.config(font=font)

    def on_validate_input(self, field_input):
        """
        Validates the input for the start time,
        end time, and break time fields.

        Parameters
        ----------
        field_input : str
            The input string to be validated, expected in "HH:MM" format.

        Returns
        -------
        bool
            True if input matches the "HH:MM"
            format or is empty; False otherwise.
        """
        is_valid = True
        try:
            dtf.convert_string_to_time(self, field_input)
            if field_input[-2] != ":":
                self.store_input()
        except Exception:
            if field_input == '':
                self.delete_input()

# Regex: Every possible substring which still can lead to
#        a valid time string by writing from left to right.
        pattern = re.compile(
            "([0-2]?|([0-2][0-3]|[0-1]?[0-9])|([0-2][0-3]|[0-1]?[0-9]):|([0-2][0-3]|[0-1]?[0-9]):[0-5]|([0-2][0-3]|[0-1]?[0-9]):[0-5][0-9])|([-:]{0,5})")
        if not pattern.fullmatch(field_input):
            is_valid = False

        if len(field_input) > 5:
            is_valid = False

        return is_valid

    def on_validate_end(self, field_input):
        """
        Validates that the end time input is in the correct format
        and occurs after the start time.

        Parameters
        ----------
        field_input : str
            The input string for end time, expected in "HH:MM" format.

        Returns
        -------
        bool
            True if the end time is valid and
            follows start time; False otherwise.
        """
        is_valid = self.on_validate_input(field_input)

        for i in range(0, len(field_input)):
            try:
                start = dtf.convert_string_to_time(
                    self, self.var_start_time.get())
            except ValueError:
                start = dtf.convert_string_to_time(self, '0:00')

            try:
                end = field_input[:i+1] + '-9:59'[i+1:]
                end = dtf.convert_string_to_time(self, end)
            except Exception:
                end = dtf.convert_string_to_time(self, '23:59')

            try:
                dtf.get_time_difference(self, start, end)
            except ValueError:
                is_valid = False

        return is_valid

    def delete_input(self):
        self.master.master.main.delete_input_data(self)

    def store_input(self):
        """
        Saves the current input data from this
        DayWidget to the application's main data model.
        """
        self.master.master.main.store_input_data(self)

    def set_day_number(self, day):
        """
        Sets the day number displayed in this widget.

        Parameters
        ----------
        day : int
            The day number to be displayed.
        """
        self.var_day.set(f"{day:02}")

    def get_verified_time_string(self, time):
        """
        Converts a datetime object to a formatted time string or
        returns "--:--" if the time is None.

        Parameters
        ----------
        time : datetime.time or None
            The time to format.

        Returns
        -------
        str
            The formatted time string.
        """
        if time is None:
            time_string = gui_constants.NO_TIME_DATA
        else:
            time_string = time.strftime(gui_constants.TIME_FORMAT)
        return time_string

    def set_start_time(self, time_object):
        """
        Sets the start time in this widget.

        Parameters
        ----------
        time_object : datetime.time
            The start time to be displayed.
        """
        self.var_start_time.set(self.get_verified_time_string(time_object))

    def set_end_time(self, time_object):
        """
        Sets the end time in this widget.

        Parameters
        ----------
        time_object : datetime.time
            The end time to be displayed.
        """
        self.var_end_time.set(self.get_verified_time_string(time_object))

    def set_break_time(self, time_in_seconds):
        """
        Sets the break time in this widget.

        Parameters
        ----------
        time_in_seconds : int
            The break time in seconds.
        """
        self.var_break_time.set(dtf.time_to_string(self, time_in_seconds))

    def set_total_time(self, time_in_seconds):
        """
        Sets the total work time in this widget.

        Parameters
        ----------
        time_in_seconds : int
            The total work time in seconds.
        """
        self.var_total_time.set(dtf.time_to_string(self, time_in_seconds))


class Info_Panel:
    def __init__(self, parent):
        """Composite widget containing six labels for displaying information."""
        self.frame = tk.Frame(parent, bg="lightgray")

        # Original labels
        self.label_flex_time = tk.Label(self.frame, text="Flex-Time", font=("Arial", 12, "underline"), bg="lightgray")
        self.label_vacation_days = tk.Label(self.frame, text="Vacation Days", font=("Arial", 12, "underline"), bg="lightgray")
        self.label_vacation_days_previous = tk.Label(self.frame, text="From Previous Year", font=("Arial", 12, "underline"), bg="lightgray")

        # New labels displaying "--"
        self.label_flex_time_text = tk.Label(self.frame, text="--", font=("Arial", 12), bg="lightgray")
        self.label_vacation_days_text = tk.Label(self.frame, text="--", font=("Arial", 12), bg="lightgray")
        self.label_vacation_days_previous_text = tk.Label(self.frame, text="--", font=("Arial", 12), bg="lightgray")

        # Arrange labels in the Info_Panel
        self.label_flex_time.pack(padx=5, pady=(2, 0), anchor="w")
        self.label_flex_time_text.pack(padx=10, pady=(0, 5), anchor="w")

        self.label_vacation_days.pack(padx=5, pady=(2, 0), anchor="w")
        self.label_vacation_days_text.pack(padx=10, pady=(0, 5), anchor="w")

        self.label_vacation_days_previous.pack(padx=5, pady=(2, 0), anchor="w")
        self.label_vacation_days_previous_text.pack(padx=10, pady=(0, 5), anchor="w")

class Sidebar:
    def __init__(self, parent, width):
        """A composite sidebar widget with an Info_Panel and buttons."""
        self.frame = tk.Frame(parent, width=width, bg="gray")
        self.frame.grid_propagate(False)  # Prevents resizing

        # Create the Info_Panel at the top of the sidebar
        self.info_panel = Info_Panel(self.frame)
        self.info_panel.frame.pack(padx=10, pady=10, fill="x")

        # Add button directly below the Info_Panel
        self.button_request_vacation = tk.Button(self.frame, text="Request Vacation", font=("Arial", 12))
        self.button_request_vacation.pack(padx=10, fill="x")

        # Create two buttons at the bottom, stacked on top of each other
        self.button_start_break = tk.Button(self.frame, text="Start Break", font=("Arial", 12))
        self.button_start_work = tk.Button(self.frame, text="Start Workday", font=("Arial", 12))

        # Place these buttons at the bottom
        self.button_start_break.pack(side="bottom", padx=10, pady=10, fill="x")
        self.button_start_work.pack(side="bottom", padx=10, fill="x")

class TopBar:
    def __init__(self, parent, height):
        """A composite top bar widget that expands to fit the width of the window."""
        self.frame = tk.Frame(parent, bg="darkblue", height=height)
        self.frame.grid_propagate(False)

        # Logout button on the right side of the top bar
        self.logout_button = tk.Button(self.frame, text="Logout", font=("Arial", 12), bg="white")
        self.logout_button.pack(padx=10, pady=10, side="right")  # Align the button to the right side of the bar
    
class MainApp:
    def __init__(self):
        # Initialize the root window
        self.root = tk.Tk()
        self.root.title("SCT GUI")
        self.root.geometry("1280x720")
        self.root.minsize(1280, 720)

        # Configure root layout
        self.root.columnconfigure(0, minsize=200)  # Sidebar column
        self.root.columnconfigure(1, weight=1)     # Expandable Calendar_Frame
        self.root.rowconfigure(0, minsize=70)      # Top bar row
        self.root.rowconfigure(1, weight=1)        # Expandable Calendar_Frame area

        # Initialize components
        self.create_sidebar()
        self.create_top_bar()
        self.create_calendar_frame()

    def create_sidebar(self):
        # Sidebar in the leftmost column
        self.sidebar = Sidebar(self.root, width=200)
        self.sidebar.frame.grid(row=0, column=0, rowspan=2, sticky="nesw")

    def create_top_bar(self):
        # Top bar in the top row
        self.top_bar = TopBar(self.root, height=70)
        self.top_bar.frame.grid(row=0, column=1, sticky="nesw")

    def create_calendar_frame(self):
        # Calendar frame for Day_Widget grid area
        self.calendar_frame = tk.Frame(self.root, bg="lightblue")
        self.calendar_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        # Configure columns and rows
        for i in range(7):
            self.calendar_frame.columnconfigure(i, weight=1, uniform="column")
        for j in range(2, 8):
            self.calendar_frame.rowconfigure(j, weight=1, uniform="row")

        # Create current month header with navigation buttons
        self.button_previous_month = tk.Button(self.calendar_frame, font=("Arial", 10), text="Previous Month")
        self.button_previous_month.grid(row=0, column=0, sticky="new", padx=5, pady=5)

        self.label_current_month = tk.Label(self.calendar_frame, font=("Arial", 18, "bold"), bg="lightblue", text="Current Month")
        self.label_current_month.grid(row=0, column=1, columnspan=5, sticky="nsew")

        self.button_next_month = tk.Button(self.calendar_frame, font=("Arial", 10), text="Next Month")
        self.button_next_month.grid(row=0, column=6, sticky="new", padx=5, pady=5)

        # Row of labels for each day of the week
        days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        for i, day in enumerate(days_of_week):
            day_label = tk.Label(self.calendar_frame, text=day, font=("Arial", 14), bg="lightblue")
            day_label.grid(row=1, column=i, sticky="nsew")

        # Create and place Day_Widget instances
        self.composite_widgets = []
        for row in range(2, 8):
            for col in range(7):
                widget = Day_Widget(self.calendar_frame, width_ratio=1/7, height_ratio=1/6)
                widget.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)
                self.composite_widgets.append(widget)

    def run(self):
        # Run the Tkinter event loop
        self.root.mainloop()

app = MainApp()
app.run()