from flask import Flask,request, render_template
import sqlite3

app = Flask (__name__)

#@app.route('/groceries', methods=['GET','POST'])
#def insertFood():
    #conn = sqlite3.connect('groceries.sqlite')
    #cursor = conn.cursor()

    #if request.method == 'GET':
        #sql_search = """SELECT * FROM groceries"""
        #cursor.execute(sql_search)
        #food = cursor.fetchall()
        #return {"food": food}, 200

    #elif request.method == 'POST':
        #request_data = request.get_json()
        #new_food = {
            #"name": request_data['name'],
            #"cdprice": request_data['cdprice'],
            #"nwprice": request_data['nwprice'],
            #"pnsprice": request_data['pnsprice']
        #}

        #sql_query = """INSERT INTO groceries (name, cdprice, nwprice, pnsprice) VALUES (?, ?, ?, ?)"""
        #cursor.execute(sql_query, (new_food['name'], new_food['cdprice'], new_food['nwprice'], new_food['pnsprice']))
        #conn.commit()
        #return new_food, 201

@app.route('/', methods=['GET'])
def main():
    return render_template('addfood.html')

@app.route('/viewfood', methods=['GET'])
def viewFood():
    conn = sqlite3.connect('groceries.sqlite')
    cursor = conn.cursor()

    sql_fetch_query = """SELECT * FROM groceries"""
    cursor.execute(sql_fetch_query)
    groceries = cursor.fetchall()

    return render_template('viewfood.html', food_content = groceries)

@app.route('/addfood', methods=['POST'])
def addFood():
    conn = sqlite3.connect('groceries.sqlite')
    cursor = conn.cursor()

    received_data_obj = request.form
    data_obj_to_save = dict(received_data_obj)

    data_model = {
        'name': data_obj_to_save['name'],
        'cdprice': data_obj_to_save['cdprice'],
        'nwprice': data_obj_to_save['nwprice'],
        'pnsprice': data_obj_to_save['pnsprice']
    }

    sql_query = """INSERT INTO groceries (name, cdprice, nwprice, pnsprice) VALUES (?, ?, ?, ?)"""
    cursor.execute(sql_query,
                   (data_model['name'],
                   data_model['cdprice'],
                   data_model['nwprice'],
                   data_model['pnsprice']))
    conn.commit()

    return 'Food added successfully', 201

if __name__ == '__main__':
    app.run(debug=True)