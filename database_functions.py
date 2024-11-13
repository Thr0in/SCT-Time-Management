# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 08:34:07 2024

@author: jnath, Luka
"""
# Database Function Module

import sqlite3
import datetime

from datetime_functions import DatetimeFunctions
import gui_constants

# ------------------------------------------------------------------------------


class DatabaseFunctions:

    # Create Connection to database
    def connect_to_database(self):
        # Create or connect to a SQLite database
        # (the database file will be created if it doesn't exist yet)
        self.conn = sqlite3.connect(gui_constants.DATABASE_PATH)
        # 'timesheet.db' is the file name
        # Create a cursor object to interact with the database
        self.c = self.conn.cursor()

        # conn and c should be instance attributes of the class, so it can be used across different methods 
        # -> self.conn / self.c

        # Create a table (if it doesn't already exist)
        with self.conn:
            # with: Automatically commits/rollbacks transactions
            self.c.execute('''
                CREATE TABLE IF NOT EXISTS timesheet (
                    employee_id TEXT,
                    date DATE,
                    starttime DATETIME,
                    endtime DATETIME,
                    workhours REAL,
                    breaktime REAL,
                    state TEXT
                )
            ''')

    # ------------------------------------------------------------------------------

    # Insert data into the table
    # work with default parameters because python does not support overloading
    def insert_into_database(self, employee_id, date, starttime, endtime=None, breaktime=None, state='default'):
        # Inserts a new record into the timesheet table.
        # - date: The date of the work entry (required).
        # - starttime: The start time of the work (required).
        # - endtime: The end time of the work (optional, can be None).
        # - breaktime: The break time (optional, can be None).
        # - state: sick day or normal working day (default: 'default')

        # Try to insert data into databse
        try:
            # Convert strings to datetime objects if needed
            if isinstance(date, str):
                date = DatetimeFunctions.convert_string_to_date(self, date)
            if isinstance(starttime, str):
                starttime = DatetimeFunctions.convert_string_to_time(
                    self, starttime)
            if isinstance(endtime, str) and endtime:  # only converts if endtime exists
                endtime = DatetimeFunctions.convert_string_to_time(
                    self, endtime)

            # As datetime.time() objects are not supported in database table:
            # Conevert to full datetime object by merging with the passed date before inserting into table
            if isinstance(starttime, datetime.time):
                starttime = DatetimeFunctions.merge_date_and_time_to_datetime(
                    self, date, starttime)
            if isinstance(endtime, datetime.time):
                endtime = DatetimeFunctions.merge_date_and_time_to_datetime(
                    self, date, endtime)

            # Calculate Workhours if starttime and endtime exist
            # If no start or end time are logged, then the workhours are None
            if starttime is None or endtime is None:
                workhours = None
            # If both start and end time are logged, then calculate the time difference
            else:
                workhours = DatetimeFunctions.get_time_difference(
                    self, starttime, endtime)
                # convert workhours to full datetime object, so they can be stored in the table
                if isinstance(workhours, datetime.time):
                    workhours = DatetimeFunctions.merge_date_and_time_to_datetime(
                        self, date, workhours)

            # Check if an entry for the passed date already exists,
            # If so, update the entry instead of creating a new one

            # Check if employee and date already exists in timesheet table
            self.c.execute('''
                SELECT * FROM timesheet WHERE employee_id = ? AND date = ?
            ''', (employee_id, date))

            # Fetch row, if it exists
            existing_entry = self.c.fetchone()  

            # If record already exists then update it
            if existing_entry:
                # Check if entry has changed:
                # Make new entry to compare to the old one
                new_entry = (employee_id, date, starttime,
                             endtime, workhours, breaktime, state)

                # If the data of the new entry are not already in the table, then update them
                if not self.__is_equal(existing_entry, new_entry):

                    self.edit_in_database(
                        employee_id, date, starttime, endtime, breaktime, state)
                    print(f"Record for date {date} updated successfully.")
            
            # If the record does not already exist, then insert it into the table
            else:

                # Insert data into databse
                self.c.execute("INSERT INTO timesheet (employee_id, date, starttime, endtime, workhours, breaktime, state) VALUES (?, ?, ?, ?, ?, ?, ?)",
                               (employee_id, date, starttime, endtime, workhours, breaktime, state))

                # Commit the changes to the database
                self.conn.commit()

        # If data could not be inserted into database, raise error
        except sqlite3.Error as e:
            # Rollback in case something goes wrong
            self.conn.rollback()
            # Raise Error
            raise sqlite3.Error(f"Error inserting into database: {e}")

    # ------------------------------------------------------------------------------

    def __is_equal(self, entry_list_a, entry_list_b):
        """Check if two entry lists for this database are equal."""
        is_equal = False
        if entry_list_a is not None and entry_list_b is not None:
            is_equal = True
            for entry_a, entry_b in zip(entry_list_a, entry_list_b):
                entry_a = self.__unify_entry(entry_a)
                entry_b = self.__unify_entry(entry_b)

                if entry_a is not entry_b and entry_a != entry_b:
                    is_equal = False
        return is_equal

    # ------------------------------------------------------------------------------

    def __unify_entry(self, entry):
        """Unify datetime dates, datetimes and strings to string."""
        if isinstance(entry, datetime.datetime):
            entry = entry.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(entry, datetime.date):
            entry = "{:%Y-%m-%d}".format(entry)
        return entry

    # ------------------------------------------------------------------------------

    # Edit data in the table of the database
    def edit_in_database(self, employee_id, date, starttime, endtime=None, breaktime=None, state='default'):
        # Try to update data in databse
        try:
            # Convert strings to datetime objects if needed
            if isinstance(date, str):
                date = DatetimeFunctions.convert_string_to_date(self, date)
            if isinstance(starttime, str):
                starttime = DatetimeFunctions.convert_string_to_time(
                    self, starttime)
            if isinstance(endtime, str) and endtime:  # only converts if endtime exists
                endtime = DatetimeFunctions.convert_string_to_time(
                    self, endtime)

            # Calculate Workhours if starttime and endtime exists
            if starttime is None or endtime is None:
                workhours = None
            else:
                workhours = DatetimeFunctions.get_time_difference(
                    self, starttime, endtime)

            # Update the timesheet record for the given date
            self.c.execute('''
                UPDATE timesheet
                SET starttime = ?, endtime = ?, workhours = ?, breaktime = ?, state = ?
                WHERE employee_id = ? AND date = ?
            ''',
                           (starttime, endtime, workhours, breaktime, state, employee_id, date))

            # Commit the changes to the database
            self.conn.commit()

        # If data could not be updated, raise error
        except sqlite3.Error as e:
            # Rollback in case something goes wrong
            self.conn.rollback()
            # Raise Error
            raise sqlite3.Error(f"Error updating database: {e}")

    # ------------------------------------------------------------------------------

    # Delete data from database
    def delete_from_database(self, employee_id, date):
        try:
            # Delete a record from the timesheet table where the date matches
            self.c.execute('''
                DELETE FROM timesheet
                WHERE employee_id = ? AND date = ?
            ''', (employee_id, date))

            # Commit the changes to the database
            self.conn.commit()

            # Check if any rows were affected
            if self.c.rowcount == 0:
                if gui_constants.DEBUG:
                    print(f"No records found for date {date} to delete.")
            else:
                print(f"Record for date {date} deleted successfully.")

        # If data could not be deleted
        except sqlite3.Error as e:
            # Rollback in case something goes wrong
            self.conn.rollback()
            # Raise Error
            raise sqlite3.Error(f"Error deleting from database: {e}")

    # ------------------------------------------------------------------------------

    # Disconnect from database
    def disconnect_from_database(self):
        # Close the connection to the database
        self.conn.close()
