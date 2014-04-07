#!/usr/bin/python3
import npyscreen
from functions import *
import os
import shutil

arg = None

class MainMenu(npyscreen.FormBaseNew):
    def create(self):

# Define the 6 buttons' functions:
        def buttonpress0(*args):
            if arg == 'btree':
                makeBTREE()
            elif arg == 'hash':
                makeHASH()
            else:
                makeINDEXFILE()

        def buttonpress1(*args):
            self.parentApp.switchForm("KEYRETRIEVE")
        def buttonpress2(*args):
            self.parentApp.switchForm("DATARETRIEVE")
        def buttonpress3(*args):
            self.parentApp.switchForm("RANGERETRIEVE")
        def buttonpress4(*args):
            # Check for database file to remove. Return errors.
            try:
                dropDB(hashfile=(True if arg=='indexfile' else False))
            except Exception as e:
                npyscreen.notify_confirm(str(e),
                    title="Database File Error", editw=1) 
                return

            npyscreen.notify_confirm("Database file removed successfully",
                title="Database Deleted", editw=1)

        def buttonpress5(*args):
            self.parentApp.setNextForm(None)
            self.editing = False

            # Remove database and directory
            try:
                shutil.rmtree(DA_DIR)
            except OSError:
                npyscreen.notify_confirm("/tmp file could not be deleted",
                    title="File Error", editw=1) 
                return

            # Clear the answers file
            with open("answers", 'w') as fout:
                print('', file=fout)

            # Quit
            raise SystemExit

        # Create the buttons and link to the appropriate functions.
        self.button0 = self.add(npyscreen.ButtonPress, 
                                name="Create and populate the database")
        self.button0.whenPressed = buttonpress0
        self.button1 = self.add(npyscreen.ButtonPress,
                                name="Retrieve records with a given key")
        self.button1.whenPressed = buttonpress1
        self.button2 = self.add(npyscreen.ButtonPress,
                                name="Retrieve records with a given data")
        self.button2.whenPressed = buttonpress2
        self.button3 = self.add(npyscreen.ButtonPress,
                                name="Retrieve records with a given range of key values")
        self.button3.whenPressed = buttonpress3
        self.button4 = self.add(npyscreen.ButtonPress,
                                name="Destroy the database")
        self.button4.whenPressed = buttonpress4
        self.button5 = self.add(npyscreen.ButtonPress,
                                name="Quit")
        self.button5.whenPressed = buttonpress5




