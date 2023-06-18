import sqlite3
import os
from flask import Flask, request, render_template

app = Flask(__name__)

db_path = os.path.join(app.root_path, 'instance', 'shoppingDB.sqlite')


@app.route('/', methods=['GET'])
def main():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    sql_fetch_query = """SELECT * FROM lists"""
    cursor.execute(sql_fetch_query)
    lists = cursor.fetchall()

    return render_template('index.html', list_content=lists)


@app.route('/addlist', methods=['POST', 'GET'])
def add_list():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    received_data_obj = request.form
    data_obj_to_save = dict(received_data_obj)

    data_model = {
        'lname': data_obj_to_save['lname'],
        'ldate': data_obj_to_save['ldate']
    }

    sql_query = """INSERT INTO lists (lname, ldate) VALUES (?, ?)"""
    cursor.execute(sql_query, (data_model['lname'], data_model['ldate']))
    conn.commit()

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    sql_fetch_query = """SELECT * FROM lists"""
    cursor.execute(sql_fetch_query)
    lists = cursor.fetchall()

    return render_template('index.html', list_content=lists)


@app.route('/viewfood', methods=['GET'])
def view_food():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    sql_fetch_query = """SELECT * FROM items"""
    cursor.execute(sql_fetch_query)
    items = cursor.fetchall()

    return render_template('viewFood.html', items_content=items)


@app.route('/list/<int:list_id>', methods=['GET'])
def disp_list(list_id):
    supermarket = 1

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    sql_fetch_query = """SELECT iname, iquantity, price, ipricetype FROM lists_items li, Items i, SupermarketsItems si
    WHERE li.lid=? 
    AND li.iid=i.iid 
    AND li.iid=si.iid
    AND si.sid=?
    """

    cursor.execute(sql_fetch_query, (list_id, supermarket,))
    lists_items = cursor.fetchall()

    sql_fetch_query = """SELECT lname, ldate FROM Lists WHERE lid=?"""
    cursor.execute(sql_fetch_query, (list_id,))
    list_name = cursor.fetchall()

    return render_template('dispList.html', list_items_content=lists_items, list_name=list_name)


if __name__ == '__main__':
    app.run(debug=True)
