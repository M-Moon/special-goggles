""" Server Database Handling """

import sqlite3

def db_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except sqlite3.Error as e:
        print(e)
    finally:
        conn.close()

db_connection('userdatabase.db')
