# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 18:46:08 2024

@author: Luka
"""
import tkinter as tk

from calendar_widget import CalendarWidget
from side_bar import SideBar


"""

Deprecated! Don't use!


root = tk.Tk()
root.geometry('1100x620')


calendar = CalendarWidget(root)
side_bar = SideBar(root)
side_bar.pack(side="left", expand=True, fill=tk.BOTH)
calendar.pack(side="left")

calendar.content.days[0].set_start_time(30600)
calendar.content.days[0].set_end_time(60600)
calendar.content.days[0].set_break_time(2700)
calendar.content.days[0].set_total_time(60600-30600-2700)

root.mainloop()


"""
