# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 16:17:50 2024
test
@author: Luka
"""

from datetime import date, datetime
import os.path
import csv

DATABASE = False


class WorkingDay():
    def __init__(self, date_object):
        self.start_time = -1
        self.end_time = -1
        self.break_time = -1

        self.state = "default"

        self.date = date_object


class WorkTimeEmployee():
    def __init__(self, employee_id="default"):
        self.employee_id = employee_id
        self.file_path = self.employee_id + ".csv"

        self.working_days = {}

        if os.path.isfile(self.file_path):
            self.load_working_days()

    def create_day(self, date_object=date.today()):
        day = WorkingDay(date_object)
        self.working_days["{:%Y%m%d}".format(date_object)] = day
        return day

    def load_working_days(self):
        if DATABASE:
            print("Accessing database...")
        else:
            try:
                with open(self.file_path, 'r') as csvfile:
                    reader = csv.DictReader(csvfile)

                    for row in reader:
                        date_object = datetime.strptime(row['Date'], '%Y%m%d')
                        start_time = row['Start Time']
                        end_time = row['End Time']
                        break_time = row['Break Time']
                        state = row['State']

                        day = self.create_day(date_object)

                        day.start_time = start_time
                        day.end_time = end_time
                        day.break_time = break_time
                        day.state = state

            except Exception as e:
                print("Error", f"Failed to load timesheet: {e}")

    def save_working_days(self):
        if DATABASE:
            print("Accessing database...")
        else:
            with open(self.file_path, 'w', newline='') as csvfile:

                fieldnames = ['Date', 'Start Time',
                              'End Time', 'Break Time', 'State']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()
                for date_string, day in self.working_days.items():
                    writer.writerow(
                        {'Date': date_string,
                         'Start Time': day.start_time,
                         'End Time': day.end_time,
                         'Break Time': day.break_time,
                         'State': day.state})


# Testing of data model
# =============================================================================
# test = WorkTimeEmployee()
# test.create_day()
#
# test.save_working_days()
# print(test.working_days.items())
#
# =============================================================================
