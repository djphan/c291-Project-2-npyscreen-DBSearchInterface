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
        """
        if not results:
            npyscreen.notify_confirm("No results given. Time taken: %f" %time, editw=1,
                                     title='Result Error')


        if results:
            with open("log.out", mode='a') as fout:
                print("KEY_SEARCH: %s"%gui.arg,
                      "             key queried = %s"%results[0],
                      "             data returned = %s"%results[1],
                      "             time taken (s): %f"%(time),
                      sep='\n', end='\n\n', file=fout)

            npyscreen.notify_confirm('\n\n'.join([
                    "Key Queried: %s \n"%results[0], 
                    "Value found: %s \n"%results[1], 
                    "Time taken: %f"%time]),
                    editw=1, title='One result found:')

        #self.results.values = ['\n']
        #joined = dict()

        #for items in results:
            #if not items[1] in joined:
                #joined[items[1]] = list()
                #joined[items[1]].append("Key: %s\n"%items[0])
                #joined[items[1]].append("Value: %s\n"%items[1])
                #joined[items[1]].append("Time: %s\n"%time)
            #else:
                #joined[items[1]].insert(-2, ' '*26+'\n')

        #for values in joined:
            #self.results.values.extend(joined[values])

    def open_db(self):
        """
        Opens the database file to read (since it was closed on creation)
        """
        if gui.arg == 'btree':
            db =  bsddb.btopen(DA_FILE, "r")

        elif gui.arg == 'hash':
            db =  bsddb.hashopen(DA_FILE, "r")
        else:
            # Open Indexfile
            pass
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
            time1 = time.time()
            # Returns a tuple of (key, value) using the BerkleyDB cursor
            results = self.open_db().set_location(self.search_key.value.encode(encoding='UTF-8'))
            time2 = time.time()
            time_result = int((time2 - time1) * 1000 * 1000)

            results = (results[0].decode(encoding='UTF-8'), results[1].decode(encoding='UTF-8'))

        except KeyError:
            npyscreen.notify_confirm("Invalid key entered. Database does not have key value", 
                                     editw=1, title='Key Error')
            return
       
        #npyscreen.notify_confirm(str(results), editw=1,
        #                             title='Search Key Error')
        self.process_result(results, time_result)

        self.editing = True

    def on_cancel(self):
        self.parentApp.switchFormPrevious()
