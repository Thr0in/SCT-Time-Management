# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 15:04:48 2024

@author: jnath
"""
# Datetime Function Module

import datetime
import numpy as np

import gui_constants

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
        """ Converts a string ('HH:MM' or 'HH:MM:SS' format) to datetime.time object """

        # If the string is empty or None
        if not time_str:
            return None

        # If input is already a datetime.time object, return it directly
        if isinstance(time_str, datetime.time):
            return time_str

        # If input is a datetime.datetime object, convert to datetime.time
        if isinstance(time_str, datetime.datetime):
            return time_str.time()

        # If input is a string, try to convert it
        if isinstance(time_str, str):
            try:

                # If there are seconds, but we only need hours and minutes (Format 'HH:MM:SS')
                if len(time_str.split(':')) == 3:
                    # Strip off the seconds part by splitting the string and keeping only 'HH:MM'
                    time_str = ':'.join(time_str.split(':')[:2])

                # Convert the string (Format 'HH:MM') to a datetime object and extract the time part
                time = datetime.datetime.strptime(time_str, "%H:%M").time()

                # Return time
                return time

            # Raise Error if could not be converted because it was a diffrent format
            except ValueError:
                raise ValueError(
                    "Time string must be in the format 'HH:MM', instead it is ", time_str)

        # Raise an error if the input is neither a string nor a datetime.time object
        raise TypeError("Input must be a string or a datetime.time object.")

    # ------------------------------------------------------------------------------

    def convert_string_to_date(self, date_str='2000-01-01'):
        """ Converts a string ('YYYY-MM-DD' format) to datetime """
        # Default Parameter for date_str implemented,
        # as error kept occuring during typing in the time
        # that claimed no date_str was passed

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

    def convert_string_to_time_from_datetime(self, datetime_str):
        """Converts a full datetime string ('YYYY-MM-DD HH:MM:SS') to a datetime.time object."""
        # If string exists
        if datetime_str:
            # Extract the time part from the datetime string and convert it
            try:
                # Split at the space to get "HH:MM:SS"
                time_part = datetime_str.split(' ')[1]
                # Use original convert_string_to_time function
                time = DatetimeFunctions().convert_string_to_time(time_part)
                return time
            # Raise Error if could not be converted because it was a diffrent format
            except Exception as e:
                raise ValueError(
                    f"Invalid datetime format: {datetime_str}, Error: {str(e)}")
        return None

     # ------------------------------------------------------------------------------

    def merge_date_and_time_to_datetime(self, date, time):
        """ Merges a date and time into a single datetime object """

        # If time is a string, try to convert it to a datetime.time object
        if isinstance(time, str):
            try:
                # Try to convert stringt to datetime.time object
                time = self.convert_string_to_time(time)
            # Raise Error if time could not be converted because it was a diffrent format
            except ValueError:
                raise ValueError(
                    "Time is a string and cannot be converted to datetime. Therefore Date and time cannot be merged to datetime.")

        # If time is already a datetime.date object, raise an error (since you can't merge a date with another date)
        elif isinstance(time, datetime.date) and not isinstance(time, datetime.time):
            raise TypeError(
                "Time must be a datetime.time object or a string representing a time, not a date.")

        # If date is a string, convert it to a datetime.date object
        if isinstance(date, str):
            try:
                # Try to convert it to a datetime.date object
                date = self.convert_string_to_date(date)
             # Raise Error if date could not be converted because it was a diffrent format
            except ValueError:
                raise ValueError(
                    "Date is a string and cannot be converted to datetime. Therefore Date and time cannot be merged to datetime.")

        # Ensure both date and time are the correct types before merging
        if isinstance(date, datetime.date) and isinstance(time, datetime.time):
            # Combine date and time into a datetime object
            return datetime.datetime.combine(date, time)

        # If both are complete datetime objects (each has a date and a time part):
        elif isinstance(date, datetime.datetime) and isinstance(time, datetime.datetime):
            # If both are datetime objects, combine their parts
            return date.replace(hour=time.hour, minute=time.minute, second=time.second, microsecond=time.microsecond)

        # Raise an error if the input is neither a string nor a datetime.date or datetime.time object
        else:
            raise TypeError(
                "Both date and time must be datetime objects or valid date/time strings.")

    # ------------------------------------------------------------------------------

    def get_time_difference(self, start_time, end_time):
        """ Calculates time difference between two datetimes in seconds"""

        # Convert strings to datetime objects if needed
        if isinstance(start_time, str):
            start_time = self.convert_string_to_time(start_time)
        if isinstance(end_time, str):
            end_time = self.convert_string_to_time(end_time)

        # Convert datetime objects to datetime.time objects if needed
        if isinstance(start_time, datetime.datetime):
            start_time = start_time.time()
        if isinstance(end_time, datetime.datetime):
            end_time = end_time.time()

        # Calculate the time difference in seconds
        today = datetime.date.today()
        start_datetime = datetime.datetime.combine(today, start_time)
        end_datetime = datetime.datetime.combine(today, end_time)

        # Ensure end_time is greater than start_time
        if end_datetime < start_datetime:
            raise ValueError("End time must be after start time")

        # Calculate time difference
        delta = end_datetime - start_datetime

        # Return time difference
        return delta.total_seconds()

    # ------------------------------------------------------------------------------

    def time_to_string(self, time=None, unsigned=True):
        """
        Convert time in seconds to a string formatted as "HH:MM".

        Parameters
        ----------
        time : int, optional
            The time in seconds to convert. Default is None, which
            returns "--:--".
        unsigned : bool
            Wether the returned string shall contain the sign of the time.

        Returns
        -------
        str
            The formatted time string.
        """
        time_string = gui_constants.NO_TIME_DATA

        if time is not None:
            sign = np.sign(time)
            time = np.abs(time)

            time = time // 60
            minutes = time % 60
            hours = time // 60

            time_string = ''
            if not unsigned:
                if sign < 0:
                    time_string = '- '
                else:
                    time_string = '+ '
            time_string += '{h:02.0f}:{m:02.0f}'.format(h=hours, m=minutes)
        return time_string

    # ------------------------------------------------------------------------------

    def time_object_to_string(self, time_object=None):
        """
        Convert a datetime.time object to a string with the format 'hh:mm'.

        Parameters
        ----------
        time_object : datetime.time, optional
            Datetime.time object. The default is None.

        Returns
        -------
        time_object : str or None
            Time as formatted string. Is None if input is None.

        """
        if time_object is not None:
            time_object = time_object.strftime("%H:%M")
        return time_object

    # ------------------------------------------------------------------------------

    def time_in_seconds(self, time_object):
        """
        Return the provided time objects time as a value in seconds.

        Parameters
        ----------
        time_object : datetime.time
            The given datetime.time object.

        Returns
        -------
        int
            Time in seconds.

        """
        return (time_object.hour * 60 + time_object.minute) * 60 + time_object.second
