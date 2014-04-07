import bsddb3 as bsddb
import random, os
# Make sure you run "mkdir /tmp/djp_db" first!

# Setting file paths for our database
DA_DIR = "/tmp/djp_db/"
DA_FILE = "/tmp/djp_db/sample_db"
INDEX_FILE = "/tmp/djp_db/index_db"

# Set seeds to generate the random char strings
DB_SIZE = 100 * 1000
SEED = 10000000


# Program taken from the sample python3.py program
# Generate psudo-random char strings using the above setting.
def get_random():
    return random.randint(0, 63)
def get_random_char():
    return chr(97 + random.randint(0, 25))

def makeBTREE():
    # Attempt to write/create the database file.
    try:
        db = bsddb.btopen(DA_FILE, "w")
    except:
        db = bsddb.btopen(DA_FILE, "c")
    random.seed(SEED)

    # Set database values with the random chars generated.
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
    # Attempt to write/create the database file.
    try:
        db = bsddb.hashopen(DA_FILE, "w")
    except:
        print("DB doesn't exist, creating a new one")
        db = bsddb.hashopen(DA_FILE, "c")
    random.seed(SEED)

    # Set database values with the random chars generated.
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
    os.remove(DA_FILE)
    if hashfile:
        os.remove(INDEX_FILE)

def makeINDEXFILE():
    # Attempt to write/create the database file.
    try:
        db = bsddb.btopen(DA_FILE, "w")
    except:
        db = bsddb.btopen(DA_FILE, "c")

    # Attempt to write/create the index file.
    try:
        indexfile = bsddb.hashopen(INDEX_FILE, "w")
    except:
        indexfile = bsddb.hashopen(INDEX_FILE, "c")

    # Set database values with the random chars generated.
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

        # Database file and index file are inverse of each other.
        db[key] = value
        indexfile[value] = key

    try:
        db.close()
        indexfile.close()
    except Exception as e:
        print (e)

