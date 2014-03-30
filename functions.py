import bsddb3 as bsddb
import random, os
# Make sure you run "mkdir /tmp/my_db" first!
DA_DIR = "/tmp/djphan_db/"
DA_FILE = "/tmp/djphan_db/sample_db"
DB_SIZE = 1000
SEED = 10000000

def get_random():
    return random.randint(0, 63)
def get_random_char():
    return chr(97 + random.randint(0, 25))

def makeBTREE():
    try:
        db = bsddb.btopen(DA_FILE, "w")
    except:
        # print("DB doesn't exist, creating a new one")
        db = bsddb.btopen(DA_FILE, "c")
    random.seed(SEED)

    for index in range(DB_SIZE):
        krng = 64 + get_random()
        key = ""
        for i in range(krng):
            key += str(get_random_char())
        vrng = 64 + get_random()
        value = ""
        for i in range(vrng):
            value += str(get_random_char())
        # print (key)
        # print (value)
        # print ("")
        key = key.encode(encoding='UTF-8')
        value = value.encode(encoding='UTF-8')
        db[key] = value
    try:
        db.close()
    except Exception as e:
        print (e)

def makeHASH():
    try:
        db = bsddb.hashopen(DA_FILE, "w")
    except:
        print("DB doesn't exist, creating a new one")
        db = bsddb.hashopen(DA_FILE, "c")
    random.seed(SEED)

    for index in range(DB_SIZE):
        krng = 64 + get_random()
        key = ""
        for i in range(krng):
            key += str(get_random_char())
        vrng = 64 + get_random()
        value = ""
        for i in range(vrng):
            value += str(get_random_char())
        #print (key)
        #print (value)
        #print ("")
        key = key.encode(encoding='UTF-8')
        value = value.encode(encoding='UTF-8')
        db[key] = value
    try:
        db.close()
    except Exception as e:
        print (e)

def dropDB():
    # db.remove(DA_FILE) method should probably be called for now
    # os.remove clears the file out.
    os.remove(DA_FILE)
