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
    #supermarket is set to new world (supermarket = 1)
    supermarket = 1

    conn = sqlite3.connect('shoppingDB.sqlite')
    cursor = conn.cursor()

    sql_fetch_query = """SELECT iname, iquantity, price FROM ListsItems li, Items i, SupermarketsItems si
    WHERE li.lid=? 
    AND li.iid=i.iid 
    AND li.iid=si.iid
    AND si.sid=?
    """
    cursor.execute(sql_fetch_query, (list_id,supermarket,))
    ListsItems = cursor.fetchall()

    sql_fetch_query = """SELECT lname, ldate FROM Lists WHERE lid=?"""
    cursor.execute(sql_fetch_query, (list_id,))
    ListName = cursor.fetchall()

    return render_template('dispList.html', list_items_content=ListsItems, list_name=ListName)

if __name__ == '__main__':
    app.run(debug=True)