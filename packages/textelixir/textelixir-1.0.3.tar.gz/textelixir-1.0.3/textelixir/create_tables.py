import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_option_table(conn, lang, tagger):
    try:
        c = conn.cursor()
        # TODO: We may want to try making a determination on whether it should be a string or integer.
        c.execute(f"""CREATE TABLE option (lang TEXT, tagger TEXT);""")
        c.execute(f"""INSERT INTO option (lang, tagger) VALUES('{lang}', '{tagger}');""")
    except Error as e:
        print(e)


def create_metadata_table(conn, table_name):
    try:
        c = conn.cursor()
        # TODO: We may want to try making a determination on whether it should be a string or integer.
        c.execute(f"""CREATE TABLE {table_name} (id INTEGER PRIMARY KEY, value TEXT);""")
    except Error as e:
        print(e)


def create_corpus_table(conn, columns):
    sql_columns = ', '.join([f'{c} INTEGER' for c in columns])
    try:
        c = conn.cursor()
        # TODO: We may want to try making a determination on whether it should be a string or integer.
        c.execute(f"""CREATE TABLE corpus (id INTEGER PRIMARY KEY AUTOINCREMENT, {sql_columns});""")
    except Error as e:
        print(e)

def create_word_table(conn, columns):
    sql_columns = ', '.join([f'{c} TEXT' for c in columns])
    try:
        c = conn.cursor()
        # TODO: We may want to try making a determination on whether it should be a string or integer.
        c.execute(f"""CREATE TABLE word (id INTEGER PRIMARY KEY, {sql_columns});""")
    except Error as e:
        print(e)