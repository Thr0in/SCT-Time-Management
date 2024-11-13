# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 21:49:00 2024

This module provides the main graphical user interface (GUI) logic for the
STC time management application.
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

@author: Luka, jnath, lpasd, Tim, Danny
"""
import tkinter as tk
import calendar
from datetime import date
import os.path
import csv
import dateutil.relativedelta as rdelta
import sqlite3

from data_model import WorkTimeEmployee
from datetime_functions import DatetimeFunctions as dtf
from login import LoginFrame
import gui
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
    employees : dict
        Dictionary storing `WorkTimeEmployee` instances, keyed by employee ID.
    current_employee : WorkTimeEmployee
        The employee currently selected and whose data is displayed.

    Methods
    -------
    __init__()
        Initializes the timesheet application with the calendar and sidebar.
    on_closing()
        Saves the working days of all employees and closes the application.
    print_day(day)
        Prints start time, end time, break time, date, and state of a given
        working day if debugging is enabled.
    update_info_panel()
        Updates the flex- and vacation day information in the sidebar.
    update_from_db()
        Loads and updates calendar entries from the data model.
    add_employee(employee_id)
        Adds an employee with a given ID to the application.
    get_month_days(date_object)
        Returns a list of day numbers for the specified month,
        padded to create a complete 6x7 grid.
    change_color(color, container=None)
        Recursively changes the background color of a widget and its children.
    hide_empty_row()
        Hides the last row of the calendar if the month has fewer than 36 days.
    select_month(date_object=date.today())
        Updates the calendar to reflect the selected month and
        highlights the current date if within the displayed month.
    log_work_time()
        Logs the start or end time of the current workday
        and updates the display.
    log_break_time()
        Logs the start or end time of a break period and updates the display.
    update_buttons()
        Updates button labels in the sidebar based on
        the employee’s work state.
    """

    def __init__(self):
        """
        Construct a timesheet object.

        Initializes the Timesheet application
        window with a calendar and sidebar.
        Sets window dimensions, initializes
        selected date, adds a default employee,
        and starts the main loop.

        Falls back to csv files if no database shall be used.
        """
        if not gui_constants.USE_DATABASE:
            gui_constants.IMPORT_FROM_CSV = True

        self.run()

    def run(self):
        """Create the main window provided by the os' window manager."""
        self.selected_date = date.today()
        self.root = tk.Tk()

        self.create_login_window()

        if gui_constants.AUTO_LOGIN:
            self.login('default')

        self.root.mainloop()

    def create_login_window(self):
        """
        Create login window.

        Creates the login window and prepares important
        attributes for the timesheet.
        """
        for widget in self.root.winfo_children():
            widget.destroy()

        window_pos_x = (self.root.winfo_screenwidth()-300)/2
        window_pos_y = (self.root.winfo_screenheight()-200)/2

        self.root.title("Login Screen")
        self.root.minsize(300, 200)
        self.root.geometry('300x200+%d+%d' % (window_pos_x, window_pos_y))
        self.root.protocol("WM_DELETE_WINDOW", lambda: self.on_closing())

        try:
            os.mkdir(gui_constants.DATA_PATH)
        except FileExistsError:
            print("Tried to create '~/data' folder but it exists already.")
        except OSError as error:
            print(error)

        self.employees = {}
        self.file_path_employees = os.path.join(
            gui_constants.DATA_PATH, "employees.csv")
        if os.path.isfile(self.file_path_employees) or os.path.isfile(gui_constants.DATABASE_PATH):
            self.load_employees()
        else:
            self.save_employees()
        self.current_employee = None

        self.login_frame = LoginFrame(self.root, self)
        self.login_frame.pack(expand=True, fill=tk.BOTH)

        self.root.bind('<Return>', self.login_frame.login)

    def create_timesheet_window(self):
        """Create the timesheet widgets and initializes them."""
        self.login_frame.pack_forget()

        window_size_x = self.root.winfo_screenwidth()/2
        window_size_y = self.root.winfo_screenheight()/2
        window_pos_x = (self.root.winfo_screenwidth()-window_size_x)/2
        window_pos_y = (self.root.winfo_screenheight()-window_size_y)/2

        self.root.title("STC Timesheet Calendar")
        self.root.geometry('%dx%d+%d+%d' % (window_size_x,
                           window_size_y, window_pos_x, window_pos_y))
        self.root.minsize(1280, 720)
        self.root.protocol("WM_DELETE_WINDOW", lambda: self.on_closing())

        self.gui = gui.MainApp(self.root, self)
        self.gui.pack(expand=True, fill=tk.BOTH)

        self.change_color(gui_constants.DEFAULT_COLOR,
                          self.gui.sidebar.info_panel)
        self.select_month()

        self.gui.top_bar.employee_name.set(self.current_employee.name)
        self.gui.top_bar.role.set(self.current_employee.role)

        day = self.current_employee.get_day(date.today())
        self.print_day(day)

        self.root.bind('<Return>', self.update)

    def login(self, user, role='Employee', name='default'):
        """
        Log in a user.

        Has to exist in userdata.txt

        Parameters
        ----------
        user : str
            Username/employee_id.
        """
        self.add_employee(user)
        self.current_employee = self.employees.get(user)
        self.current_employee.role = role
        self.current_employee.name = name

        self.current_employee.load_working_days()

        self.create_timesheet_window()

    def logout(self):
        """Save all data and log out the current employee."""
        self.store_all_inputs()
        self.current_employee.save_working_days()

        self.current_employee = None
        self.save_employees()

        self.root.destroy()
        self.run()

    def update(self, event=None):
        """
        Update timesheet.

        Callback method for update button.
        """
        self.root.focus_set()
        self.update_info_panel()

    def request_vacation(self):
        """Request a vacation day."""
        if self.current_employee.amount_old_vacation_days > 0:
            self.current_employee.amount_old_vacation_days -= 1
        elif self.current_employee.amount_vacation_days > 0:
            self.current_employee.amount_vacation_days -= 1
        else:
            print("""You can't request a day off as
                  you don't have any vacation days left.""")
        self.update_info_panel()
        self.save_employees()

    def store_all_inputs(self):
        """Save all data of the selected month persistently on disk."""
        for day in self.gui.days:
            self.store_input_data(day)
        if not gui_constants.REDUCED_DATABASE_TRAFFIC:
            self.current_employee.save_working_days()

    def on_closing(self):
        """Save all employee working day data and closes the application."""
        if self.current_employee is not None:
            self.store_all_inputs()
            self.current_employee = None
        for employee in self.employees.values():
            employee.save_working_days()
        self.save_employees()
        self.root.destroy()

    def print_day(self, day, always_enabled=False):
        """
        Print the details of a given working day if debugging is enabled.

        Parameters
        ----------
        day : WorkingDay
            The working day object containing the day’s information.
        """
        if gui_constants.DEBUG or always_enabled:
            print(day.date, ":")
            print(day.start_time)
            print(day.end_time)
            print(day.break_time)
            print(day.state)

    def update_info_panel(self):
        """Update the flex-time and vacation day information in the sidebar."""
        panel = self.gui.sidebar.info_panel
        panel.var_flex_time.set(dtf.time_to_string(
            self, self.current_employee.get_flex_time(), unsigned=False))

        panel.var_vacation_days.set(self.current_employee.amount_vacation_days)
        panel.var_old_vacation_days.set(
            self.current_employee.amount_old_vacation_days)

    def purge_inputs(self):
        """Remove all data from all input fields."""
        for day in self.gui.days:
            day.set_start_time(None)
            day.set_end_time(None)
            day.set_break_time(None)
            day.set_total_time(None)

    def update_from_db(self):
        """
        Load and update the calendar from the current employee’s data model.

        For every day without entry, the fields
        are filled with gui_constants.NO_TIME_DATA.
        """
        if not gui_constants.REDUCED_DATABASE_TRAFFIC:
            self.current_employee.save_working_days()
            self.current_employee.load_working_days()
        for day in self.gui.days:
            current_date = day.date
            if current_date is not None:
                try:
                    work_day = self.current_employee.get_day(current_date)
                    day.set_start_time(work_day.start_time)
                    day.set_end_time(work_day.end_time)
                    day.set_break_time(work_day.break_time)
                    day.set_total_time(work_day.get_work_time())
                    self.print_day(work_day)  # Debug
                except Exception:
                    if gui_constants.DEBUG:
                        print("Error at day:" + day.var_day.get())

        self.update_info_panel()
        self.update_buttons()

    def get_old_date_of_day(self, day):
        """
        Return the date currently displayed by the specified DayWidget.

        Parameters
        ----------
        day : DayWidget
            The DayWidget display.

        Returns
        -------
        current_date : datetime.date
            The displayed date.

        """
        number_of_days = calendar.monthrange(self.selected_date.year,
                                             self.selected_date.month)[1]
        current_date = None
        if (day.var_day.get() != '' and
                int(day.var_day.get()) in range(1, number_of_days+1)):
            current_date = self.selected_date.replace(
                day=int(day.var_day.get()))

        return current_date

    def get_date_month_delta(self, month_delta):
        """
        Return a date with the same day as the selected date in another month.

        Parameters
        ----------
        month_delta : int
            How many months to subtract or add to the current date.

        Returns
        -------
        datetime.date
            The date object differing by month_delta
            months from the selected date.

        """
        return self.selected_date + rdelta.relativedelta(months=month_delta)

    def add_employee(self, employee_id):
        """
        Add an employee with the specified ID to the application.

        Parameters
        ----------
        employee_id : str
            Unique ID for the new employee.
        """
        if employee_id not in self.employees:
            self.employees[employee_id] = WorkTimeEmployee(employee_id)
        else:
            print("Employee with id '{e_id}' already in database.".format(
                e_id=employee_id))

    def get_month_days(self, date_object):
        """
        Return day numbers as list for a specified month, padded to a 6x7 grid.

        Parameters
        ----------
        date_object : date
            The date object representing the month.

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
        Change the background color of a widget and its children recursively .

        Parameters
        ----------
        color : str
            The color to apply to the widget background.
        container : widget, optional
            The widget container whose background color will be changed.
            Defaults to the root widget.
        """
        if container is None:
            container = self.root  # set to root window
        container.config(bg=color)
        for child in container.winfo_children():
            child.config(bg=color)
            if child.winfo_children():
                # child has children, go through its children
                self.change_color(color, child)

    def load_employees(self):
        """Load the list of employees from disk."""
        if gui_constants.USE_DATABASE:
            self.load_employees_from_database()
        if gui_constants.IMPORT_FROM_CSV:
            self.load_employees_from_csv()

    def load_employees_from_database(self):
        """Load employees and their vacation days from the database."""
        con = sqlite3.connect(gui_constants.DATABASE_PATH)
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS employees(
                        employee_id TEXT PRIMARY KEY,
                        vacation_days INTEGER,
                        old_vacation_days INTEGER)"""
                    )

        for row in cur.execute("""SELECT employee_id,
                                   vacation_days,
                                   old_vacation_days FROM employees"""):
            self.add_employee(row[0])
            employee = self.employees.get(row[0])
            employee.amount_vacation_days = int(
                row[1]) if row[1] else 30
            employee.amount_old_vacation_days = int(
                row[2]) if row[2] else 0
        con.close()

    def load_employees_from_csv(self):
        """Load employees and their vacation days from a csv file."""
        try:
            with open(self.file_path_employees, 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    self.add_employee(row['Employee ID'])

                    employee = self.employees.get(row['Employee ID'])
                    employee.amount_vacation_days = int(
                        row['Vacation Days']) if row['Vacation Days'] else 30
                    employee.amount_old_vacation_days = int(
                        row['Old Vacation Days']) if row['Old Vacation Days'] else 0

        except Exception as e:
            print("Error", f"Failed to load employees: {e}")

    def save_employees(self):
        """Save the list of employees to disk."""
        if gui_constants.USE_DATABASE:
            self.save_employees_to_database()
        if gui_constants.WRITE_TO_CSVS:
            self.save_employees_to_csv()

    def save_employees_to_database(self):
        """Save the list of employees and their vacation days to a csv file."""
        con = sqlite3.connect(gui_constants.DATABASE_PATH)
        cur = con.cursor()
        cur.execute(
            """CREATE TABLE IF NOT EXISTS
            employees(employee_id TEXT PRIMARY KEY,
            vacation_days INTEGER,
            old_vacation_days INTEGER)"""
        )

        for employee in self.employees.values():
            cur.execute("""INSERT OR REPLACE INTO employees(employee_id,
                        vacation_days,
                        old_vacation_days) VALUES (?, ?, ?)""",
                        (employee.employee_id,
                         employee.amount_vacation_days,
                         employee.amount_old_vacation_days)
                        )

        con.commit()
        con.close()

    def save_employees_to_csv(self):
        """Save the list of employees and their vacation days to a csv file."""
        with open(self.file_path_employees, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=[
                                    'Employee ID',
                                    'Vacation Days',
                                    'Old Vacation Days'
                                    ])
            writer.writeheader()
            for employee in self.employees.values():
                writer.writerow({
                    'Employee ID': employee.employee_id,
                    'Vacation Days': employee.amount_vacation_days,
                    'Old Vacation Days': employee.amount_old_vacation_days
                })

    def hide_empty_row(self):
        """
        Shrink calendar to minimum number of days.

        Conditionally hides the last row of the
        calendar if it contains only days of the next month.
        """
        if gui_constants.SHOW_ONLY_MINIMUM_DAYS:
            month_days_flat = sum(calendar.monthcalendar(
                self.selected_date.year, self.selected_date.month), [])
            if len(month_days_flat) <= 35:
                for i in range(35, 42):
                    self.gui.days[i].grid_remove()
            else:
                for i in range(35, 42):
                    self.gui.days[i].grid()

    def select_month(self, date_object=date.today()):
        """
        Update the calendar to show the selected month.

        Highlights the current day if it falls within the displayed month.

        Parameters
        ----------
        date_object : date, optional
            The date object representing the month to display.
            Defaults to today.
        """
        self.purge_inputs()
        if date_object == "self.selected_date":
            date_object = self.selected_date
        else:
            self.selected_date = date_object

        self.gui.var_selected_month.set(
            self.selected_date.strftime("%B %Y"))

        month_days = self.get_month_days(date_object)
        month_days_last = self.get_month_days(self.get_date_month_delta(-1))
        month_days_next = self.get_month_days(self.get_date_month_delta(1))

        leading_days = 0
        for i, day in enumerate(month_days):
            if day == 0:
                if i < 7:
                    leading_days += 1

        month_days_last = self.strip_zero_from_list(month_days_last)
        month_days_next = self.strip_zero_from_list(month_days_next)
        month_length = len(self.strip_zero_from_list(month_days))

        for i, (day, month_day) in enumerate(zip(self.gui.days, month_days)):
            day.var_day.set(month_day)
            current_date = self.get_old_date_of_day(day)

            if month_day == 0:
                if i < 7:
                    n = month_days_last[i - leading_days]
                    day.var_day.set(n)
                    current_date = self.get_date_month_delta(-1).replace(day=n)
                else:
                    n = month_days_next[i - (leading_days + month_length)]
                    day.var_day.set(n)
                    current_date = self.get_date_month_delta(1).replace(day=n)
                    # day.var_day.set('')
                self.change_color(gui_constants.DISABLED_COLOR, day)
                day.label_day.config(bg=gui_constants.WEEKEND_COLOR)

            elif (self.selected_date.replace(day=month_day) == date.today()):
                self.change_color(gui_constants.HIGHLIGHT_COLOR, day)
                day.label_day.config(bg=gui_constants.DEFAULT_COLOR)
                # day.config(bg=gui_constants.HIGHLIGHT_COLOR)

            else:
                self.change_color(gui_constants.DEFAULT_COLOR, day)
                if current_date.weekday() > 4:
                    self.change_color(gui_constants.WEEKEND_COLOR, day)
                day.label_day.config(bg=gui_constants.HIGHLIGHT_COLOR)

            day.date = current_date
        self.hide_empty_row()
        self.update_from_db()

    def strip_zero_from_list(self, array):
        """
        Return the provided list without any zeros.

        Parameters
        ----------
        array : list
            A  list possibly containing zeros.

        Returns
        -------
        list
            The input list without zeros.
        """
        return [value for value in array if value != 0]

    def log_work_time(self):
        """Log the start or end time of a workday and update the display."""
        self.store_all_inputs()
        today = self.current_employee.create_day()
        self.print_day(today)
        if today.start_time is None:
            today.start_time = dtf.get_current_time(self)
        else:
            if self.current_employee.on_break is not None:
                self.log_break_time()
            today.end_time = dtf.get_current_time(self)

        if not gui_constants.REDUCED_DATABASE_TRAFFIC:
            self.current_employee.save_working_days()
        self.update_from_db()

    def log_break_time(self):
        """
        Log the start or end time of a break period and update the display.

        As long as the workday is not ended, an
        arbitrary amount of breaks can be entered.
        """
        self.store_all_inputs()
        if self.current_employee.get_day().start_time is None:
            print("You can't take a break before you start to work.")
        elif self.current_employee.get_day().end_time is not None:
            print("You can't take a break after you've finished work.")
        elif self.current_employee.on_break is None:
            self.current_employee.on_break = dtf.get_current_time(self)
        else:
            break_start = self.current_employee.on_break
            break_end = dtf.get_current_time(self)
            break_time = dtf.get_time_difference(self, break_start, break_end)
            try:
                self.current_employee.get_day().break_time += break_time
            except TypeError:
                self.current_employee.get_day().break_time = break_time

            self.current_employee.on_break = None

        if not gui_constants.REDUCED_DATABASE_TRAFFIC:
            self.current_employee.save_working_days()
        self.update_from_db()

    def update_buttons(self):
        """Update button labels in the sidebar based on current work state."""
        if self.current_employee.on_break is not None:
            button_label_break = "End Break"
        else:
            button_label_break = "Start Break"
        self.gui.sidebar.button_log_break.config(text=button_label_break)

        if self.current_employee.create_day().start_time is None:
            button_label_time = "Start Workday"
        elif self.current_employee.create_day().end_time is None:
            button_label_time = "End Workday"
        else:
            button_label_time = "Update Endtime"
        self.gui.sidebar.button_log_work.config(text=button_label_time)

    def store_input_data(self, day):
        """
        Store input data of given day widget.

        Stores all present data from the given days input
        fields in the internal data model
        Parameters
        ----------
        day : DayWidget
            The day widget which data to store.
        """
        current_date = day.date
        if current_date is not None:
            try:
                work_day = self.current_employee.create_day(current_date)
                try:
                    work_day.start_time = dtf.convert_string_to_time(
                        self, day.var_start_time.get())
                    if gui_constants.DEBUG:
                        print(work_day.start_time)
                except Exception:
                    if gui_constants.DEBUG:
                        print("No data in start_time")
                try:
                    work_day.end_time = dtf.convert_string_to_time(
                        self, day.var_end_time.get())
                    if gui_constants.DEBUG:
                        print(work_day.end_time)
                except Exception:
                    if gui_constants.DEBUG:
                        print("No data in end_time")

                try:
                    break_time = dtf.convert_string_to_time(
                        self, day.var_break_time.get())
                    break_time = dtf.time_in_seconds(self, break_time)
                    if break_time > 59:
                        work_day.break_time = break_time
                    if gui_constants.DEBUG:
                        print(work_day.break_time)
                except Exception as e:
                    if gui_constants.DEBUG:
                        print("No data in break_time", e)

                day.set_total_time(work_day.get_work_time())
            except AttributeError as e:
                print(e)  # pass

            if not gui_constants.REDUCED_DATABASE_TRAFFIC:
                self.current_employee.save_working_days()
            self.update_buttons()

    def delete_input_data(self, day):
        """
        Delete data from internal memory.

        Delete all missing data in the given days input
        fields from the internal data model
        Parameters
        ----------
        day : DayWidget
            The day widget which data to delete.
        """
        current_date = day.date
        if current_date is not None:
            work_day = self.current_employee.create_day(current_date)
            if day.var_start_time.get() in (gui_constants.NO_TIME_DATA, ''):
                if gui_constants.DEBUG:
                    print(day.var_day.get(), 'start', day.var_start_time.get())
                work_day.start_time = None

            if day.var_end_time.get() in (gui_constants.NO_TIME_DATA, ''):
                if gui_constants.DEBUG:
                    print(day.var_day.get(), 'end', day.var_end_time.get())
                work_day.end_time = None

            if day.var_break_time.get() in (gui_constants.NO_TIME_DATA, ''):
                if gui_constants.DEBUG:
                    print(day.var_day.get(), 'break', day.var_break_time.get())
                work_day.break_time = None

            day.set_total_time(work_day.get_work_time())
            if not gui_constants.REDUCED_DATABASE_TRAFFIC:
                self.current_employee.save_working_days()
            self.update_buttons()


# Testing GUI
if __name__ == "__main__":
    # gui_constants.DEBUG = True
    app = Timesheet()
