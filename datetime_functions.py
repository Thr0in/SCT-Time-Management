# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 15:04:48 2024

@author: jnath
"""
import datetime

# ------------------------------------------------------------------------------


class DatetimeFunctions():

    # ------------------------------------------------------------------------------

    def get_current_date(self):
        """ Function to get current date """

        # Get current datetime (date and time)
        current_datetime = datetime.datetime.now()

        # Extract the date part (YYYY-MM-DD)
        current_date = current_datetime.date()

        # Return date
        return current_date

    # ------------------------------------------------------------------------------

    def get_current_time(self):
        """ Function to get current time """

        # Get current datetime (date and time)
        current_datetime = datetime.datetime.now()

        # Extract the time part (hours:minutes:seconds)
        current_time = current_datetime.time()

        # Return time
        return current_time

    # ------------------------------------------------------------------------------

    def convert_string_to_time(self, time_str):
        """ Converts a string ('HH:MM' format) to datetime """

        # If input is already a datetime.time object, return it directly
        if isinstance(time_str, datetime.time):
            return time_str

        # If input is a string, try to convert it
        if isinstance(time_str, str):
            try:
                # Convert the string to a datetime object and extract the time part
                time = datetime.datetime.strptime(time_str, "%H:%M").time()
                # Return time
                return time
            # Raise Error if could not be converted because it was a diffrent format
            except ValueError:
                raise ValueError("Time string must be in the format 'HH:MM'")

        # Raise an error if the input is neither a string nor a datetime.time object
        raise TypeError("Input must be a string or a datetime.time object.")

    # ------------------------------------------------------------------------------

    def convert_string_to_date(self, date_str):
        """ Converts a string ('YYYY-MM-DD' format) to datetime """

        # If input is already a datetime.date object, return it directly
        if isinstance(date_str, datetime.date):
            return date_str

        # If input is a string, try to convert it
        if isinstance(date_str, str):
            try:
                # Convert the string to a datetime object and extract the date part
                date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
                # Return date
                return date
            # Raise Error if could not be converted because it was a diffrent format
            except ValueError:
                raise ValueError(
                    "Date string must be in the format 'YYYY-MM-DD'")

        # Raise an error if the input is neither a string nor a datetime.date object
        raise TypeError("Input must be a string or a datetime.date object.")

    # ------------------------------------------------------------------------------

    def merge_date_and_time_to_datetime(self, date, time):
        """ Merges a date and time into a single datetime object """

        # Try to convert strings to datetime objects if needed
        if isinstance(time, str):
            try:
                time = self.convert_string_to_time(time)
            except ValueError:
                raise ValueError(
                    "Time is a string and cannot be converted to datetime. \
                        Therefore Date and time cannot be merged to datetime.")

        if isinstance(date, str):
            try:
                date = self.convert_string_to_date(date)
            except ValueError:
                raise ValueError(
                    "Date is a string and cannot be converted to datetime. \
                        Therefore Date and time cannot be merged to datetime.")

        # Ensure both date and time are date/time objects of datetime
        if isinstance(date, datetime.date) and isinstance(time, datetime.time):
            # Combine date and time into a datetime object
            return datetime.datetime.combine(date, time)

        # If both are complete datetime objects (each has a date and a time part):
        elif isinstance(date, datetime.datetime) and isinstance(time, datetime.datetime):
            # If both are datetime objects, combine their parts
            return date.replace(hour=time.hour, minute=time.minute, second=time.second, microsecond=time.microsecond)

        else:
            raise TypeError(
                "Both date and time must be datetime objects or valid date/time strings")

    # ------------------------------------------------------------------------------

    def get_time_difference(self, start_time, end_time):
        """ Calculates time difference between two datetimes in seconds"""

        # Convert strings to datetime objects if needed
        if isinstance(start_time, str):
            start_time = self.convert_string_to_time(start_time)
        if isinstance(end_time, str):
            end_time = self.convert_string_to_time(end_time)

        # Calculate the time difference in seconds
        today = datetime.date.today()
        start_datetime = datetime.datetime.combine(today, start_time)
        end_datetime = datetime.datetime.combine(today, end_time)

        # Ensure end_time is greater than start_time
        if end_datetime < start_datetime:
            raise ValueError("End time must be after start time")

        delta = end_datetime - start_datetime
        return delta.total_seconds()
