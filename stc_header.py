# -*- coding: utf-8 -*-
"""
Created on Sat Nov  9 03:30:18 2024

@author: Luka
"""

import tkinter as tk

import gui_constants


class STCHeader(tk.Frame):
    def __init__(self, parent, main=None):
        super().__init__(master=parent, borderwidth=1)
        self.main = main
        self.employee_name = tk.StringVar(value='default')
        self.role = tk.StringVar(value='(Employee)')

        self.logo = tk.Frame(self, relief="solid", padx=28)
        self.logo.pack(side='left', fill=tk.X)

        tk.Label(self.logo, text='STC',
                 font=gui_constants.EXTRA_LARGE).pack(side='top')
        tk.Label(self.logo, text='Time Management System',
                 font=gui_constants.BOLD).pack(side='top')

        self.menu = tk.Frame(self, relief="solid", padx=20)
        self.menu.pack(side='right', expand=True, fill=tk.BOTH)

        self.logout = tk.Button(
            self.menu, text="Logout", command=lambda: self.logout(),
            font=gui_constants.BOLD)
        self.logout.pack(side='right')

        employee = tk.Frame(self.menu)
        employee.pack(side='right')

        tk.Label(employee, textvariable=self.employee_name,
                 font=gui_constants.LARGE).pack(side='top')
        tk.Label(employee, textvariable=self.role).pack(side='top', padx=20)

    def logout(self):
        self.main.logout()


# Testing Login
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Login Screen")
    root.geometry("300x200")

    login = STCHeader(root)
    login.pack(expand=True, fill=tk.BOTH)

    root.mainloop()
