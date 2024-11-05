# Time Management Application

This is a Tkinter-based time management application designed to help users manage workdays, track flex time, request vacation days, and log working hours. The main components of the application include a calendar for tracking working hours, a sidebar for managing flex time and vacation requests, and an information panel displaying current work status.

## Table of Contents

- [Features](#features)
- [Modules](#modules)
  - [calendar_widget.py](#calendar_widgetpy)
  - [day_widget.py](#day_widgetpy)
  - [data_model.py](#data_modelpy)
  - [side_bar.py](#side_barpy)
  - [test_main.py](#test_mainpy)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Requirements](#requirements)

## Features

- **Calendar View**: Displays a grid of day widgets for viewing workdays.
- **Workday Logging**: Allows users to log start, end, and break times for each day.
- **Flex Time Tracking**: Calculates accumulated flex time based on work hours.
- **Vacation Management**: Provides options for managing vacation days.
- **Persistent Data Storage**: Saves and loads workday data from a CSV file.

## Modules

### calendar_widget.py

The `calendar_widget.py` module creates the main calendar interface, including:
- `CalendarHeader`: Contains navigation buttons and displays the selected month.
- `CalendarContent`: Holds the grid of day widgets (`DayWidget` instances).
- `CalendarWidget`: The main calendar frame that combines the header and content sections.


### day_widget.py

The `day_widget.py` module defines the `DayWidget` class, which represents individual days in the calendar. Each `DayWidget` allows users to view and edit:
- **Day Number**: The specific day within a month.
- **Start Time**: Time the workday started.
- **End Time**: Time the workday ended.
- **Break Time**: Total break time taken during the day.
- **Total Time**: Total time worked for the day, minus breaks.


### data_model.py

The `data_model.py` module includes the data handling and logic classes:
- `WorkingDay`: Represents a single working day, with attributes for start time, end time, break time, and state (e.g., default, sick, vacation).
- `WorkTimeEmployee`: Manages the data for an employee, including vacation days and working day records. Provides methods for loading and saving workday data to CSV, and calculates flex time based on working hours.


### side_bar.py

The `side_bar.py` module provides the sidebar interface, which includes:
- `SideBar`: Contains buttons for requesting vacation and logging work/break times.
- `InfoPanel`: Displays information such as remaining flex time, vacation days, and carryover vacation days from previous years.


### test_main.py

The `test_main.py` script is the main entry point for running the application. It initializes the Tkinter root window, creates instances of `CalendarWidget` and `SideBar`, and adds test data to display sample work hours for the first day.


## Getting Started

1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/Thr0in/SCT-Time-Management.git
2. Navigate to the project directory:
   ```bash
   cd SCT-Time-Management
3. Run the application:
   ```bash
   python test_main.py

## Usage

- **Calendar**: Navigate through months using the < and > buttons in the calendar header. Click on any day to log working hours.
- **Sidebar**: Use the "Request Vacation" and "Start Workday/Break" buttons to log activities.
- **Information Panel**: View your flex time and remaining vacation days.
- **Data Persistence**: Working days are saved in a CSV file (<employee_id>.csv) for persistence.

## Requirements

- Python 3.x
- Tkinter (usually included with Python)
