import bsddb3 as bsddb
from functions import *
import gui
import npyscreen
import time

class DataRetrieve(npyscreen.ActionForm):
    def create(self):
        self.search_data = self.add(npyscreen.TitleText, name='Input Data:')

    def on_ok(self):
        if gui.arg == 'btree':
            db = bsddb.btopen(DA_FILE, 'r')
        elif gui.arg == 'hash':
            db = bsddb.hashopen(DA_FILE, 'r')
        
        result = None
        time1 = time.time()
        for item in db.iteritems():
            if item[1] == self.search_data.value.encode():
                time2 = time.time()
                timer = time2 - time1
                npyscreen.notify_confirm('\n\n'.join([
                    "Key found: %s"%item[0].decode(), "Time taken: %f"%timer]),
                                         editw=1, title='One result found:')
                result = item
                break
        time3 = time.time()
        timer = time3 - time1
        if not result:
                npyscreen.notify_confirm('\n\n'.join([
                    "No record found.", "Time taken: %f"%timer]),
                                         editw=1, title='Result:')
                
        if result:
            with open("log.out", mode='a') as fout:
                print("DATA_SEARCH: %s"%gui.arg,
                      "             data queried = %s"%self.search_data.value,
                      "             key returned = %s"%result[0].decode(),
                      "             time taken (s): %f"%(timer),
                      sep='\n', end='\n\n', file=fout)
        
        self.editing = True

    def on_cancel(self):
        self.parentApp.switchFormPrevious()
