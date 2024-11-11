# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 18:46:08 2024

@author: Luka
"""

from gui_logic import Timesheet
import gui_constants


# Start STC time management program
if __name__ == "__main__":
    #gui_constants.AUTO_LOGIN = True
    gui_constants.USE_DATABASE = True
    app = Timesheet()
