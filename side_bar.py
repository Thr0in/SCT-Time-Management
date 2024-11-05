# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 15:53:40 2024

@author: Luka

A time management application using the Tkinter library.
The main components of this GUI include a sidebar for managing flex time
and vacation requests, and information panels to display the user's
current work status.
"""
import tkinter as tk


class SideBar(tk.Frame):
    """
    A sidebar component containing action buttons and an information panel.

    Methods
    -------
    __init__(parent)
        Initializes the sidebar with buttons and an information panel.
    """

    def __init__(self, parent):
        """
        Constructs the SideBar with vacation and time logging buttons.

        Parameters
        ----------
        parent : widget
            The parent widget in which this sidebar will be placed.
        """

        super().__init__(master=parent, bg="azure3", padx=20, pady=20)

        self.info_panel = InfoPanel(self)

        button_request_vacation = tk.Button(self, text="Request Vacation")
        button_log_working_time = tk.Button(self, text="Start Workday")
        button_log_break_time = tk.Button(self, text="Start BreaK")

        self.info_panel.pack(fill=tk.X, pady=5)
        button_request_vacation.pack(side="top", fill=tk.X, pady=5)
        button_log_break_time.pack(side="bottom", fill=tk.X, pady=5)
        button_log_working_time.pack(side="bottom", fill=tk.X, pady=5)


class InfoPanel(tk.Frame):
    """
    A panel for displaying user information such as
    flex time and vacation days.

    Methods
    -------
    __init__(parent)
        Initializes the information panel with labels for user status.
    """

    def __init__(self, parent):
        """
        Constructs the InfoPanel to display flex time and vacation details.

        Parameters
        ----------
        parent : widget
            The parent widget in which this information panel will be placed.
        """

        super().__init__(master=parent, padx=10, pady=10,
                         borderwidth=1, relief="solid")

        self.var_flex_time = tk.StringVar(value="+ 27:13")
        self.var_vacation_days = tk.StringVar(value=17)
        self.var_old_vacation_days = tk.StringVar(value=0)

        tk.Label(self, text="Flex-Time:").pack(anchor="nw")
        tk.Label(self, textvariable=self.var_flex_time).pack(anchor="nw")

        tk.Label(self, text="Remaining vacation days:").pack(anchor="nw")
        tk.Label(self, textvariable=self.var_vacation_days).pack(anchor="nw")

        tk.Label(self, text="Vacation from last year:").pack(anchor="nw")
        tk.Label(
            self, textvariable=self.var_old_vacation_days).pack(anchor="nw")
