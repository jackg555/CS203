import sqlite3
import os

db_path = os.path.join(os.getcwd(), 'instance', 'shoppingDB.sqlite')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

sql_query = """CREATE TABLE IF NOT EXISTS Items (
        iid integer NOT NULL, 
        iname text NOT NULL,
        iquantity text NOT NULL,
        ipricetype text NOT NULL,
        primary key (iid)
        );"""
cursor.execute(sql_query)

sql_query = """CREATE TABLE IF NOT EXISTS Supermarkets (
        sid integer NOT NULL, 
        sname text NOT NULL,
        slocation text NOT NULL,
        snumber integer NOT NULL,
        primary key (sid)
        );"""
cursor.execute(sql_query)

sql_query = """CREATE TABLE IF NOT EXISTS Lists (
        lid integer NOT NULL, 
        lname text NOT NULL, 
        ldate text NOT NULL,
        primary key (lid)
        );"""
cursor.execute(sql_query)

sql_query = """CREATE TABLE IF NOT EXISTS SupermarketsItems (
        iid integer NOT NULL, 
        sid integer NOT NULL, 
        price text NOT NULL,
        primary key (iid, sid), 
        foreign key (iid) references Items(iid),
        foreign key (sid) references Supermarkets(sid)
        );"""
cursor.execute(sql_query)

sql_query = """CREATE TABLE IF NOT EXISTS ListsItems (
        lid integer NOT NULL, 
        iid integer NOT NULL, 
        lquantity integer NOT NULL, 
        primary key (lid, iid), 
        foreign key (lid) references Lists(lid), 
        foreign key (iid) references Items(iid)
        );"""
cursor.execute(sql_query)
