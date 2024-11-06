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


class DayWidget(tk.Frame):
    """
    A class used to represent a working day element in the
    SCT time management GUI.

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
        Sets the start time in the widget using time in seconds.

    set_end_time(time_in_seconds)
        Sets the end time in the widget using time in seconds.

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

        no_time_data = "--:--"

        self.var_day = tk.StringVar(value=f"{0:02}")
        self.var_start_time = tk.StringVar(value=no_time_data)
        self.var_end_time = tk.StringVar(value=no_time_data)
        self.var_break_time = tk.StringVar(value=no_time_data)
        self.var_total_time = tk.StringVar(value=no_time_data)

        # self.rowconfigure(6)
        # self.columnconfigure(4, uniform='z')

        # Day number
        tk.Label(self, textvariable=self.var_day, border=1,
                 relief='solid', width=2).grid(sticky="nw", row=0, column=0)

        # Start and end of working time
# =============================================================================
#         tk.Label(self, textvariable=self.var_start_time, border=1,
#                  relief='solid').grid(row=2, column=1, padx=5, pady=5)
#         tk.Label(self, textvariable=self.var_end_time, border=1,
#                  relief='solid').grid(row=3, column=1, padx=5, pady=5)
# =============================================================================
        tk.Entry(self, width=5, textvariable=self.var_start_time).grid(
            row=2, column=1)
        tk.Entry(self, width=5, textvariable=self.var_end_time).grid(
            row=3, column=1)

        # Break time
# =============================================================================
#         tk.Label(self, textvariable=self.var_break_time, border=1,
#                  relief='solid', pady=16).grid(row=2, rowspan=3, column=3,
#                                                padx=5, pady=5)
# =============================================================================
        tk.Entry(self, width=5, textvariable=self.var_break_time).grid(
            row=2, rowspan=3, column=3)

        # Total working time
        tk.Label(self, textvariable=self.var_total_time, border=1,
                 relief='solid', padx=21).grid(row=5, column=1, columnspan=3,
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

    def set_start_time(self, time_in_seconds):
        """
        Sets the start time in this widget.

        Parameters
        ----------
        time_in_seconds : int
            The start time in seconds to be displayed.
        """
        time_string = self.time_to_string(time_in_seconds)
        self.var_start_time.set(time_string)

    def set_end_time(self, time_in_seconds):
        """
        Sets the end time in this widget.

        Parameters
        ----------
        time_in_seconds : int
            The end time in seconds to be displayed.
        """
        time_string = self.time_to_string(time_in_seconds)
        self.var_end_time.set(time_string)

    def set_break_time(self, time_in_seconds):
        """
        Sets the break time in this widget.

        Parameters
        ----------
        time_in_seconds : int
            The break time in seconds to be displayed.
        """
        time_string = self.time_to_string(time_in_seconds)
        self.var_break_time.set(time_string)

    def set_total_time(self, time_in_seconds):
        """
        Sets the total working time in this widget.

        Parameters
        ----------
        time_in_seconds : int
            The total working time in seconds to be displayed.
        """
        time_string = self.time_to_string(time_in_seconds)
        self.var_total_time.set(time_string)

    def time_to_string(self, time=-1):
        """
        Converts time in seconds to a string formatted as "HH:MM".

        Parameters
        ----------
        time : int, optional
            The time in seconds to convert. Default is -1, which
            returns "--:--" as any value outside of range(0, 24*60*60-1).

        Returns
        -------
        str
            The formatted time string.
        """
        time_string = "--:--"

        if 0 <= time <= 24 * 60 * 60 - 1:
            time = time // 60
            minutes = time % 60
            hours = time // 60

            time_string = f"{hours:02}:{minutes:02}"

        return time_string
