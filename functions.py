import bsddb3 as bsddb
import random, os
# Make sure you run "mkdir /tmp/djp_db" first!
DA_DIR = "/tmp/djp_db/"
DA_FILE = "/tmp/djp_db/sample_db"
INDEX_FILE = "/tmp/djp_db/index_db"
DB_SIZE = 100 * 1000
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
        key = key.encode(encoding='UTF-8')
        value = value.encode(encoding='UTF-8')
        db[key] = value
    try:
        db.close()
    except Exception as e:
        print (e)

def dropDB(hashfile=False):
    # db.remove(DA_FILE) method should probably be called for now
    # os.remove clears the file out.
    os.remove(DA_FILE)

    if hashfile:
        os.remove(INDEX_FILE)


def makeINDEXFILE():
    try:
        db = bsddb.btopen(DA_FILE, "w")
    except:
        # print("DB doesn't exist, creating a new one")
        db = bsddb.btopen(DA_FILE, "c")

    try:
        indexfile = bsddb.hashopen(INDEX_FILE, "w")
    except:
        # print("DB doesn't exist, creating a new one")
        indexfile = bsddb.hashopen(INDEX_FILE, "c")

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
        key = key.encode()
        value = value.encode()
        db[key] = value
        indexfile[value] = key

    try:
        db.close()
        indexfile.close()
    except Exception as e:
        print (e)

