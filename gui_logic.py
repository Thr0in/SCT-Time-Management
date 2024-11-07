# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 21:49:00 2024

This module provides the main graphical user interface (GUI) logic for the
SCT time management application.
It creates a `Timesheet` application window containing a calendar and sidebar,
allowing users to navigate and interact with their monthly timesheets.

Classes:
--------
Timesheet
    The main application window for the timesheet, featuring a calendar widget
    for date selection and a sidebar for additional options and data display.

Functions:
----------
get_month_days(date_object)
    Returns the days in the month as a flattened list of integers, including
    padding days to create a 6x7 grid.

change_color(color, container=None)
    Changes the background color of a container widget
    and all its child widgets.

select_month(date_object=date.today())
    Updates the calendar display based on the selected month,
    highlighting the current day if applicable.

@author: Luka, jnath
"""
import tkinter as tk
import calendar
from datetime import date

from calendar_widget import CalendarWidget
from side_bar import SideBar
from data_model import WorkTimeEmployee
import gui_constants


class Timesheet:
    """
    The main application window for the timesheet.

    This class creates a window with a calendar widget for selecting dates,
    and a sidebar for displaying related options and information.

    Attributes
    ----------
    selected_date : date
        Stores the currently selected date.
    root : Tk
        The root window for the application.
    calendar : CalendarWidget
        The main calendar widget for date navigation and time tracking.
    side_bar : SideBar
        A sidebar widget for additional options and data display.

    Methods
    -------
    __init__()
        Initializes the timesheet application with the calendar and sidebar.
    get_month_days(date_object)
        Returns a flat list of day numbers for the specified month,
        with padding days to form a complete 6x7 grid.
    change_color(color, container=None)
        Recursively changes the background color of a widget and its children.
    select_month(date_object=date.today())
        Updates the calendar display to reflect the selected
        month and highlights the current date if applicable.
    """

    def __init__(self):
        """
        Initializes the Timesheet application
        window with a calendar and sidebar.
        Sets the window dimensions, initializes the
        selected date, and starts the main loop.
        """
        self.selected_date = date.today()
        self.root = tk.Tk()
        self.root.geometry('1100x730')

        self.calendar = CalendarWidget(self.root, self)
        self.side_bar = SideBar(self.root)

        self.side_bar.pack(side="left", expand=True, fill=tk.BOTH)
        self.calendar.pack(side="top", expand=True, fill=tk.Y)

        self.employees = {}

        self.select_month()

        self.add_employee("default")

        self.root.mainloop()

    def add_employee(self, employee_id):
        self.employees[employee_id] = WorkTimeEmployee(employee_id)

    def get_month_days(self, date_object):
        """
        Generates a list of days for a given month with padding
        to complete a 6x7 grid.

        Parameters
        ----------
        date_object : date
            The date object representing the month to retrieve days for.

        Returns
        -------
        list
            A list of integers representing the days of the month,
            with 0s for padding.
        """
        month_days = calendar.monthcalendar(date_object.year,
                                            date_object.month)
        month_days_flat = sum(month_days, [])
        return month_days_flat[:42] + [0]*(42 - len(month_days_flat))

    def change_color(self, color, container=None):
        """
        Recursively changes the background color of a widget
        and its child widgets.

        Parameters
        ----------
        color : str
            The color to apply to the widget background.
        container : widget, optional
            The widget container whose background color will be changed.
            If not provided, defaults to the root widget.
        """
        if container is None:
            container = self.root  # set to root window
        container.config(bg=color)
        for child in container.winfo_children():
            child.config(bg=color)
            if child.winfo_children():
                # child has children, go through its children
                self.change_color(color, child)

    def hide_empty_row(self):
        month_days_flat = sum(calendar.monthcalendar(
            self.selected_date.year, self.selected_date.month), [])
        if len(month_days_flat) <= 35:
            for i in range(35, 42):
                self.calendar.content.days[i].grid_remove()
        else:
            for i in range(35, 42):
                self.calendar.content.days[i].grid()

    def select_month(self, date_object=date.today()):
        """
        Updates the calendar to display the days of the selected month.

        Highlights the current day if it falls within the displayed month.

        Parameters
        ----------
        date_object : date, optional
            The date object representing the month to display.
            Defaults to today.
        """
        if date_object == "self.selected_date":
            date_object = self.selected_date
        else:
            self.selected_date = date_object

        self.calendar.header.var_selected_month.set(
            self.selected_date.strftime("%B %Y"))

        month_days = self.get_month_days(date_object)

        for day, month_day in zip(self.calendar.content.days, month_days):
            day.var_day.set(month_day)

            if month_day == 0:
                day.var_day.set('')
                self.change_color(gui_constants.DISABLED_COLOR, day)

            elif (self.selected_date.year == date.today().year and
                  self.selected_date.month == date.today().month and
                    month_day == date.today().day):
                self.change_color(gui_constants.HIGHLIGHT_COLOR, day)

            else:
                self.change_color('SystemButtonFace', day)
        self.hide_empty_row()


# Testing GUI
if __name__ == "__main__":
    app = Timesheet()
