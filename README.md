
# STC Time Management Application

This is a time management and tracking application for employees, built using Python and Tkinter. It allows employees to log their work hours, manage break times, and track their vacation days. The application provides a graphical calendar view for easy navigation and interaction.

## Table of Contents

- [Features](#features)
- [Modules](#modules)
  - [main.py](#1-mainpy)
  - [login.py](#2-loginpy)
  - [data_model.py](#3-data_modelpy)
  - [database_functions.py](#4-database_functionspy)
  - [datetime_functions.py](#5-datetime_functionspy)
  - [gui_constants.py](#6-gui_constantspy)
  - [gui.py](#7-guipy)
  - [gui_logic.py](#8-gui_logicpy)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Authors](#authors)

## Features

- **Employee Login**: Users log in with their credentials, which are validated against stored data.
- **Calendar View**: A 6x7 grid calendar displays each day of the month, with entries for work start time, end time, and break time.
- **Flexible Data Tracking**: Users can log start and end of work, breaks, and view accumulated flex time and vacation days.
- **Database Integration**: Supports saving and loading workday data to a SQLite database or CSV files.
- **Customizable Interface**: GUI elements and theme colors can be modified using configuration constants.

## Modules

### 1. `main.py`
This script launches the STC Time Management Application, initializing the main GUI and setting program options (e.g., enabling debug mode).

### 2. `login.py`
Defines the login screen interface:
- **LoginFrame**: Presents the login GUI, allowing users to enter and validate their credentials.
- **login()**: Validates username and password against stored data.

### 3. `data_model.py`
Handles employee workday data:
- **WorkingDay**: Represents a workday with attributes such as start time, end time, break time, and state (e.g., “vacation”).
- **WorkTimeEmployee**: Manages an employee’s workdays, calculates flex time, and tracks vacation days. Includes methods for loading, saving, and retrieving workday data.

### 4. `database_functions.py`
Provides SQLite database functions:
- **connect_to_database()**: Establishes a connection to the SQLite database and creates tables if needed.
- **insert_into_database()** and **edit_in_database()**: Insert and update timesheet records.
- **delete_from_database()**: Deletes records based on date.
- **disconnect_from_database()**: Closes the database connection.

### 5. `datetime_functions.py`
Contains utility functions for date and time manipulation:
- **get_current_date()** and **get_current_time()**: Retrieve the current date and time.
- **convert_string_to_time()** and **convert_string_to_date()**: Convert strings to date/time objects.
- **get_time_difference()**: Calculates time difference in seconds.
- **time_to_string()**: Formats time values as strings.

### 6. `gui_constants.py`
Defines constants for the application, including:
- GUI color themes, font settings, and data paths.
- Feature toggles such as **DEBUG** mode and **AUTO_LOGIN**.

### 7. `gui.py`
Constructs the GUI components:
- **Day_Widget**: A widget representing a single day, allowing entry of work start, end, break, and total times.
- **Info_Panel**: Displays flex time and vacation days.
- **Sidebar** and **TopBar**: Provide additional controls and display user information.
- **MainApp**: The main application container, organizing the layout of the calendar, sidebar, and top bar.

### 8. `gui_logic.py`
Implements the main logic for the STC application:
- **Timesheet**: Manages the login, calendar, and data handling. Provides functions for logging workday start/end, tracking breaks, loading and saving data, and navigating the calendar.

## Installation

1. Clone or download the repository.
2. Run the application:
   ```bash
   python main.py
   ```

## Usage

1. **Login**: Enter credentials on the login screen.
2. **Log Work Time**: Use the calendar interface to log work start/end times and breaks.
3. **View Data**: Track accumulated flex time and vacation days in the sidebar.
4. **Save Data**: Data is saved automatically when you log out or exit the application.

## Configuration

Settings in `gui_constants.py` allow customization:
- **DEBUG**: Enables debug output for troubleshooting.
- **AUTO_LOGIN**: Allows skipping the login screen.
- **USE_DATABASE**: Switch between using SQLite or CSV files for data storage.

## Authors

Developed by Luka, Jnath, Lpasd, Tim, and Danny.
