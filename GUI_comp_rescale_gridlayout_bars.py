# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 11:45:51 2024

@author: games
"""

import tkinter as tk

class Day_Widget:
    def __init__(self, parent, bg_frame="lightgreen"):
        self.parent = parent
        self.font_scale_factor = 0.1

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

        # Bind resize event to adjust font size
        self.frame.bind("<Configure>", self.adjust_font_size)

    def adjust_font_size(self, event):
        # Calculate font size based on the height of the Day_Widget frame
        font_size = int(event.height * self.font_scale_factor)

        # Apply calculated font size to each label and entry widget
        self.label_day.config(font=("Arial", font_size))
        self.entry_start.config(font=("Arial", font_size))
        self.entry_end.config(font=("Arial", font_size))
        self.entry_break.config(font=("Arial", font_size))
        self.label_total.config(font=("Arial", font_size))

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
    
class MainApp:
    def __init__(self):
        # Initialize the root window
        self.root = tk.Tk()
        self.root.title("SCT GUI")
        self.root.geometry("1280x720")
        self.root.minsize(1280, 720)

        # Configure root layout
        self.root.columnconfigure(0, minsize=200)  # Sidebar column
        self.root.columnconfigure(1, weight=1)     # Expandable Calendar_Frame
        self.root.rowconfigure(0, minsize=70)      # Top bar row
        self.root.rowconfigure(1, weight=1)        # Expandable Calendar_Frame area

        # Initialize components
        self.create_sidebar()
        self.create_top_bar()
        self.create_calendar_frame()

    def create_sidebar(self):
        # Sidebar in the leftmost column
        self.sidebar = Sidebar(self.root, width=200)
        self.sidebar.frame.grid(row=0, column=0, rowspan=2, sticky="nesw")

    def create_top_bar(self):
        # Top bar in the top row
        self.top_bar = TopBar(self.root, height=70)
        self.top_bar.frame.grid(row=0, column=1, sticky="nesw")

    def create_calendar_frame(self):
        # Calendar frame for Day_Widget grid area
        self.calendar_frame = tk.Frame(self.root, bg="lightblue")
        self.calendar_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        # Configure columns and rows
        for i in range(7):
            self.calendar_frame.columnconfigure(i, weight=1, uniform="column")
        for j in range(2, 8):
            self.calendar_frame.rowconfigure(j, weight=1, uniform="row")

        # Create current month header with navigation buttons
        self.button_previous_month = tk.Button(self.calendar_frame, font=("Arial", 10), text="Previous Month")
        self.button_previous_month.grid(row=0, column=0, sticky="new", padx=5, pady=5)

        self.label_current_month = tk.Label(self.calendar_frame, font=("Arial", 18, "bold"), bg="lightblue", text="Current Month")
        self.label_current_month.grid(row=0, column=1, columnspan=5, sticky="nsew")

        self.button_next_month = tk.Button(self.calendar_frame, font=("Arial", 10), text="Next Month")
        self.button_next_month.grid(row=0, column=6, sticky="new", padx=5, pady=5)

        # Row of labels for each day of the week
        days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        for i, day in enumerate(days_of_week):
            day_label = tk.Label(self.calendar_frame, text=day, font=("Arial", 14), bg="lightblue")
            day_label.grid(row=1, column=i, sticky="nsew")

        # Create and place Day_Widget instances
        self.composite_widgets = []
        for row in range(2, 8):
            for col in range(7):
                widget = Day_Widget(self.calendar_frame)
                widget.frame.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)
                self.composite_widgets.append(widget)

    def run(self):
        # Run the Tkinter event loop
        self.root.mainloop()

app = MainApp()
app.run()