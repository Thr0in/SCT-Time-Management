# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 02:39:41 2024

@author: Luka

This module defines a graphical element, `DayWidget`, used in the STC time management
application for displaying and managing daily work time details.

The DayWidget provides input fields for start time, end time, and break time, as well
as a label to display total time worked on a specific day. It is designed to validate
time inputs in the format "HH:MM".

Classes:
--------
DayWidget
    A Tkinter Frame subclass representing a day element in the time management application.

Methods:
-------
__init__(parent)
    Initializes the DayWidget, creating Tkinter variables and widgets for displaying
    and editing daily time entries.

on_validate_input(field_input)
    Validates the user input for start, end, and break times in "HH:MM" format.

on_validate_end(field_input)
    Validates the end time input, ensuring it is after the start time.

store_input()
    Stores the current input data from this DayWidget in the application's main data model.

set_day_number(day)
    Sets the day number displayed in the widget.

get_verified_time_string(time)
    Converts a datetime object to a formatted time string, defaulting to "--:--" if `None`.

set_start_time(time_object)
    Sets the start time in the widget using a datetime object.

set_end_time(time_object)
    Sets the end time in the widget using a datetime object.

set_break_time(time_in_seconds)
    Sets the break time in the widget using time in seconds.

set_total_time(time_in_seconds)
    Sets the total working time in the widget using time in seconds.

"""

import tkinter as tk
import datetime as dt
import re

from datetime_functions import DatetimeFunctions as dtf
import gui_constants


class DayWidget(tk.Frame):
    """
    A class used to represent a working day element in the
    STC time management GUI.

    This widget displays the following daily work information:
    - Day number
    - Start time
    - End time
    - Break time
    - Total work time

    Attributes
    ----------
    var_day : StringVar
        Tkinter variable holding the day number.
    var_start_time : StringVar
        Tkinter variable holding the start time.
    var_end_time : StringVar
        Tkinter variable holding the end time.
    var_break_time : StringVar
        Tkinter variable holding the break time.
    var_total_time : StringVar
        Tkinter variable holding the total work time.

    Methods
    -------
    __init__(parent)
        Initializes the DayWidget with the given parent widget.

    on_validate_input(field_input)
        Validates the input for the start time, end time, and break time fields
        according to the format "HH:MM".

    on_validate_end(field_input)
        Ensures that the end time input is valid and occurs after the start time.

    store_input()
        Stores the current input values from this DayWidget in the application's main data model.

    set_day_number(day)
        Sets the day number displayed in the top-left corner of this widget.

    get_verified_time_string(time)
        Returns a formatted string for a time object or "--:--" if `None`.

    set_start_time(time_object)
        Updates the start time display based on a datetime object.

    set_end_time(time_object)
        Updates the end time display based on a datetime object.

    set_break_time(time_in_seconds)
        Sets the break time display based on the time provided in seconds.

    set_total_time(time_in_seconds)
        Sets the total working time display based on the time provided in seconds.

    """

    def __init__(self, parent):
        """
        Initializes this Day_Widget object, constructs all necessary
        attributes and sets its master as the specified parent.

        Parameters
        ----------
        parent : widget
            The parent widget in which this widget will be placed.
        """

        super().__init__(master=parent)

        self.config(borderwidth=1, relief='solid')

        self.var_day = tk.StringVar(value=f"{0:02}")
        self.var_start_time = tk.StringVar(value=gui_constants.NO_TIME_DATA)
        self.var_end_time = tk.StringVar(value=gui_constants.NO_TIME_DATA)
        self.var_break_time = tk.StringVar(value=gui_constants.NO_TIME_DATA)
        self.var_total_time = tk.StringVar(value=gui_constants.NO_TIME_DATA)

        vcmd = (self.register(self.on_validate_input), '%P')
        vcmd_end = (self.register(self.on_validate_end), '%P')

        # Day number
        tk.Label(self, textvariable=self.var_day, border=1,
                 relief='solid', width=2).grid(sticky="nw", row=0, column=0)

        # Start and end of working time
        self.start_entry = tk.Entry(self, width=5, textvariable=self.var_start_time,
                                    justify='center', validate="key", validatecommand=vcmd).grid(row=2, column=1)

        self.end_entry = tk.Entry(self, width=5, textvariable=self.var_end_time,
                                  justify='center', validate="key", validatecommand=vcmd_end).grid(row=3, column=1)

        # Break time
        self.break_entry = tk.Entry(self, width=5, textvariable=self.var_break_time, justify='center',
                                    validate="all", validatecommand=vcmd).grid(row=2, rowspan=3, column=3)

        # Total working time
        tk.Label(self, textvariable=self.var_total_time, border=1, relief='solid',
                 width=10).grid(row=5, column=1, columnspan=3, padx=5, pady=5)

        # Spacer
        tk.Label(self, text=' ').grid(row=5, rowspan=2, column=4, pady=10)

    def on_validate_input(self, field_input):
        """
        Validates the input for the start time, end time, and break time fields.

        Parameters
        ----------
        field_input : str
            The input string to be validated, expected in "HH:MM" format.

        Returns
        -------
        bool
            True if input matches the "HH:MM" format or is empty; False otherwise.
        """
        is_valid = True
        try:
            dtf.convert_string_to_time(self, field_input)
            if field_input[-2] != ":":
                self.store_input()
        except Exception:
            if field_input == "--:--" or field_input == "":
                self.store_input()

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
            True if the end time is valid and follows start time; False otherwise.
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

    def store_input(self):
        """
        Saves the current input data from this DayWidget to the application's main data model.
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
