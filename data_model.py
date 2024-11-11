# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 16:17:50 2024

@author: Luka, jnath
"""

import datetime as dt
import os.path
import csv
import sqlite3

from database_functions import DatabaseFunctions
from datetime_functions import DatetimeFunctions as dtf
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

    def get_work_time(self):
        """
        Returns the seconds worked on this day if calculatable by
        subtracting self.start_time from self.end_time. Subtracts
        the self.break_time if set.
        In all other cases it will return None.

        Returns
        -------
        work_time : int or None
            This days working time in seconds or None if not set.

        """
        work_time = None
        # if self.start_time is not None and self.end_time is not None:
        try:
            work_time = dtf.get_time_difference(
                self, self.start_time, self.end_time)

            if self.break_time is not None:
                work_time -= self.break_time
        except Exception as e:
            if gui_constants.DEBUG:
                print(
                    "An error occured while calculating worktime for day {:%Y-%m-%d}: ".format(self.date), e)
            pass
        return work_time

    def has_entry(self):
        """
        Checks wether this day has any data stored besides its date.

        Returns
        -------
        has_entry : bool
            True if this day contains data.

        """
        has_entry = False
        if self.start_time is not None:
            has_entry = True
        if self.end_time is not None:
            has_entry = True
        if self.break_time is not None:
            has_entry = True
        if self.state != "default":
            has_entry = True
        return has_entry


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
    amount_old_vacation_days : int
        Unused vacation days carried over from the previous year.
    on_break : datetime.time
        A timestamp which indicates when this employee started it's last break.
        Is None if this employee is not on break currently.

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
        self.name = 'default'
        self.role = 'employee'
        self.file_path = os.path.join(
            gui_constants.DATA_PATH, self.employee_id + ".csv")

        self.working_days = {}
        self.amount_vacation_days = 30
        self.amount_old_vacation_days = 0
        self.on_break = None

        if os.path.isfile(self.file_path):
            self.load_working_days()
        else:
            self.save_working_days()

    def create_day(self, date_object=dt.date.today()):
        """
        Creates a new WorkingDay instance for the specified date and adds
        it to the working_days dictionary. If a working day already exists
        for this date, this day will be passed instead.

        Parameters
        ----------
        date_object : datetime.date, optional
            The date for which to create a new WorkingDay (default is today).

        Returns
        -------
        WorkingDay
            The WorkingDay instance for the specified date.
        """
        day = self.get_day(date_object)
        if day.date is None:
            day = WorkingDay(date_object)
            try:
                self.working_days["{:%Y-%m-%d}".format(date_object)] = day
            except TypeError:
                raise TypeError("Cannot create day with date None")
                pass

        return day

    def get_day(self, date_object=dt.date.today()):
        """
        Retrieves the WorkingDay instance for the specified date.

        If there is no WorkingDay for the specified date yet,
        a None-Day will be passed. All its attributes are NoneTypes
        and will not be stored.

        Parameters
        ----------
        date_object : datetime.date, optional
            The date for which to retrieve the WorkingDay (default is today).

        Returns
        -------
        WorkingDay
            The WorkingDay instance for the specified date.
        """
        if "{:%Y-%m-%d}".format(date_object) in self.working_days:
            day = self.working_days.get("{:%Y-%m-%d}".format(date_object))
        else:
            day = WorkingDay(None)
        return day

    def get_flex_time(self):
        """
        Calculates the flex time for the employee by summing the daily
        work hours and deducting the expected daily working hours in seconds.

        Returns
        -------
        int
            The calculated flex time in seconds.
        """
        flex_time = 0

        for day in self.working_days.values():
            if day.has_entry():
                flex_time += float(day.get_work_time() or 0)

# Deduct expected daily working hours if the day is not "sick" or "vacation"
                if day.state not in ("sick", "vacation") and day.date.weekday() < 5:
                    flex_time -= (gui_constants.DAILY_WORKING_HOURS * 3600.0)
        return flex_time

    def load_working_days(self):
        """
        Saves the working_days dictionary to a CSV file with columns 'Date',
        'Start Time', 'End Time', 'Break Time', and 'State'.
        """
        if gui_constants.USE_DATABASE:
            #print("Accessing database...")

            try:
                # Create connection to the database
                db = DatabaseFunctions()
                db.connect_to_database()
                
                # Query to get all working days from the timesheet table for the employee
                db.c.execute('''SELECT date, starttime, endtime, breaktime, state FROM timesheet
                                WHERE employee_id = ?''', (self.employee_id,))
            
                # Fetch all results
                rows = db.c.fetchall()
            
                # Populate the working_days dictionary
                for row in rows:
                    date_object = dtf.convert_string_to_date(self, row[0])  # Convert date string to datetime
                    day = self.create_day(date_object)
            
                    # Handle start_time and end_time by extracting time from datetime string
                    day.start_time = dtf.convert_string_to_time_from_datetime(self, row[1]) if row[1] else None
                    day.end_time = dtf.convert_string_to_time_from_datetime(self, row[2]) if row[2] else None
                    
                    # Handle break_time
                    day.break_time = float(row[3]) if row[3] else None
                    
                    # Handle state
                    day.state = row[4]
            
            # Catch possible errors
            except sqlite3.Error as e:
                print(f"Error loading working days from the database: {e}")
            
            # Ensure database connection is closed even in case of error
            finally:
                db.disconnect_from_database()

        else:
            try:
                with open(self.file_path, 'r') as csvfile:
                    reader = csv.DictReader(csvfile)

                    for row in reader:
                        date_object = dtf.convert_string_to_date(
                            self, row['Date'])
                        day = self.create_day(date_object)

                        day.start_time = dtf.convert_string_to_time(
                            self, row['Start Time']) if row['Start Time'] else None
                        day.end_time = dtf.convert_string_to_time(
                            self, row['End Time']) if row['End Time'] else None
                        day.break_time = float(
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
            #print("Accessing database...")

            try: 
                # Create connection to the 
                # Important: use instance -> db=...
                db = DatabaseFunctions()
                db.connect_to_database()
            
                # Save data to database
                for date_string, day in self.working_days.items():
                    # Ensure that the day has data before saving
                    if day.has_entry():  
                        # Ensure breaktime is valid, set to None if less than 15 minutes
                        if day.break_time is not None and day.break_time < 15:
                            day.break_time = None
                        
                        # Insert or update the database
                        db.insert_into_database(
                            self.employee_id, 
                            date_string,
                            day.start_time,
                            day.end_time,
                            day.break_time,
                            day.state  
                        )
                        
            # Catch possible errors
            except sqlite3.Error as e:
                print(f"Error saving working days to the database: {e}")
            
            # Ensure database connection is closed even in case of error
            finally:
                db.disconnect_from_database()

        else:
            with open(self.file_path, 'w', newline='') as csvfile:

                fieldnames = ['Date', 'Start Time',
                              'End Time', 'Break Time', 'State']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()
                for date_string, day in self.working_days.items():
                    if day.has_entry():
                        if day.break_time is not None and day.break_time < 60:
                            day.break_time = None
                        writer.writerow({
                            'Date': date_string,
                            'Start Time': dtf.time_object_to_string(self, day.start_time),
                            'End Time': dtf.time_object_to_string(self, day.end_time),
                            'Break Time': day.break_time,
                            'State': day.state
                        })


# Testing the data model
if __name__ == "__main__":
    test = WorkTimeEmployee()
    test.create_day()

    test_saving = True

    if test_saving:
        today = test.get_day(dt.date.today())
        today.start_time = dt.datetime.now().time().replace(
            hour=dt.datetime.now().hour - 7)  # 7 hours earlier than .now()
        today.end_time = dt.datetime.now().time()  # .now()

        today.state = "default"

    test.save_working_days()
    print(list(test.working_days.items()))
    print("Flex time (seconds):", test.get_flex_time())
