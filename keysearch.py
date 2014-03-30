import npyscreen

# Problems with circular dependancies? - DP
import bsddb3 as bsddb
from functions import *
import gui 


class KeyRetrieve(npyscreen.ActionForm):
    def create(self):
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
            results = self.open_file(*args)
            # Close this file later
            results = (results[0].decode(encoding='UTF-8'), results[1].decode(encoding='UTF-8'))

        except KeyError:
            npyscreen.notify_confirm("Invalid key entered. Database does not have key value", 
                                     editw=1, title='Key Error')
            return

       
        npyscreen.notify_confirm(str(results), editw=1,
                                     title='Search Key Error')
        self.process_result(results, 10)

    def on_cancel(self):
        self.parentApp.switchFormPrevious()
