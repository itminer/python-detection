# -*- coding: utf-8 -*-
import os
import io
import numpy as np
import sqlite3 as sq

db_name = 'sock.db'
tb_name = 'socklist'

def adapt_array(arr):
    """
    http://stackoverflow.com/a/31312102/190597 (SoulNibbler)
    """
    out = io.BytesIO()
    np.save(out, arr)
    out.seek(0)
    return sq.Binary(out.read())

def convert_array(text):
    out = io.BytesIO(text)
    out.seek(0)
    return np.load(out)

# Converts np.array to TEXT when inserting
sq.register_adapter(np.ndarray, adapt_array)
# Converts TEXT to np.array when selecting
sq.register_converter("array", convert_array)

def make_db(db_name,tb_name):
    conn = sq.connect(db_name, detect_types=sq.PARSE_DECLTYPES)
    curs = conn.cursor()
    curs.execute("CREATE TABLE "+tb_name+"(id INTEGER PRIMARY KEY,name varchar(255) NOT NULL,des array)")
    print("Success")
    conn.commit()
    conn.close()

def get_all():
    if not os.path.isfile(db_name):
        make_db(db_name, tb_name)
    conn = sq.connect(db_name, detect_types=sq.PARSE_DECLTYPES)
    curs = conn.cursor()
    ret = []
    for row in curs.execute("SELECT * FROM "+tb_name):
        ret.append(row)
    conn.commit()
    conn.close()
    return ret

def insert_info(name, des):
    if not os.path.isfile(db_name):
        make_db(db_name, tb_name)
    conn = sq.connect(db_name, detect_types=sq.PARSE_DECLTYPES)
    curs = conn.cursor()
    values = [(name, des)]
    curs.executemany("INSERT INTO " + tb_name + "(name, des) VALUES (?,?)", values)
    print("Success")
    conn.commit()
    conn.close()

def select_by_name(name):
    if not os.path.isfile(db_name):
        make_db(db_name, tb_name)
    conn = sq.connect(db_name, detect_types=sq.PARSE_DECLTYPES)
    curs = conn.cursor()
    ret = []
    for row in curs.execute("SELECT * FROM socklist WHERE name ='" + name + "'"):
        ret.append(row)
    conn.commit()
    conn.close()
    print(ret)
    return ret

def isNameExist(name):
    if not os.path.isfile(db_name):
        make_db(db_name, tb_name)
    ret = select_by_name(name)
    if len(ret) > 0:
        return True
    else:
        return False

# if __name__ == '__main__':
#     if not os.path.isfile(db_name):
#         make_db(db_name, tb_name)
#     else:
#         get_all()
        





