# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 18:46:08 2024

@author: Luka
"""

import argparse
from gui_logic import Timesheet
import gui_constants


# Start STC time management program
if __name__ == "__main__":
    # =========================================================================
    #     parser = argparse.ArgumentParser()
    #     parser.add_argument("-D", "--debug", type=bool)
    #     parser.add_argument("-a", "--auto-login", type=bool)
    #     parser.add_argument("-m", "--minimum-calendar", type=bool)
    #     parser.add_argument("-t", "--text-hints", type=bool)
    #     parser.add_argument("-d", "--use-database", type=bool)
    #     parser.add_argument("-l", "--less-traffic", type=bool)
    #     parser.add_argument("-i", "--import-csv", type=bool)
    #     parser.add_argument("-e", "--export-csv", type=bool)
    #
    #     args = parser.parse_args()
    #
    #     gui_constants.DEBUG = args.debug
    #     gui_constants.AUTO_LOGIN = args.auto_login
    #     gui_constants.SHOW_ONLY_MINIMUM_DAYS = args.minimum_calendar
    #     gui_constants.USE_TEXT_HINTS = args.text_hints
    #     gui_constants.USE_DATABASE = args.use_database
    #     gui_constants.REDUCED_DATABASE_TRAFFIC = args.less_traffic
    #     gui_constants.IMPORT_FROM_CSV = args.import_csv
    #     gui_constants.WRITE_TO_CSVS = args.export_csv
    # =========================================================================

    # gui_constants.DEBUG = False
    # gui_constants.AUTO_LOGIN = False
    # gui_constants.SHOW_ONLY_MINIMUM_DAYS = False
    # gui_constants.USE_TEXT_HINTS = False
    # gui_constants.USE_DATABASE = True
    # gui_constants.REDUCED_DATABASE_TRAFFIC = True
    # gui_constants.IMPORT_FROM_CSV = False
    # gui_constants.WRITE_TO_CSVS = False

    app = Timesheet()
