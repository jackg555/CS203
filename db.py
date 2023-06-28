import sqlite3
import os

db_path = os.path.join(os.getcwd(), 'instance', 'kiwibasketDB.sqlite')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

sql_query = """CREATE TABLE IF NOT EXISTS Items (
        item_id integer NOT NULL, 
        item_name text NOT NULL,
        item_quantity text NOT NULL,
        item_price_type text NOT NULL,
        primary key (item_id)
        );"""
cursor.execute(sql_query)

sql_query = """CREATE TABLE IF NOT EXISTS Supermarkets (
        smarket_id integer NOT NULL, 
        smarket_name text NOT NULL,
        smarket_location text NOT NULL,
        smarket_number integer NOT NULL,
        primary key (smarket_id)
        );"""
cursor.execute(sql_query)

sql_query = """CREATE TABLE IF NOT EXISTS Lists (
        list_id integer NOT NULL, 
        list_name text NOT NULL, 
        list_date text NOT NULL,
        primary key (list_id)
        );"""
cursor.execute(sql_query)

sql_query = """CREATE TABLE IF NOT EXISTS SupermarketsItems (
        item_id integer NOT NULL, 
        smarket_id integer NOT NULL, 
        price float NOT NULL,
        primary key (item_id, smarket_id), 
        foreign key (item_id) references Items(item_id),
        foreign key (smarket_id) references Supermarkets(smarket_id)
        );"""
cursor.execute(sql_query)

sql_query = """CREATE TABLE IF NOT EXISTS ListsItems (
        list_id integer NOT NULL, 
        item_id integer NOT NULL, 
        list_quantity float NOT NULL, 
        primary key (list_id, item_id), 
        foreign key (list_id) references Lists(list_id) ON DELETE CASCADE, 
        foreign key (item_id) references Items(item_id)
        );"""
cursor.execute(sql_query)
