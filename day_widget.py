# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 02:39:41 2024

@author: Luka

A time management application using the Tkinter library.
The main components of this GUI include a calendar widget for viewing workdays,
a sidebar for managing flex time and vacation requests, and information panels
to display the user's current work status.
"""
import tkinter as tk
import datetime as dt
from datetime_functions import DatetimeFunctions as dtf

import gui_constants


class DayWidget(tk.Frame):
    """
    A class used to represent a working day element in the
    STC time management GUI.

    --------------------------------
    |day                           |
    |                              |
    |   start time                 |
    |                 break time   |
    |   end time                   |
    |                              |
    |         total time           |
    |                              |
    --------------------------------


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
        Initializes the Day_Widget with the given parent widget.

    set_day_number(day)
        Sets the day number displayed in the widget.

    set_start_time(time_in_seconds)
        Sets the start time in the widget using datetime.time.

    set_end_time(time_in_seconds)
        Sets the end time in the widget using datetime.time.

    set_break_time(time_in_seconds)
        Sets the break time in the widget using time in seconds.

    set_total_time(time_in_seconds)
        Sets the total working time in the widget using time in seconds.

    time_to_string(time=-1)
        Converts time in seconds to a string formatted as "HH:MM".
        Returns "--:--" if time is outside of range(0, 24*60*60-1).
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

        # Day number
        tk.Label(self, textvariable=self.var_day, border=1,
                 relief='solid', width=2).grid(sticky="nw", row=0, column=0)

        # Start and end of working time
        self.start_entry = tk.Entry(self, width=5, textvariable=self.var_start_time, justify='center').grid(
            row=2, column=1)
        self.end_entry = tk.Entry(self, width=5, textvariable=self.var_end_time, justify='center').grid(
            row=3, column=1)

        # Break time
        self.break_entry = tk.Entry(self, width=5, textvariable=self.var_break_time, justify='center').grid(
            row=2, rowspan=3, column=3)

        # Total working time
        tk.Label(self, textvariable=self.var_total_time, border=1,
                 relief='solid', width=10).grid(row=5, column=1, columnspan=3,
                                               padx=5, pady=5)

        # Spacer
        tk.Label(self, text=' ').grid(row=5, rowspan=2, column=4, pady=10)

    def set_day_number(self, day):
        """
        Sets the day number in the top-left corner of this widget.

        Parameters
        ----------
        day : int
            The day number to be displayed.
        """
        self.var_day.set(f"{day:02}")

    def get_verified_time_string(self, time):
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
        time_in_seconds : datetime.time
            The start time to display as datetime.time.
        """
        self.var_start_time.set(self.get_verified_time_string(time_object))

    def set_end_time(self, time_object):
        """
        Sets the end time in this widget.

        Parameters
        ----------
        time_in_seconds : datetime.time
            The end time to display as datetime.time.
        """
        self.var_end_time.set(self.get_verified_time_string(time_object))

    def set_break_time(self, time_in_seconds):
        """
        Sets the break time in this widget.

        Parameters
        ----------
        time_in_seconds : int
            The break time in seconds to be displayed.
        """
        self.var_break_time.set(dtf.time_to_string(self, time_in_seconds))

    def set_total_time(self, time_in_seconds):
        """
        Sets the total working time in this widget.

        Parameters
        ----------
        time_in_seconds : int
            The total working time in seconds to be displayed.
        """
        time_string = dtf.time_to_string(self, time_in_seconds)
        self.var_total_time.set(time_string)
