# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 10:00:33 2024

This module implements the login screen for the STC time management application.
It presents a simple graphical user interface (GUI) for users to enter their
credentials and log in.

Classes
-------
LoginFrame
    A GUI frame that displays the login interface, allowing users to enter
    their username and password and validating these credentials from a file.

Functions
---------
login()
    Verifies the entered username and password against stored user data.
    Displays success or error messages based on login outcome.

Usage
-----
This module can be run as a standalone script to display the login screen.
When used in the main application, it should be embedded in the parent GUI.

@author: lpasd, Luka
"""

import tkinter as tk
from tkinter import messagebox
import os.path

import gui_constants


class LoginFrame(tk.Frame):
    """
    A frame for user login in the STC time management application.

    This class creates a login form with fields for entering a username
    and password. The credentials are validated against a file containing
    stored user data.

    Attributes
    ----------
    label_title : Label
        A label widget displaying the title of the login form.
    label_username : Label
        A label widget prompting the user to enter their username.
    __entry_username : Entry
        An entry widget for the user to input their username.
    label_password : Label
        A label widget prompting the user to enter their password.
    __entry_password : Entry
        An entry widget for the user to input their password.

    Methods
    -------
    __init__(parent)
        Initializes the login frame with labels,
        input fields, and a login button.

    login()
        Verifies entered credentials and displays a message indicating
        success or failure.
    """

    def __init__(self, parent, main=None):
        """
        Initializes the LoginFrame with a title,
        input fields for username and password,
        and a login button.

        Parameters
        ----------
        parent : widget
            The parent widget in which this frame will be placed.
        """
        super().__init__(master=parent)

        self.main = main
        self.file_path_users = gui_constants.DATA_PATH

        self.label_title = tk.Label(
            self, text="Bitte einloggen", font=("Arial", 14))
        self.label_title.pack(pady=10)

        self.label_username = tk.Label(self, text="Benutzername:")
        self.label_username.pack()
        self.__entry_username = tk.Entry(self)
        self.__entry_username.pack()

        self.label_password = tk.Label(self, text="Passwort:")
        self.label_password.pack()
        self.__entry_password = tk.Entry(self, show="*")
        self.__entry_password.pack()

        button_login = tk.Button(self, text="Login", command=self.login)
        button_login.pack(pady=10)

    def login(self):
        """
        Validates the entered username and password.

        Reads the stored user data from "userdaten.txt" and checks if the
        entered credentials match any stored user. If successful, displays
        a success message. If validation fails, displays an error message.

        Returns
        -------
        None
        """
        username = self.__entry_username.get()
        password = self.__entry_password.get()

        with open(os.path.join(self.file_path_users, "userdata.txt"), "r") as file:
            users = file.readlines()

        for user in users:
            user_data = user.strip().split(",")
            if len(user_data) == 3:
                file_username, file_password, role = user_data
                if username == file_username and password == file_password:

                    messagebox.showinfo("Login Erfolgreich",
                                        f"Login Erfolgreich als {username}")
                    self.main.login(username, role)
                    return
                    messagebox.showerror(
                        "Fehler", "Benutzername oder Passwort ist falsch!")


# Testing Login
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Login Screen")
    root.geometry("300x200")

    login = LoginFrame(root)
    login.pack(expand=True, fill=tk.BOTH)

    root.mainloop()
