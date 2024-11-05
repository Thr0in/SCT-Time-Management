# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 15:58:42 2024

@author: Luka
"""
import tkinter as tk
import calendar
from day_widget import DayWidget


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
