#!/usr/bin/python3

import sys
import bsddb3 as bsddb
import random
import os
import npyscreen
import gui
from functions import *

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
        # self.addFormClass('DATARETRIEVE', DataRetrieve, name="DATA RETRIEVE")
        # self.addFormClass('RANGERETRIEVE', RangeRetrieve, name="RANGE RETRIEVE")
        
        # Create the temp directory
        try:
            os.mkdir(DA_DIR)
        except OSError:
            print("A temp directory named %s already exists % DA_DIR")

class KeyRetrieve(npyscreen.ActionPopup):
    def create(self):
        self.search_key = self.add(npyscreen.TitleText, name='Input Key:')

    def process_result(self, results, time):
        # THINK ABOUT HOW TO PROCESS ERRORS SOME MORE
        """
        Takes in results as a tuple of (key, value), and time, 
        and displays the desired results given in the form. 
        """

        if not results:
            npyscreen.notify_confirm("No results given.", editw=1,
                                     title='Result Error')
        for items in results:
            pass
        pass

    def on_ok(self):
        # ERROR PROCESSING
        if not self.search_key.value:
            npyscreen.notify_confirm("Please insert key to search by.", editw=1,
                                     title='Search Key Error')
            return

        try:
           self.results =  db.keys(self.search_key.value.encode(encoding='UTF-8'))
        except KeyError:
            npyscreen.notify_confirm("Invalid key entered. Database does not have key value", editw=1,
                                     title='Key Error')
        else:
            npyscreen.notify_confirm("STRANGE ERROR.", editw=1,
                                     title='Error')

        # Seperate Modules?   
        # Figure out why database is not being accessed.
        self.parentApp.switchFormPrevious()
    def on_cancel(self):
        self.parentApp.switchFormPrevious()

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
