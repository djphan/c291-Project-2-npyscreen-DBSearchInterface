import functions
import time
import npyscreen
import gui
import pdb
import string
import random
from timeit import Timer
NUM_TESTS = 4
RANGE_LEN = 200


class RangeRetrieve(npyscreen.ActionForm):
    def create(self):
        # open the appropriate database
        if gui.arg == 'btree':
            self.db = functions.bsddb.btopen(functions.DA_FILE, "r")
        if gui.arg == 'hash':
            self.db = functions.bsddb.hashopen(functions.DA_FILE, "r")

        def timer_bpress():
            # list will be populated with tuples of (search time,
            # search results)
            self.range_search_data = [] 
            if gui.arg == 'btree':
                for key_pair in self.key_pairs:
                    self.range_search_data.append(self.bt_range_search(key_pair))
            if gui.arg == 'hash':
                for key_pair in self.key_pairs:
                    self.range_search_data.append(self.ht_range_search(key_pair))

            # output the results and range for testing purposes
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
            f = open("answers", "w+")
            for i in range(NUM_TESTS):
                for record in self.range_search_data[i][1]:
                    f.write(record[0].decode("utf-8") + '\n')
                    f.write(record[1].decode("utf-8") + '\n\n')
            f.close()

        def generate_key_pairs():
            """
            generate pairs of keys for the range search
            static for possible external use
            """
            self.key_pairs = []
            db_keys = self.db.keys()
            if gui.arg == 'btree':
                for i in range(NUM_TESTS):
                    # generate a random char prefix generates smaller key range
                    # for testing on db size of 1000
                    if functions.DB_SIZE == 1000:
                        start_prefix = random.choice(string.ascii_letters[:-1]).lower()
                        end_prefix = chr(ord(start_prefix) + 1)
                        start_key = self.db.set_location(start_prefix.encode(encoding='UTF-8'))[0]
                        end_key = self.db.set_location(end_prefix.encode(encoding='UTF-8'))[0]
                        self.key_pairs.append((start_key, end_key))
                    else:
                        start_prefix1 = random.choice(string.ascii_letters).lower()
                        start_prefix2 = random.choice(string.ascii_letters[:-1]).lower()
                        start_prefix = start_prefix1 + start_prefix2
                        end_prefix1 = start_prefix1
                        end_prefix2 = chr(ord(start_prefix2) + 1)
                        end_prefix = end_prefix1 + end_prefix2
                        start_key = self.db.set_location(start_prefix.encode(encoding='UTF-8'))[0]
                        end_key = self.db.set_location(end_prefix.encode(encoding='UTF-8'))[0]
                        self.key_pairs.append((start_key, end_key))
                return

            # this needs work to be TA approved.
            if gui.arg == 'hash':
                key_count = 0
                while True:
                    while key_count < 4:
                        self.db_keys_sorted = db_keys.sort()
                        rand_key_index = random.randint(0, len(db_keys))
                        rand_start_key = db_keys[rand_key_index]
                        try:
                            end_key = db_keys[rand_key_index + RANGE_LEN]
                        except Exception as e:
                            break
                        self.key_pairs.append((rand_start_key, end_key))
                        key_count += 1
                    if key_count > 3:
                        break
            
            return

        # create form buttons and fields
        self.nextrely+=1
        self.generate_button = self.add(npyscreen.ButtonPress,
            name="Generate key pairs")
        self.timer_button = self.add(npyscreen.ButtonPress,
            name="Start timing process")
        self.timer_button.whenPressed = timer_bpress
        self.generate_button.whenPressed = generate_key_pairs
        self.nextrely+=1
        self.result1 = self.add(npyscreen.TitleText, 
            name="Result 1: ", editable=False)
        self.result2 = self.add(npyscreen.TitleText, 
            name="Result 2: ", editable=False)
        self.result3 = self.add(npyscreen.TitleText, 
            name="Result 3: ", editable=False)
        self.result4 = self.add(npyscreen.TitleText, 
            name="Result 4: ", editable=False)


    def bt_range_search(self, key_pair):
        # for the time being append to a list but ask about this.
        range_set = []
        t0 = time.time()
        current = self.db.set_location(key_pair[0])
        while current[0] != key_pair[1]:
            range_set.append(current)
            current = self.db.next() 
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
            current_index[0] >=key_pair[0] and \
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
