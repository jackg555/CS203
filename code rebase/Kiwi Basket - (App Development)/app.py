import sqlite3
import os
from flask import Flask, request, render_template

app = Flask(__name__)

db_path = os.path.join(app.root_path, 'instance', 'shoppingDB.sqlite')

def fetch_list_items(list_id):
    supermarket = 1

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    sql_fetch_query = """SELECT iname, iquantity, price, ipricetype, lquantity, li.iid
        FROM ListsItems li, Items i, SupermarketsItems si
        WHERE li.lid=? 
        AND li.iid=i.iid 
        AND li.iid=si.iid
        AND si.sid=?
        """

    cursor.execute(sql_fetch_query, (list_id, supermarket,))
    lists_items = cursor.fetchall()

    sql_fetch_query = """SELECT * FROM Lists WHERE lid=?"""
    cursor.execute(sql_fetch_query, (list_id,))
    list_name = cursor.fetchall()

    total_price = 0
    for list_items in lists_items:
        quantity = float(list_items[4])
        price = float(list_items[2])
        total_price += (price * quantity)
        total_price = round(total_price, 2)

    conn.close()

    return lists_items, list_name, total_price
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
    cursor.execute(sql_query, (data_model['lname'], data_model['ldate']),)
    conn.commit()
    conn.close()

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    sql_fetch_query = """SELECT * FROM lists"""
    cursor.execute(sql_fetch_query)
    lists = cursor.fetchall()

    return render_template('index.html', list_content=lists)


@app.route('/viewfood/<int:list_id>', methods=['GET'])
def view_food(list_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    sql_fetch_query = """SELECT * FROM items"""
    cursor.execute(sql_fetch_query)
    items = cursor.fetchall()

    return render_template('viewFood.html', items_content=items, list_id=list_id)


@app.route('/list/<int:list_id>', methods=['POST', 'GET'])
def disp_list(list_id):
    if request.method == 'POST':
        default_quantity = 1
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        food_id = request.form.get('iid')

        check_query = """SELECT COUNT(*) FROM ListsItems WHERE lid = ? AND iid = ?"""
        cursor.execute(check_query, (list_id, food_id),)
        count = cursor.fetchone()[0]

        pricetype_query = """SELECT ipricetype FROM Items WHERE iid = ?"""
        cursor.execute(pricetype_query, (food_id,))
        ipricetype = cursor.fetchone()[0]

        if ipricetype == 'kg':
            default_quantity = 0.1
        elif ipricetype == 'ea':
            default_quantity = 1

        if count == 0:
            sql_query = """INSERT INTO ListsItems (lid, iid, lquantity) VALUES (?, ?, ?)"""
            cursor.execute(sql_query, (list_id, food_id, default_quantity),)
        else:
            update_query = """UPDATE ListsItems SET lquantity = lquantity + ? WHERE lid = ? AND iid = ?"""
            cursor.execute(update_query, (default_quantity, list_id, food_id),)

        conn.commit()
        conn.close()

    lists_items, list_name, total_price = fetch_list_items(list_id)

    return render_template('dispList.html',
                           list_items_content=lists_items,
                           list_name=list_name,
                           total_price=total_price,
                           list_id=list_id)

@app.route('/updatequantity/<int:list_id>', methods=['POST'])
def update_quantity(list_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    item_id = request.form.get('iid')
    update_quantity = float(request.form.get('update'))

    sql_fetch_query = """SELECT lquantity FROM ListsItems WHERE iid=? AND lid=?"""
    cursor.execute(sql_fetch_query, (item_id, list_id),)
    quantity = cursor.fetchone()[0]

    updated_quantity = quantity + update_quantity

    if updated_quantity <= 0.001:
        delete_query = """DELETE FROM ListsItems WHERE iid=? AND lid=?"""
        cursor.execute(delete_query, (item_id, list_id),)
    else:
        update_query = """UPDATE ListsItems SET lquantity = ? WHERE iid=? AND lid=?"""
        cursor.execute(update_query, (updated_quantity, item_id, list_id),)

    conn.commit()
    conn.close()

    lists_items, list_name, total_price = fetch_list_items(list_id)

    return render_template('dispList.html',
                           list_items_content=lists_items,
                           list_name=list_name,
                           total_price=total_price,
                           list_id=list_id)

if __name__ == '__main__':
    app.run(debug=True)
