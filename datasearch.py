import bsddb3 as bsddb
from functions import *
import gui
import npyscreen
import time

class DataRetrieve(npyscreen.ActionForm):
    def create(self):
        self.search_data = self.add(npyscreen.TitleText, name='Input Data:')

    def on_ok(self):
        if gui.arg == 'indexfile':
            self.index_file_retrieve_data()
            self.editing=True
            return

        if gui.arg == 'btree':
            db = bsddb.btopen(DA_FILE, 'r')
        elif gui.arg == 'hash':
            db = bsddb.hashopen(DA_FILE, 'r')
        

        # Here we loop through all the data items in the database:
        time1 = time.time()     # START TIMER
        result = [item[0] for item in db.iteritems()
                  if item[1] == self.search_data.value.encode()]
        time2 = time.time()     # STOP TIMER


        timer = int((time2 - time1) * 1000 * 1000)
        if not result:
            npyscreen.notify_confirm('\n\n'.join([
                        "No record found.", "Time taken: %f"%timer]),
                                     editw=1, title='Result:')
                
        else:
            npyscreen.notify_confirm("%d records retrieved.\n"%(len(result)) +
                                     "Execution time: %d microseconds."%(timer),
                                     editw=1, title='Result:')
            with open("log.out", mode='a') as fout:
                print("DATA_SEARCH: %s"%gui.arg,
                      "             data queried = %s"%self.search_data.value,
                      "             key returned = %s"%result[0].decode(),
                      "             time taken (s): %d"%(timer),
                      sep='\n', end='\n\n', file=fout)
        
        try: db.close()
        except: pass
        self.editing = True

    def on_cancel(self):
        self.parentApp.switchFormPrevious()

    def index_file_retrieve_data(self):
        index = bsddb.hashopen(INDEX_FILE, 'r')

        time1 = time.time()
        result = index[self.search_data.value.encode()].decode()
        time2 = time.time()

        timer = int((time2 - time1) * 1000 * 1000)
        npyscreen.notify_confirm("One record retrieved.\n" +
                                 "Execution time: %d microseconds."%(timer),
                                 editw=1, title='Result:')
        with open("log.out", mode='a') as fout:
            print("DATA_SEARCH: %s"%gui.arg,
                  "             data queried = %s"%self.search_data.value,
                  "             key returned = %s"%result,
                  "             time taken (s): %d"%(timer),
                  sep='\n', end='\n\n', file=fout)

        try: index.close()
        except: pass
        
        
