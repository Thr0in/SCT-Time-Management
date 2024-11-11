# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 18:46:08 2024

@author: Luka
"""

from gui_logic import Timesheet
import gui_constants


# Start STC time management program
if __name__ == "__main__":
    # gui_constants.DEBUG = True
    # gui_constants.AUTO_LOGIN = True
    gui_constants.USE_TEXT_HINTS = False
    gui_constants.SHOW_ONLY_MINIMUM_DAYS = True
    app = Timesheet()
