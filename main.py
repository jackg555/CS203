from flask import Flask,request
import sqlite3

app = Flask (__name__)

@app.route('/groceries', methods=['GET','POST'])
def insertFood():
    conn = sqlite3.connect('groceries.sqlite')
    cursor = conn.cursor()

    if request.method == 'GET':
        sql_search = """SELECT * FROM groceries"""
        cursor.execute(sql_search)
        food = cursor.fetchall()
        return {"food": food}, 200

    elif request.method == 'POST':
        request_data = request.get_json()
        new_food = {
            "name": request_data['name'],
            "cdprice": request_data['cdprice'],
            "nwprice": request_data['nwprice'],
            "pnsprice": request_data['pnsprice']
        }

        sql_query = """INSERT INTO groceries (name, cdprice, nwprice, pnsprice) VALUES (?, ?, ?, ?)"""
        cursor.execute(sql_query, (new_food['name'], new_food['cdprice'], new_food['nwprice'], new_food['pnsprice']))
        conn.commit()
        return new_food, 201

if __name__ == '__main__':
    app.run(debug=True)