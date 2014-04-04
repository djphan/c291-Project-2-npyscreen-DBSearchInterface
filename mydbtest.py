#!/usr/bin/python3

import sys
import bsddb3 as bsddb
import random
import os
import npyscreen
import gui
from functions import *
from datasearch import DataRetrieve
from keysearch import KeyRetrieve
from range_search import RangeRetrieve

# Note: Program crashes when you try and execute a search when you don't have a database.
# Try/except catch needed to fix this.

class MyApplication(npyscreen.NPSAppManaged):
    """
    An NPS Managed Application. This class holds all the forms, manages their
    status, switches between them and displays them.
    
    To launch the application, an instance of MyApplication is created, and
    MyApplication.run is called.

    This happens automatically when this module is run as a script.
    """

    def onStart(self):
        self.addFormClass('MAIN', gui.MainMenu, name="MAIN MENU")
        self.addFormClass('KEYRETRIEVE', KeyRetrieve, name="KEY RETRIEVE")
        self.addFormClass('DATARETRIEVE', DataRetrieve, name="DATA RETRIEVE")
        self.addFormClass('RANGERETRIEVE', RangeRetrieve, name="RANGE RETRIEVE")

        # Create the temp directory
        try:
            os.mkdir(DA_DIR)
        except OSError:
           npyscreen.notify_confirm("A temp directory named %s already exists" %DA_DIR, editw=1,
                                     title='Warning:')

if __name__ == "__main__":
    
    # Startup error prompting, check for arguments and correctness.
    try:
        gui.arg = sys.argv[1]
    except IndexError:
        print("Please provide an argument.")
        raise SystemExit

    if gui.arg not in {'btree', 'hash', 'indexfile'}:
        print("Invalid argument. Use db_type arguments: btree, hash, or indexfile to run program")
        raise SystemExit

    app = MyApplication()
    app.run()

