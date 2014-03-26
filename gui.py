#!/usr/bin/python3
import npyscreen

class MyApplication(npyscreen.NPSAppManaged):
    """
    An NPS Managed Application. This class holds all the forms, manages their
    status, switches between them and displays them.
    
    To launch the application, an instance of MyApplication is created, and
    MyApplication.run is called.

    This happens automatically when this module is run as a script.
    """

    def onStart(self):
        self.addFormClass('MAIN', MainMenu, name="MAIN MENU")
        # self.addFormClass('KEYRETRIEVE', KeyRetrieve, name="KEY RETRIEVE")
        # self.addFormClass('DATARETRIEVE', DataRetrieve, name="DATA RETRIEVE")
        # self.addFormClass('RANGERETRIEVE', RangeRetrieve, name="RANGE RETRIEVE")

class MainMenu(npyscreen.FormBaseNew):
    def create(self):

# Define the 6 buttons' functions:
        def buttonpress0(*args):
            # Call Success popup
            pass
        def buttonpress1(*args):
            self.parentApp.switchForm("KEYRETRIEVE")
        def buttonpress2(*args):
            self.parentApp.switchForm("DATARETRIEVE")
        def buttonpress3(*args):
            self.parentApp.switchForm("RANGERETRIEVE")
        def buttonpress4(*args):
            # Call Success popup
            pass
        def buttonpress5(*args):
            self.parentApp.setNextForm(None)
            self.editing = False
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




