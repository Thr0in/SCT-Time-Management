# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 08:34:07 2024

@author: jnath
"""
import sqlite3

# Step 1: Create or connect to a SQLite database (the database file will be created if it doesn't exist)
conn = sqlite3.connect('timesheet.db')  # 'timesheet.db' is the file name
c = conn.cursor()  # Create a cursor object to interact with the database

# Step 2: Create a table (if it doesn't already exist)
c.execute('''
    CREATE TABLE IF NOT EXISTS timesheet (
        date DATE,
        starttime DATETIME,
        endtime DATETIME,
        workhours,
        breaktime,        
    )
''')

# SQL Syntax for creating a TABLE
# CREATE TABLE table_name (
#     column1_name column1_data_type [constraints],
#     column2_name column2_data_type [constraints],
#     ...
# );

# get current date with:
#     current_date = datetime.date.today()  # Get today's date (e.g., 2024-11-07)
# get current time with:
#     current_date = datetime.date.time()  # Get today's date (e.g., 2024-11-07)

        

# Step 3: Insert some data into the table
#c.execute("INSERT INTO users (name, age) VALUES ('Alice', 30)")
#c.execute("INSERT INTO users (name, age) VALUES ('Bob', 25)")
#c.execute("INSERT INTO users (name, age) VALUES ('Bob2', 25)")
c.execute("UPDATE users (name, age) VALUES ('Bob2', 25)")

# Commit the changes to the database
conn.commit()

# Step 4: Query the database to retrieve data
c.execute('SELECT * FROM users')
rows = c.fetchall()  # Fetch all the results

for row in rows:
    print(row)  # Print each row from the database

# Step 5: Close the connection to the database
conn.close()

