# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 16:17:50 2024
test
@author: Luka
"""

import datetime as dt
import os.path
import csv

from datetime_functions import DatetimeFunctions
import gui_constants


class WorkingDay():
    """
    A class representing a working day for an employee.

    Attributes
    ----------
    start_time : datetime.time or None
        Start time as a time object or None if not set.
    end_time : datetime.time or None
        End time as a time object or None if not set.
    break_time : int or None
        Break time in seconds or None if not set.
    state : str
        The state of the day, e.g., "default", "sick", or "vacation".
    date : datetime.date
        The date for this working day.
    """


    def __init__(self, date_object):
        """
        Initializes a WorkingDay with default attributes.

        Parameters
        ----------
        date_object : datetime.date
            The date associated with this working day.
        """
        self.start_time = None
        self.end_time = None
        self.break_time = None

        self.state = "default"

        self.date = date_object


class WorkTimeEmployee():
    """
    A class for managing an employee's work time, including working days,
    vacation days, and flex time calculations.

    Attributes
    ----------
    employee_id : str
        The unique ID for the employee.
    file_path : str
        The path to the employee's timesheet file.
    working_days : dict
        A dictionary mapping date strings to WorkingDay instances.
    amount_vacation_days : int
        Total vacation days available to the employee.
    amount_vacation_days_old : int
        Unused vacation days carried over from the previous year.

    Methods
    -------
    create_day(date_object=dt.date.today())
        Creates a new WorkingDay for a given date.
    get_day(date_object=dt.date.today())
        Retrieves a WorkingDay for the specified date.
    get_flex_time()
        Calculates the employee's accumulated flex time in seconds.
    load_working_days()
        Loads the working days data from a CSV file.
    save_working_days()
        Saves the working days data to a CSV file.
    """

    def __init__(self, employee_id="default"):
        """
        Initializes a WorkTimeEmployee object with a given employee ID.

        Parameters
        ----------
        employee_id : str, optional
            The unique ID of the employee (default is "default").
        """
        self.employee_id = employee_id
        self.file_path = self.employee_id + ".csv"

        self.working_days = {}
        self.amount_vacation_days = 30
        self.amount_vacation_days_old = 0

        if os.path.isfile(self.file_path):
            self.load_working_days()
        else:
            self.save_working_days()

    def create_day(self, date_object=dt.date.today()):
        """
        Creates a new WorkingDay instance for the specified date and adds
        it to the working_days dictionary.

        Parameters
        ----------
        date_object : datetime.date, optional
            The date for which to create a new WorkingDay (default is today).

        Returns
        -------
        WorkingDay
            The newly created WorkingDay instance.
        """
        if "{:%Y%m%d}".format(date_object) in self.working_days:
            day = self.working_days["{:%Y%m%d}".format(date_object)]
        else:
            day = WorkingDay(date_object)
            self.working_days["{:%Y%m%d}".format(date_object)] = day

        return day

    def get_day(self, date_object=dt.date.today()):
        """
        Retrieves the WorkingDay instance for the specified date.

        Parameters
        ----------
        date_object : datetime.date, optional
            The date for which to retrieve the WorkingDay (default is today).

        Returns
        -------
        WorkingDay
            The WorkingDay instance for the specified date.
        """
        day = self.working_days["{:%Y%m%d}".format(date_object)]
        return day

    def get_flex_time(self):
        """
        Calculates the flex time for the employee by summing the difference
        between start and end times, adjusting for break time, and deducting
        the expected daily working hours in seconds.

        Returns
        -------
        int
            The calculated flex time in seconds.
        """
        flex_time = 0

        for day in self.working_days.values():
            if day.start_time is not None and day.end_time is not None:
                flex_time += DatetimeFunctions.get_time_difference(
                    self, day.start_time, day.end_time)

                if day.break_time is not None:
                    flex_time += day.break_time

# Deduct expected daily working hours if the day is not "sick" or "vacation"
            if day.state not in ("sick", "vacation"):
                flex_time -= (gui_constants.DAILY_WORKING_HOURS * 3600)

        return flex_time

    def load_working_days(self):
        """
        Saves the working_days dictionary to a CSV file with columns 'Date',
        'Start Time', 'End Time', 'Break Time', and 'State'.
        """
        if gui_constants.USE_DATABASE:
            print("Accessing database...")
        else:
            try:
                with open(self.file_path, 'r') as csvfile:
                    reader = csv.DictReader(csvfile)

                    for row in reader:
                        date_object = dt.datetime.strptime(row['Date'], '%Y%m%d')
                        day = self.create_day(date_object)

                        day.start_time = DatetimeFunctions.convert_string_to_time(self, row['Start Time']) if row['Start Time'] else None
                        day.end_time = DatetimeFunctions.convert_string_to_time(self, row['End Time']) if row['End Time'] else None
                        day.break_time = int(
                            row['Break Time']) if row['Break Time'] else None
                        day.state = row['State']

            except Exception as e:
                print("Error", f"Failed to load timesheet: {e}")

    def save_working_days(self):
        """
        Saves the working_days dictionary to a CSV file with columns 'Date',
        'Start Time', 'End Time', 'Break Time', and 'State'.
        """
        if gui_constants.USE_DATABASE:
            print("Accessing database...")
        else:
            with open(self.file_path, 'w', newline='') as csvfile:

                fieldnames = ['Date', 'Start Time',
                              'End Time', 'Break Time', 'State']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()
                for date_string, day in self.working_days.items():
                    writer.writerow({
                        'Date': date_string,
                        'Start Time': day.start_time.strftime('%H:%M'),
                        'End Time': day.end_time.strftime('%H:%M'),
                        'Break Time': day.break_time,
                        'State': day.state
                    })


# Testing the data model
if __name__ == "__main__":
    test = WorkTimeEmployee()
    test.create_day()
    # today = test.get_day(dt.date.today())
    # today.start_time = dt.datetime.now().time() # 8 AM in seconds
    # today.end_time = dt.datetime.now().time().replace(hour=16)  # 4 PM in seconds
    # today.state = "sick"

    test.save_working_days()
    print(list(test.working_days.items()))
    print("Flex time (seconds):", test.get_flex_time())
