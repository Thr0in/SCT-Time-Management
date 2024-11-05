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
import calendar


class DayWidget(tk.Button):
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
                 relief='solid').grid(sticky="nw", row=0, column=0)

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


class CalendarHeader(tk.Frame):
    """
    A header frame for the calendar widget, containing navigation buttons.

    Methods
    -------
    __init__(parent)
        Initializes the header with navigation buttons
        and a label for the month.
    """

    def __init__(self, parent):
        """
        Constructs the CalendarHeader, including navigation
        and display elements.

        Parameters
        ----------
        parent : widget
            The parent widget in which this header widget will be placed.
        """
        super().__init__(master=parent, relief="solid", borderwidth=1)

        tk.Button(self, text="<").grid(column=0, row=0)
        tk.Button(self, text=">").grid(column=2, row=0)

        self.var_selected_month = tk.StringVar(value="Month YYYY")
        tk.Label(self, textvariable=self.var_selected_month).grid(column=1,
                                                                  row=0)


class CalendarContent(tk.Frame):
    """
    The main content area of the calendar widget, containing day widgets.

    Methods
    -------
    __init__(parent)
        Initializes the calendar grid with day widgets.
    """

    def __init__(self, parent):
        """
        Constructs the CalendarContent with day labels
        and DayWidget instances.

        Parameters
        ----------
        parent : widget
            The parent widget in which this calendar
            content widget will be placed.
        """

        super().__init__(master=parent, relief="solid", borderwidth=1, padx=10,
                         pady=10)

        self.days = [0] * 35

        for i in range(0, 7):
            day = calendar.day_name[i]
            tk.Label(self, text=day).grid(row=0, column=i)

        for i in range(0, 35):
            self.days[i] = DayWidget(self)
            day = self.days[i]
            day.grid(row=i // 7 + 1, column=i % 7, padx=5, pady=5)
            day.set_day_number(i)


class CalendarWidget(tk.Frame):
    """
    A calendar widget containing a header and content with day elements.

    Methods
    -------
    __init__(parent)
        Initializes the CalendarWidget with header and content.
    """

    def __init__(self, parent):
        """
        Constructs all necessary attributes for the CalendarWidget object.

        Parameters
        ----------
        parent : widget
            The parent widget in which this calendar widget will be placed.
        """
        super().__init__(master=parent, relief="solid", borderwidth=1)

        self.header = CalendarHeader(self)
        self.content = CalendarContent(self)

        self.header.pack(expand=True, fill=tk.BOTH)
        self.content.pack()


class SideBar(tk.Frame):
    """
    A sidebar component containing action buttons and an information panel.

    Methods
    -------
    __init__(parent)
        Initializes the sidebar with buttons and an information panel.
    """

    def __init__(self, parent):
        """
        Constructs the SideBar with vacation and time logging buttons.

        Parameters
        ----------
        parent : widget
            The parent widget in which this sidebar will be placed.
        """

        super().__init__(master=parent, bg="azure3", padx=20, pady=20)

        self.info_panel = InfoPanel(self)

        button_request_vacation = tk.Button(self, text="Request Vacation")
        button_log_working_time = tk.Button(self, text="Start Workday")
        button_log_break_time = tk.Button(self, text="Start BreaK")

        self.info_panel.pack(fill=tk.X, pady=5)
        button_request_vacation.pack(side="top", fill=tk.X, pady=5)
        button_log_break_time.pack(side="bottom", fill=tk.X, pady=5)
        button_log_working_time.pack(side="bottom", fill=tk.X, pady=5)


class InfoPanel(tk.Frame):
    """
    A panel for displaying user information such as
    flex time and vacation days.

    Methods
    -------
    __init__(parent)
        Initializes the information panel with labels for user status.
    """

    def __init__(self, parent):
        """
        Constructs the InfoPanel to display flex time and vacation details.

        Parameters
        ----------
        parent : widget
            The parent widget in which this information panel will be placed.
        """

        super().__init__(master=parent, padx=10, pady=10,
                         borderwidth=1, relief="solid")

        self.var_flex_time = tk.StringVar(value="+ 27:13")
        self.var_vacation_days = tk.StringVar(value=17)
        self.var_old_vacation_days = tk.StringVar(value=0)

        tk.Label(self, text="Flex-Time:").pack(anchor="nw")
        tk.Label(self, textvariable=self.var_flex_time).pack(anchor="nw")

        tk.Label(self, text="Remaining vacation days:").pack(anchor="nw")
        tk.Label(self, textvariable=self.var_vacation_days).pack(anchor="nw")

        tk.Label(self, text="Vacation from last year:").pack(anchor="nw")
        tk.Label(
            self, textvariable=self.var_old_vacation_days).pack(anchor="nw")
