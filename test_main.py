# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 18:46:08 2024

@author: Luka
"""

from sct_gui import DayWidget, CalendarWidget, SideBar
import tkinter as tk

root = tk.Tk()
root.geometry('1100x620')

# label = Label(root, text="Test", font=("Helvetica", 18), fg="white", bg="green", borderwidth=2, relief="solid", padx=5,pady=5)
# label.grid(column=0, row=0)





calendar = CalendarWidget(root)
side_bar = SideBar(root)
side_bar.pack(side="left", expand=True, fill=tk.BOTH)
calendar.pack(side="left")

calendar.content.days[0].set_start_time(30600)
calendar.content.days[0].set_end_time(60600)
calendar.content.days[0].set_break_time(2700)
calendar.content.days[0].set_total_time(60600-30600-2700)

root.mainloop()
