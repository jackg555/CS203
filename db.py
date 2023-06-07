import sqlite3

conn = sqlite3.connect('groceries.sqlite')
cursor = conn.cursor()
sql_query = """CREATE TABLE IF NOT EXISTS groceries (
    id integer PRIMARY KEY,
    name text NOT NULL,
    cdprice integer NOT NULL,
    nwprice integer NOT NULL,
    pnsprice integer NOT NULL
    )"""
cursor.execute(sql_query)