#!/usr/bin/python3

import sys
import bsddb3 as bsddb
import random
import os
import npyscreen
import gui
from functions import *
from datasearch import DataRetrieve
# from keysearch import KeyRetrieve

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
        # self.addFormClass('RANGERETRIEVE', RangeRetrieve, name="RANGE RETRIEVE")
        # Create the temp directory

        try:
            os.mkdir(DA_DIR)
        except OSError:
           npyscreen.notify_confirm("A temp directory named %s already exists" %DA_DIR, editw=1,
                                     title='Result Error')

class KeyRetrieve(npyscreen.ActionForm):
    def create(self):
        """
        Create the fields for npyscreen to take in the key query.
        """
        self.search_key = self.add(npyscreen.TitleText, name='Input Key:')
        self.nextrely+=1
        self.results = self.add(npyscreen.Pager, name="Results:", height=14,
                                max_height=14, scroll_exit=True,
                                slow_scroll=True, exit_left=True,
                                exit_right=True)

    def process_result(self, results, time):
        """
        Takes in results as a tuple of (key, value), and time, 
        and displays the desired results given in the form. 
        """
        if not results:
            npyscreen.notify_confirm("No results given.", editw=1,
                                     title='Result Error')

        self.results.values = ['\n']
        joined = dict()

        for items in results:
            if not items[1] in joined:
                # Format output nicely.
                joined[items[1]] = list()
                joined[items[1]].append("Key: %s\n"%items[0])
                joined[items[1]].append("Value: %s\n"%items[1])
                joined[items[1]].append("Time: %s\n"%time)
            else:
                joined[items[1]].insert(-2, ' '*26+'\n')

        for values in joined:
            self.results.values.extend(joined[values])

    def open_file(self, arg):
        if arg == 'btree':
            # should this be in "w" mode or "r" mode? -carl
            results =  bsddb.btopen(DA_FILE, "w").set_location(self.search_key.value.encode(encoding='UTF-8'))

        elif arg == 'hash':
           results =  bsddb.hashopen(DA_FILE, "w").set_location(self.search_key.value.encode(encoding='UTF-8'))

        else:
            # Indexfile
            pass

        return results

    def on_ok(self):
        if not self.search_key.value:
            npyscreen.notify_confirm("Please insert key to search by.", editw=1,
                                     title='Search Key Error')
            return

        try:
            # Note should check for what mode is executed. Currently only working for b-tree.
            results = self.open_file(gui.arg)
            # Close this file later
            results = (results[0].decode(encoding='UTF-8'), results[1].decode(encoding='UTF-8'))

        except KeyError:
            npyscreen.notify_confirm("Invalid key entered. Database does not have key value", 
                                     editw=1, title='Key Error')
            return

       
        npyscreen.notify_confirm(str(results), editw=1,
                                     title='Search Key Error')

        self.process_result(results, 10)
        
        # Close database file?
        #bsddb.close()

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

