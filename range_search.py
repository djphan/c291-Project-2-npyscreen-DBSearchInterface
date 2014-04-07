import functions
import os
import time
import npyscreen
import gui
import pdb
import string
import random
NUM_TESTS = 4
RANGE_LEN = 200


class RangeRetrieve(npyscreen.ActionForm):
    def create(self):
        # open the appropriate database
        if gui.arg in {'btree', 'indexfile'}:
            self.db = functions.bsddb.btopen(functions.DA_FILE, "r")
            self.db_max_key = self.db.last()
        if gui.arg == 'hash':
            self.db = functions.bsddb.hashopen(functions.DA_FILE, "r")
        

        def notify_must_be_letter():
            npyscreen.notify_confirm("Your key prefixes must be made up of alpha chars",
                title="Error")

        def timer_bpress():
            ltrs = string.ascii_lowercase
            # deal with case where user has provided values
            if str(self.range_start.value) != '' and str(self.range_end.value) !='':
                self.user_key_pairs = []
                for ltr in self.range_start.value.lower():
                    if ltr not in ltrs:
                        notify_must_be_letter()
                        return
                for ltr in self.range_end.value.lower():
                    if ltr not in ltrs:
                        notify_must_be_letter()
                        return

                # set the range keys based on the user provided prefixes
                start_key = self.range_start.value.encode()
                end_key = self.range_end.value.encode()
                
                
                if gui.arg in {'btree', 'indexfile'}:
                    if end_key > self.db_max_key[0]:
                        # prevent user key input thats outside the db range
                        end_key = self.db_max_key[0]
                self.user_key_pairs.append((start_key, end_key))
                
            # perform the timed searches
            self.range_search_data = [] 
            self.user_range_search_data = []
            if gui.arg in {'btree', 'indexfile'}:
                if hasattr(self, 'key_pairs'):
                    for key_pair in self.key_pairs:
                        self.range_search_data.append(self.bt_range_search(key_pair))
                if hasattr(self, 'user_key_pairs'):
                    self.user_range_search_data.append(self.bt_range_search(self.user_key_pairs[0]))
            if gui.arg == 'hash':
                if hasattr(self, 'key_pairs'):
                    for key_pair in self.key_pairs:
                        self.range_search_data.append(self.ht_range_search(key_pair))
                if hasattr(self, 'user_key_pairs'):
                    self.user_range_search_data.append(self.ht_range_search(self.user_key_pairs[0]))
                        
            # if the user self generated the key pair just display the one result
            # otherwise display all 4 results from the auto generated pairs.
            if hasattr(self, 'user_key_pairs'):
                self.user_result.value = "Time: " + str(int(self.user_range_search_data[0][0] * 1000000)) +\
                    " microseconds. Range: " +\
                    str(len(self.user_range_search_data[0][1]))
            if hasattr(self, 'key_pairs'):
                self.result1.value = str(self.range_search_data[0][0] * 1000000) +\
                    " : Range " +\
                    str(len(self.range_search_data[0][1]))
                self.result2.value = str(self.range_search_data[1][0] * 1000000) +\
                    " : Range " +\
                    str(len(self.range_search_data[1][1]))
                self.result3.value = str(self.range_search_data[2][0] * 1000000) +\
                    " : Range " +\
                    str(len(self.range_search_data[2][1]))
                self.result4.value = str(self.range_search_data[3][0] * 1000000) +\
                    " : Range " +\
                    str(len(self.range_search_data[3][1]))

            # output data to answers file
            f = open("answers", "a")
            for record in self.user_range_search_data[0][1]:
                f.write(record[0].decode("utf-8") + '\n')
                f.write(record[1].decode("utf-8") + '\n\n')
            f.close()

            # save most recent auto generated key pairs
            f = open("range_key_pairs", "w+")
            f.write(self.key_pair_list.value)
            f.close()

        def generate_key_pairs():
            """
            generate pairs of keys for the range search
            static for possible external use
            """
            self.key_pairs = []
            # try to retrieve the key pairs saved from a previous test
            if os.path.isfile('range_key_pairs'):
                choice = npyscreen.notify_ok_cancel("Use key pairs from most recent test? \
                    Press cancel to generate a new set of key pairs and use them as a basis for future tests.")
                # generate new keys if user specifies
                if choice == 0:
                    self.auto_generate_keys()                         
                    self.attach_keys_to_fm()
                    return 
                # otherwise get keys from saved file
                else:
                    try:
                        self.key_pairs = []
                        f = open("range_key_pairs", "r")
                        # set the values on the form
                        keys = f.readline().split()
                        for key_pair in keys:
                            start_key, end_key = key_pair.split(':')
                            self.key_pairs.append((start_key.encode(), end_key.encode()))
                        f.close()
                        self.attach_keys_to_fm()
                        return
                    except Exception as e:
                        npyscreen.notify_confirm("Could not open key file from b-tree mode")
                        return
            # if no file exists generate new keys
            else:
                self.auto_generate_keys()
                self.attach_keys_to_fm()
                return

        # create form buttons and fields
        self.generate_button = self.add(npyscreen.ButtonPress,
            name="Generate key prefix pairs")
        self.key_pair_list = self.add(npyscreen.TitleText,
            name="Generated key pairs", editable=False)
        self.key_pair_list.value = "No keys generated."

        self.auto_timer_button = self.add(npyscreen.ButtonPress,
            name="Start auto generated keys timing process")
        self.auto_timer_button.whenPressed = timer_bpress 

        self.result1 = self.add(npyscreen.TitleText, 
            name="Result 1: ", editable=False)
        self.result2 = self.add(npyscreen.TitleText, 
            name="Result 2: ", editable=False)
        self.result3 = self.add(npyscreen.TitleText, 
            name="Result 3: ", editable=False)
        self.result4 = self.add(npyscreen.TitleText, 
            name="Result 4: ", editable=False)

        self.nextrely+=1
        self.enter_prefix = self.add(npyscreen.TitleText,
            name="Enter key pair prefixes of your own", editable=False)
        self.range_start = self.add(npyscreen.TitleText,
            name="Start Key: ")
        self.range_start.value = ''
        self.range_end = self.add(npyscreen.TitleText,
            name="End Key: ")
        self.range_end.value = ''

        self.nextrely+=1

        self.timer_button = self.add(npyscreen.ButtonPress,
            name="Start user generated key timing process")
        self.timer_button.whenPressed = timer_bpress
        self.generate_button.whenPressed = generate_key_pairs

        
        self.user_result = self.add(npyscreen.TitleText, 
            name="User provided key pair result: ", editable=False)
    
    def auto_generate_keys(self):
        # generate key pair prefixes
        self.key_pairs = []
        for i in range(NUM_TESTS):
            start_prefix1 = random.choice(string.ascii_lowercase)
            start_prefix2 = random.choice(string.ascii_lowercase[:-1])
            start_prefix = start_prefix1 + start_prefix2
            end_prefix1 = start_prefix1
            end_prefix2 = chr(ord(start_prefix2) + 1)
            end_prefix = end_prefix1 + end_prefix2
            start_key = start_prefix.encode()
            end_key = end_prefix.encode()
            self.key_pairs.append((start_key, end_key))
        return 

    def attach_keys_to_fm(self):
        # attach keys to the form to hold for later use.
        key_pair_string = ''
        for key_pair in self.key_pairs:
            key_pair_string += key_pair[0].decode() + ':' \
                + key_pair[1].decode() + '  '
        self.key_pair_list.value = key_pair_string
        return

    def bt_range_search(self, key_pair):
        # go to first key, iterate through to last in range.
        range_set = []
        t0 = time.time()
        current = self.db.set_location(key_pair[0])
        while True: 
            if current[0] < key_pair[1]:
                range_set.append(current)
                current = self.db.next() 
            elif current[0] == key_pair[1]:
                range_set.append(current)
                break
            elif current[0] > key_pair[1]:
                break
        total_time = time.time() - t0
        return (total_time, range_set)

    def ht_range_search(self, key_pair):
        range_set = []
        t0 = time.time()
        end_index_key = self.db.last()[0]
        current_index = self.db.first()
        # iterate through each key/data pair and check whether
        # the key is in the range, if so append.
        while current_index[0] != end_index_key:
            if current_index[0] >= key_pair[0] and \
                current_index[0] <= key_pair[1]:
                    range_set.append(current_index)
            current_index = self.db.next()
        
        # keep last key check outside loop
        if current_index[0] == end_index_key and \
            current_index[0] >= key_pair[0] and \
            current_index[0] <= key_pair[1]:
                range_set.append(current_index)
        total_time = time.time() - t0
        return (total_time, range_set)
        
    def on_ok(self):
        self.db.close()
        self.parentApp.switchFormPrevious()

    def on_cancel(self):
        self.db.close()
        self.parentApp.switchFormPrevious()
