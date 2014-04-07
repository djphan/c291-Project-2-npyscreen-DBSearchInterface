import npyscreen
import bsddb3 as bsddb
from functions import *
import gui 
import time

class KeyRetrieve(npyscreen.ActionForm):
    def create(self):
        self.search_key = self.add(npyscreen.TitleText, name='Input Key:')

    def process_result(self, results, time):
        """
        Takes in results as a tuple of (key, value), and time, 
        and displays the desired results given in the form. 

        Useful for setting the cursor.
        """
        if not results:
            npyscreen.notify_confirm("No results given. Time taken: %f" %time, editw=1,
                                     title='Result Error')


        if results:
            with open("answers", mode='a') as fout:
                print(results[0],
                      results[1],
                      '',
                      sep='\n', file=fout)

            npyscreen.notify_confirm('\n\n'.join([ 
                    "Time taken: %f microseconds"%time]),
                    editw=1, title='One result found:')

    def open_db(self):
        """
        Opens the database file to read (since it was closed on creation)
        """
        if gui.arg == 'btree':
            db =  bsddb.btopen(DA_FILE, "r")
        elif gui.arg == 'hash':
            db =  bsddb.hashopen(DA_FILE, "r")
        elif gui.arg == 'indexfile':
            db =  bsddb.btopen(DA_FILE, "r")
        return db

    def on_ok(self):
        # Error checking since all keys are 26 length random char strings 
        if not self.search_key.value:
            npyscreen.notify_confirm("Please insert key to search by.", editw=1,
                                     title='Search Key Error')
            return

        results = None

        try:
            # Generate results. 
            db_file = self.open_db()
            time1 = time.time() # Time 1
            # Return the result value by indexing into the db
            results = db_file[self.search_key.value.encode(encoding='UTF-8')].decode(encoding='UTF-8')
            time2 = time.time() # Time 2
            time_result = int((time2 - time1) * 1000 * 1000)
            results = (self.search_key.value, results)

        except KeyError:
            npyscreen.notify_confirm("Invalid key entered. Database does not have key value", 
                                     editw=1, title='Key Error')
            return
      
        self.process_result(results, time_result)
        self.editing = True

        try: db_file.close()
        except: pass

    def on_cancel(self):
        self.parentApp.switchFormPrevious()
