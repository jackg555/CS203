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

    return render_template('addlist.html', list_content = Lists)

@app.route('/viewlistjson', methods=['GET'])
def viewFoodJson():
    conn = sqlite3.connect('shoppingDB.sqlite')
    cursor = conn.cursor()

    sql_fetch_query = """SELECT * FROM Lists"""
    cursor.execute(sql_fetch_query)
    Lists = cursor.fetchall()

    return jsonify(Lists)

@app.route('/addlist', methods=['POST'])
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

    return 'List Added Successfully', 201

if __name__ == '__main__':
    app.run(debug=True)