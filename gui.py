# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 11:45:51 2024

@author: games
"""

import tkinter as tk
import re
from dateutil.relativedelta import relativedelta

from datetime_functions import DatetimeFunctions as dtf
import gui_constants


class Day_Widget(tk.Frame):
    def __init__(self, parent, bg_frame="lightgreen"):
        super().__init__(master=parent, bg=bg_frame, relief="solid", borderwidth=1)
        self.parent = parent
        self.font_scale_factor = 0.1
        self.date = None

        # StringVars labels
        self.var_day = tk.StringVar(value=f"{0:02}")
        self.var_start_time = tk.StringVar(value=gui_constants.NO_TIME_DATA)
        self.var_end_time = tk.StringVar(value=gui_constants.NO_TIME_DATA)
        self.var_break_time = tk.StringVar(value=gui_constants.NO_TIME_DATA)
        self.var_total_time = tk.StringVar(value=gui_constants.NO_TIME_DATA)

        # Create a Frame for the composite widget

        vcmd = (self.register(self.on_validate_input), '%P')
        vcmd_end = (self.register(self.on_validate_end), '%P')

        # Create and place labels and entries
        self.label_day = tk.Label(
            self, textvariable=self.var_day, anchor="center")
        self.entry_start = tk.Entry(self, textvariable=self.var_start_time,
                                    justify="center", validate="all", validatecommand=vcmd)
        self.entry_end = tk.Entry(self, textvariable=self.var_end_time,
                                  justify="center", validate="all", validatecommand=vcmd_end)
        self.entry_break = tk.Entry(self, textvariable=self.var_break_time,
                                    justify="center", validate="all", validatecommand=vcmd)
        self.label_total = tk.Label(
            self, textvariable=self.var_total_time, anchor="center")

        self.entry_start.insert(0, "start")
        self.entry_end.insert(0, "end")
        self.entry_break.insert(0, "break")

        # Place labels using relative positioning
        self.label_day.place(relwidth=0.2, relheight=0.2, anchor="nw")
        self.entry_start.place(relx=0.05, rely=0.25,
                               relwidth=0.425, relheight=0.2)
        self.entry_end.place(relx=0.05, rely=0.5,
                             relwidth=0.425, relheight=0.2)
        self.entry_break.place(relx=0.525, rely=0.4,
                               relwidth=0.425, relheight=0.2)
        self.label_total.place(relx=0.05, rely=0.75,
                               relwidth=0.9, relheight=0.2)

        # Bind resize event to adjust font size
        self.bind("<Configure>", self.adjust_font_size)

    def adjust_font_size(self, event):
        # Calculate font size based on the height of the Day_Widget frame
        font_size = int(event.height * self.font_scale_factor)

        # Apply calculated font size to each label and entry widget
        self.label_day.config(font=("Arial", font_size))
        self.entry_start.config(font=("Arial", font_size))
        self.entry_end.config(font=("Arial", font_size))
        self.entry_break.config(font=("Arial", font_size))
        self.label_total.config(font=("Arial", font_size))

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
        if time_object is None and gui_constants.USE_TEXT_HINTS:
            time_string = 'start'
            self.entry_start.config(fg=gui_constants.TEXT_HINT_COLOR)
        else:
            time_string = self.get_verified_time_string(time_object)

            self.entry_start.config(fg='black')

        self.var_start_time.set(time_string)

    def set_end_time(self, time_object):
        """
        Sets the end time in this widget.

        Parameters
        ----------
        time_object : datetime.time
            The end time to be displayed.
        """
        if time_object is None and gui_constants.USE_TEXT_HINTS:
            time_string = 'end'
            self.entry_end.config(fg=gui_constants.TEXT_HINT_COLOR)
        else:
            time_string = self.get_verified_time_string(time_object)

            self.entry_end.config(fg='black')

        self.var_end_time.set(time_string)

    def set_break_time(self, time_in_seconds):
        """
        Sets the break time in this widget.

        Parameters
        ----------
        time_in_seconds : int
            The break time in seconds.
        """
        if time_in_seconds is None and gui_constants.USE_TEXT_HINTS:
            time_string = 'break'
            self.entry_break.config(fg=gui_constants.TEXT_HINT_COLOR)
        else:
            time_string = dtf.time_to_string(self, time_in_seconds)

            self.entry_break.config(fg='black')

        self.var_break_time.set(time_string)

    def set_total_time(self, time_in_seconds):
        """
        Sets the total work time in this widget.

        Parameters
        ----------
        time_in_seconds : int
            The total work time in seconds.
        """
        self.var_total_time.set(dtf.time_to_string(self, time_in_seconds))


class Info_Panel(tk.Frame):
    def __init__(self, parent):
        """Composite widget containing six labels for displaying information."""
        super().__init__(master=parent, bg=gui_constants.BACKGROUND_COLOR,
                         relief="solid", borderwidth=1)

        # Data StringVars
        self.var_flex_time = tk.StringVar(value="+ 00:00")
        self.var_vacation_days = tk.StringVar(value=30)
        self.var_old_vacation_days = tk.StringVar(value=0)

        # Original labels
        self.label_flex_time = tk.Label(
            self, text="Flex-Time:", font=("Arial", 12, "underline"), bg=gui_constants.BACKGROUND_COLOR)
        self.label_vacation_days = tk.Label(
            self, text="Vacation Days:", font=("Arial", 12, "underline"), bg=gui_constants.BACKGROUND_COLOR)
        self.label_vacation_days_previous = tk.Label(
            self, text="From Previous Year:", font=("Arial", 12, "underline"), bg=gui_constants.BACKGROUND_COLOR)

        # New labels displaying "--"
        self.label_flex_time_text = tk.Label(
            self, textvariable=self.var_flex_time, font=("Arial", 12), bg=gui_constants.BACKGROUND_COLOR)
        self.label_vacation_days_text = tk.Label(
            self, textvariable=self.var_vacation_days, font=("Arial", 12), bg=gui_constants.BACKGROUND_COLOR)
        self.label_vacation_days_previous_text = tk.Label(
            self, textvariable=self.var_old_vacation_days, font=("Arial", 12), bg=gui_constants.BACKGROUND_COLOR)

        # Arrange labels in the Info_Panel
        self.label_flex_time.pack(padx=5, pady=(2, 0), anchor="w")
        self.label_flex_time_text.pack(padx=10, pady=(0, 5), anchor="w")

        self.label_vacation_days.pack(padx=5, pady=(2, 0), anchor="w")
        self.label_vacation_days_text.pack(padx=10, pady=(0, 5), anchor="w")

        self.label_vacation_days_previous.pack(padx=5, pady=(2, 0), anchor="w")
        self.label_vacation_days_previous_text.pack(
            padx=10, pady=(0, 5), anchor="w")


class Sidebar(tk.Frame):
    def __init__(self, parent, width):
        super().__init__(master=parent, width=width,
                         background=gui_constants.BACKGROUND_COLOR)
        """A composite sidebar widget with an Info_Panel and buttons."""

        # Create the Info_Panel at the top of the sidebar
        self.info_panel = Info_Panel(self)
        self.info_panel.pack(padx=10, pady=10, fill="x")

        # Add button directly below the Info_Panel
        self.button_request_vacation = tk.Button(
            self, text="Request Vacation", font=("Arial", 12))
        self.button_request_vacation.pack(padx=10, fill="x")

        # Create two buttons at the bottom, stacked on top of each other
        self.button_log_break = tk.Button(self, text="Start Break", font=(
            "Arial", 12), command=lambda: self.log_break())
        self.button_log_work = tk.Button(self, text="Start Workday", font=(
            "Arial", 12), command=lambda: self.log_time())

        # Place these buttons at the bottom
        self.button_log_break.pack(side="bottom", padx=10, pady=10, fill="x")
        self.button_log_work.pack(side="bottom", padx=10, fill="x")

    def log_time(self):
        """
        Callback method for work time logging button.
        """
        self.master.main.log_work_time()

    def log_break(self):
        """
        Callback method for break time logging button.
        """
        self.master.main.log_break_time()


class TopBar(tk.Frame):
    def __init__(self, parent, height, bg="lightgrey"):
        super().__init__(master=parent, height=height, bg='lightgrey')
        """A composite top bar widget that expands to fit the width of the window."""

        self.employee_name = tk.StringVar(value="default")
        self.role = tk.StringVar(value="(Employee)")

        self.logo = tk.Frame(self, relief="solid", padx=28, bg=bg)
        self.logo.pack(side='left', fill=tk.X)

        tk.Label(self.logo, text='STC',
                 font=gui_constants.EXTRA_LARGE, bg=bg).pack(side='top')
        tk.Label(self.logo, text='Time Management System',
                 font=gui_constants.BOLD, bg=bg).pack(side='top')

        self.menu = tk.Frame(self, relief="solid", padx=10, bg=bg)
        self.menu.pack(side='right', expand=True, fill=tk.BOTH)

        self.logout = tk.Button(
            self.menu, text="Logout", command=lambda: self.master.main.logout(),
            font=("Arial", 12))
        self.logout.pack(side='right')

        employee = tk.Frame(self.menu, bg=bg)
        employee.pack(side='right', padx=20)

        tk.Label(employee, textvariable=self.employee_name,
                 font=gui_constants.LARGE, bg=bg).pack(side='top')
        tk.Label(employee, textvariable=self.role,
                 bg=bg).pack(side='top', padx=20)


class MainApp(tk.Frame):
    def __init__(self, parent, main=None):
        super().__init__(master=parent)
        self.main = main
        self.var_selected_month = tk.StringVar(value="Current Month")

        # Configure root layout
        self.columnconfigure(0, minsize=200)  # Sidebar column
        self.columnconfigure(1, weight=1)     # Expandable Calendar_Frame
        self.rowconfigure(0, minsize=70)      # Top bar row
        self.rowconfigure(1, weight=1)        # Expandable Calendar_Frame area

        # Initialize components
        self.create_sidebar()
        self.create_top_bar()
        self.create_calendar_frame()

    def create_sidebar(self):
        # Sidebar in the leftmost column
        self.sidebar = Sidebar(self, width=200)
        self.sidebar.grid(row=1, column=0, sticky="nesw")

    def create_top_bar(self):
        # Top bar in the top row
        self.top_bar = TopBar(self, height=70)
        self.top_bar.grid(row=0, column=0, columnspan=2, sticky="nesw")

    def create_calendar_frame(self):
        # Calendar frame for Day_Widget grid area
        self.calendar_frame = tk.Frame(self, bg=gui_constants.ACCENT_COLOR)
        self.calendar_frame.grid(
            row=1, column=1, sticky="nsew", padx=10, pady=10)

        # Configure columns and rows
        for i in range(7):
            self.calendar_frame.columnconfigure(i, weight=1, uniform="column")
        for j in range(2, 8):
            self.calendar_frame.rowconfigure(j, weight=1, uniform="row")

        # Create current month header with navigation buttons
        self.button_previous_month = tk.Button(self.calendar_frame, font=(
            "Arial", 10), text="Previous Month", command=lambda: self.previous_month())
        self.button_previous_month.grid(
            row=0, column=0, sticky="new", padx=5, pady=5)

        self.label_current_month = tk.Label(self.calendar_frame, font=(
            "Arial", 18, "bold"), bg=gui_constants.ACCENT_COLOR, textvariable=self.var_selected_month)
        self.label_current_month.grid(
            row=0, column=1, columnspan=5, sticky="nsew")

        self.button_next_month = tk.Button(self.calendar_frame, font=(
            "Arial", 10), text="Next Month", command=lambda: self.next_month())
        self.button_next_month.grid(
            row=0, column=6, sticky="new", padx=5, pady=5)

        # Row of labels for each day of the week
        days_of_week = ["Monday", "Tuesday", "Wednesday",
                        "Thursday", "Friday", "Saturday", "Sunday"]
        for i, day in enumerate(days_of_week):
            day_label = tk.Label(self.calendar_frame,
                                 text=day, font=("Arial", 14), bg=gui_constants.ACCENT_COLOR)
            day_label.grid(row=1, column=i, sticky="nsew")

        # Create and place Day_Widget instances
        self.days = []
        for row in range(2, 8):
            for col in range(7):
                widget = Day_Widget(self.calendar_frame)
                widget.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)
                self.days.append(widget)

    def next_month(self):
        """
        Advances the calendar display by one month,
        updating the main calendar widget.
        """
        self.main.store_all_inputs()
        self.main.select_month(
            self.main.selected_date + relativedelta(months=1))

    def previous_month(self):
        """
        Moves the calendar display back by one month,
        updating the main calendar widget.
        """
        self.main.select_month(self.main.selected_date +
                               relativedelta(months=-1))


# Testing Login
if __name__ == "__main__":
    root = tk.Tk()
    root.title("SCT GUI")
    root.geometry("1280x720")
    root.minsize(1280, 720)

    app = MainApp(root)

    app.pack(expand=True, fill=tk.BOTH)

    root.mainloop()
