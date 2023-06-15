from flask import Flask, request, render_template, jsonify
import sqlite3

app = Flask (__name__)
@app.route('/', methods=['GET'])
def main():
    conn = sqlite3.connect('shoppingDB.sqlite')
    cursor = conn.cursor()

    sql_fetch_query = """SELECT * FROM Lists"""
    cursor.execute(sql_fetch_query)
    Lists = cursor.fetchall()

    return render_template('index.html', list_content=Lists)
@app.route('/addlist', methods=['POST', 'GET'])
def addList():
    conn = sqlite3.connect('shoppingDB.sqlite')
    cursor = conn.cursor()

    received_data_obj = request.form
    data_obj_to_save = dict(received_data_obj)

    data_model = {
        'lname': data_obj_to_save['lname'],
        'ldate': data_obj_to_save['ldate']
    }

    sql_query = """INSERT INTO Lists (lname, ldate) VALUES (?, ?)"""
    cursor.execute(sql_query, (data_model['lname'], data_model['ldate']))
    conn.commit()

    conn = sqlite3.connect('shoppingDB.sqlite')
    cursor = conn.cursor()

    sql_fetch_query = """SELECT * FROM Lists"""
    cursor.execute(sql_fetch_query)
    Lists = cursor.fetchall()

    return render_template('index.html', list_content = Lists)

@app.route('/viewfood', methods=['GET'])
def viewFood():
    conn = sqlite3.connect('shoppingDB.sqlite')
    cursor = conn.cursor()

    sql_fetch_query = """SELECT * FROM Items"""
    cursor.execute(sql_fetch_query)
    Items = cursor.fetchall()

    return render_template('viewFood.html', items_content=Items)

@app.route('/list/<int:list_id>', methods=['GET'])
def dispList(list_id):
    conn = sqlite3.connect('shoppingDB.sqlite')
    cursor = conn.cursor()

    #fix "lid=1" as this needs to be list_id not 1
    sql_fetch_query = """SELECT * FROM ListsItems WHERE lid=1"""
    cursor.execute(sql_fetch_query)
    ListsItems = cursor.fetchall()

    sql_fetch_query = """SELECT * FROM Items"""
    cursor.execute(sql_fetch_query)
    Items = cursor.fetchall()

    return render_template('dispList.html', list_items_content=ListsItems, items_content=Items)

if __name__ == '__main__':
    app.run(debug=True)