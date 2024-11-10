# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 11:45:51 2024

@author: games
"""

import tkinter as tk

class Day_Widget:
    def __init__(self, parent, width_ratio, height_ratio, bg_frame="lightgreen"):
        self.parent = parent
        self.width_ratio = width_ratio
        self.height_ratio = height_ratio

        # Create a Frame for the composite widget
        self.frame = tk.Frame(parent, bg=bg_frame)
        self.frame.grid_propagate(False)

        # Create and place labels and entries
        self.label_day = tk.Label(self.frame, text="00", anchor="center")
        self.entry_start = tk.Entry(self.frame, justify="center")
        self.entry_end = tk.Entry(self.frame, justify="center")
        self.entry_break = tk.Entry(self.frame, justify="center")
        self.label_total = tk.Label(self.frame, text="total", anchor="center")

        self.entry_start.insert(0, "start")
        self.entry_end.insert(0, "end")
        self.entry_break.insert(0, "break")

        # Place labels using relative positioning
        self.label_day.place(relwidth=0.2, relheight=0.2, anchor="nw")
        self.entry_start.place(relx=0.05, rely=0.25, relwidth=0.425, relheight=0.2)
        self.entry_end.place(relx=0.05, rely=0.5, relwidth=0.425, relheight=0.2)
        self.entry_break.place(relx=0.525, rely=0.4, relwidth=0.425, relheight=0.2)
        self.label_total.place(relx=0.05, rely=0.75, relwidth=0.9, relheight=0.2)

    def update_size(self, width, height):
        composite_width = int(width * self.width_ratio)
        composite_height = int(height * self.height_ratio)
        self.frame.config(width=composite_width, height=composite_height)
        
        # Calculate font size based on composite height
        font_size = max(8, int(composite_height * 0.1))
        font = ("Arial", font_size)

        # Update font for each label and entry
        self.label_day.config(font=font)
        self.entry_start.config(font=font)
        self.entry_end.config(font=font)
        self.entry_break.config(font=font)
        self.label_total.config(font=font)

class Info_Panel:
    def __init__(self, parent):
        """Composite widget containing six labels for displaying information."""
        self.frame = tk.Frame(parent, bg="lightgray")
        
        # Original labels
        self.label_flex_time = tk.Label(self.frame, text="Flex-Time", font=("Arial", 12, "underline"), bg="lightgray")
        self.label_vacation_days = tk.Label(self.frame, text="Vacation Days", font=("Arial", 12, "underline"), bg="lightgray")
        self.label_vacation_days_previous = tk.Label(self.frame, text="From Previous Year", font=("Arial", 12, "underline"), bg="lightgray")
        
        # New labels displaying "--"
        self.label_flex_time_text = tk.Label(self.frame, text="--", font=("Arial", 12), bg="lightgray")
        self.label_vacation_days_text = tk.Label(self.frame, text="--", font=("Arial", 12), bg="lightgray")
        self.label_vacation_days_previous_text = tk.Label(self.frame, text="--", font=("Arial", 12), bg="lightgray")
        
        # Arrange labels in the Info_Panel
        self.label_flex_time.pack(padx=5, pady=(2, 0), anchor="w")
        self.label_flex_time_text.pack(padx=10, pady=(0, 5), anchor="w")
        
        self.label_vacation_days.pack(padx=5, pady=(2, 0), anchor="w")
        self.label_vacation_days_text.pack(padx=10, pady=(0, 5), anchor="w")
        
        self.label_vacation_days_previous.pack(padx=5, pady=(2, 0), anchor="w")
        self.label_vacation_days_previous_text.pack(padx=10, pady=(0, 5), anchor="w")

class Sidebar:
    def __init__(self, parent, width):
        """A composite sidebar widget with an Info_Panel and buttons."""
        self.frame = tk.Frame(parent, width=width, bg="gray")
        self.frame.grid_propagate(False)  # Prevents resizing

        # Create the Info_Panel at the top of the sidebar
        self.info_panel = Info_Panel(self.frame)
        self.info_panel.frame.pack(padx=10, pady=10, fill="x")

        # Add button directly below the Info_Panel
        self.button_request_vacation = tk.Button(self.frame, text="Request Vacation", font=("Arial", 12))
        self.button_request_vacation.pack(padx=10, fill="x")

        # Create two buttons at the bottom, stacked on top of each other
        self.button_start_break = tk.Button(self.frame, text="Start Break", font=("Arial", 12))
        self.button_start_work = tk.Button(self.frame, text="Start Workday", font=("Arial", 12))
        
        # Place these buttons at the bottom
        self.button_start_break.pack(side="bottom", padx=10, pady=10, fill="x")
        self.button_start_work.pack(side="bottom", padx=10, fill="x")

class TopBar:
    def __init__(self, parent, height):
        """A composite top bar widget that expands to fit the width of the window."""
        self.frame = tk.Frame(parent, bg="darkblue", height=height)
        self.frame.grid_propagate(False)
        
        # Logout button on the right side of the top bar
        self.logout_button = tk.Button(self.frame, text="Logout", font=("Arial", 12), bg="white")
        self.logout_button.pack(padx=10, pady=10, side="right")  # Align the button to the right side of the bar

def update_dimensions():
    # Update width and height of Calendar_Frame for resizing Day_Widget instances
    width = Calendar_Frame.winfo_width()
    height = Calendar_Frame.winfo_height()

    # Update all Day_Widget sizes
    for widget in composite_widgets:
        widget.update_size(width, height)

def on_resize(event):
    global resize_id
    if resize_id is not None:
        root.after_cancel(resize_id)
    resize_id = root.after(100, update_dimensions)

# Set up the main window
root = tk.Tk()
root.title("SCT GUI")
root.geometry("1280x720")
root.minsize(1280, 720)

# Configure root layout: sidebar in leftmost column, top bar at top
root.columnconfigure(0, minsize=200)  # Fixed width for sidebar
root.columnconfigure(1, weight=1)     # Expandable Calendar_Frame
root.rowconfigure(0, minsize=70)      # Fixed height for top bar
root.rowconfigure(1, weight=1)        # Expandable Calendar_Frame area

# Initialize and place sidebar in the leftmost column
sidebar = Sidebar(root, width=200)
sidebar.frame.grid(row=0, column=0, rowspan=2, sticky="nesw")

# Initialize and place top bar in the top row
top_bar = TopBar(root, height=70)
top_bar.frame.grid(row=0, column=1, sticky="nesw")

# Create and configure Calendar_Frame for the main Day_Widget grid area
Calendar_Frame = tk.Frame(root, bg="lightblue")
Calendar_Frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

# Configure Calendar_Frame with 7 columns and 8 rows (1 row for the main label, 1 for days of the week)
for i in range(7):
    Calendar_Frame.columnconfigure(i, weight=1, uniform="column")
for j in range(2, 8):  # Rows 2 to 7 will contain the Day_Widget grid
    Calendar_Frame.rowconfigure(j, weight=1, uniform="row")

# Create the current month header with navigation buttons
button_previous_month = tk.Button(Calendar_Frame, font=("Arial",  10), text="Previous Month")
button_previous_month.grid(row=0, column=0, sticky="new", padx=5, pady=5)

label_current_month = tk.Label(Calendar_Frame, font=("Arial", 18, "bold"), bg="lightblue", text="Current Month")
label_current_month.grid(row=0, column=1, columnspan=5, sticky="nsew")

button_next_month = tk.Button(Calendar_Frame, font=("Arial",  10), text="Next Month")
button_next_month.grid(row=0, column=6, sticky="new", padx=5, pady=5)

# Create a row of labels for each day of the week
days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
for i, day in enumerate(days_of_week):
    day_label = tk.Label(Calendar_Frame, text=day, font=("Arial", 14), bg="lightblue")
    day_label.grid(row=1, column=i, sticky="nsew")

# Create and place Day_Widget instances starting from row 2 onward
composite_widgets = []
for row in range(2, 8):
    for col in range(7):
        widget = Day_Widget(Calendar_Frame, width_ratio=1/7, height_ratio=1/6)
        widget.frame.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)
        composite_widgets.append(widget)

# Variable to store the resize timer ID
resize_id = None

# Bind the resize function to window resize events
root.bind("<Configure>", on_resize)

# Run the Tkinter event loop
root.mainloop()
