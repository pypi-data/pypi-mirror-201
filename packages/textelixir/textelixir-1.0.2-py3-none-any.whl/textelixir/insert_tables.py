import sqlite3
from sqlite3 import Error

def insert_metadata_value(conn, table_name, row_id, value):
    try:
        c = conn.cursor()
        c.execute(f"""INSERT INTO {table_name} (id, value) VALUES({row_id}, '{value}');""")
    except Error as e:
        print(e)

def insert_word_value(conn, table_name, row_id, value_list):
    columns = 'word, pos, xpos, lemma' if len(value_list) > 1 else 'word'
    values = ', '.join(f"'{value}'" if value != 'NULL' else "NULL" for value in value_list)
    
    try:
        c = conn.cursor()
        c.execute(f"""INSERT INTO {table_name} (id, {columns}) VALUES({row_id}, {values});""")
    except Error as e:
        print(e)

def insert_corpus_value(conn, columns, values):
    column_names = ', '.join(columns)
    values = ', '.join([str(v) for v in values])
    try:
        c = conn.cursor()
        c.execute(f"""INSERT INTO corpus ({column_names}) VALUES({values});""")
    except Error as e:
        print(e)