import sqlite3
import os
from flask import Flask, request, render_template

app = Flask(__name__)
db_path = os.path.join(app.root_path, 'instance', 'kiwibasketDB.sqlite')

# Function that creates database connection
def create_connection():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    return conn, cursor

# Function that handles receiving all the necessary information regarding the users list
def fetch_list_items(list_id):
    # Calls get_best_supermarket function that returns the
    # cheapest supermarket to shop at based on items in the users list
    supermarket = get_best_supermarket(list_id)
    conn, cursor = create_connection()

    # Fetches all the information about the items in the users list as well as the information
    # regarding the best supermarket
    sql_fetch_query = """SELECT iname, iquantity, price, ipricetype, lquantity, li.iid, s.sname, s.slocation, s.snumber
        FROM ListsItems li, Items i, SupermarketsItems si, Supermarkets s
        WHERE li.lid=? 
        AND li.iid=i.iid 
        AND li.iid=si.iid
        AND si.sid=?
        AND s.sid=?
        """

    cursor.execute(sql_fetch_query, (list_id, supermarket, supermarket,))
    lists_items = cursor.fetchall()

    # Fetches all the data from the current list
    sql_fetch_query = """SELECT * FROM Lists WHERE lid=?"""
    cursor.execute(sql_fetch_query, (list_id,))
    list_name = cursor.fetchall()

    # Calculates the total price based on all the items inside the users list
    total_price = 0
    for list_items in lists_items:
        quantity = float(list_items[4])
        price = float(list_items[2])
        total_price += (price * quantity)
        total_price = round(total_price, 2)

    conn.close()

    return lists_items, list_name, total_price

# Function that calculates the best supermarket to shop at based on the food inside the users list
def get_best_supermarket(list_id):
    conn, cursor = create_connection()

    # Fetches price of items at each supermarket based on items inside users list
    sql_fetch_query = """SELECT sid, price
                        FROM ListsItems li, Items i, SupermarketsItems si
                        WHERE li.lid=? 
                        AND li.iid=i.iid 
                        AND li.iid=si.iid
                        """

    cursor.execute(sql_fetch_query, (list_id,))
    supermarket_data = cursor.fetchall()

    # If user doesn't have any items inside their list else run price calculation
    if len(supermarket_data) == 0:
        return 1
    else:
        # Puts supermarket_data into a dictionary then calculates the total price for each supermarket
        supermarket_dict = {}

        for item in supermarket_data:
            sid = item[0]
            price = float(item[1])

            if sid in supermarket_dict:
                supermarket_dict[sid] += price
            else:
                supermarket_dict[sid] = price

        # Makes default value for lowest_total = to the first ([0]) value inside supermarket_dict
        values = list(supermarket_dict.values())
        lowest_total = values[0]
        supermarket = 1

        # Calculates which supermarket is the cheapest
        for key in supermarket_dict:
            item_total = supermarket_dict[key]

            if (item_total < lowest_total):
                lowest_total = item_total
                supermarket = key

        conn.close()

        return str(supermarket)

# Function that fetches all the lists that have been created
def fetch_lists():
    conn, cursor = create_connection()

    sql_fetch_query = """SELECT * FROM lists"""
    cursor.execute(sql_fetch_query)
    lists = cursor.fetchall()

    return lists

# Renders home page and display all the created lists by calling fetch_lists()
@app.route('/', methods=['GET'])
def main():
    lists = fetch_lists()

    return render_template('index.html', list_content=lists)

# When the user creates a new list insert it into the database
@app.route('/addlist', methods=['POST'])
def add_list():
    conn, cursor = create_connection()

    received_data_obj = request.form
    data_obj_to_save = dict(received_data_obj)

    data_model = {
        'lname': data_obj_to_save['lname'],
        'ldate': data_obj_to_save['ldate']
    }

    # Receives list name and date from html form and inserts it into datebase
    sql_query = """INSERT INTO lists (lname, ldate) VALUES (?, ?)"""
    cursor.execute(sql_query, (data_model['lname'], data_model['ldate'],))
    conn.commit()
    conn.close()

    # Fetches all the created lists then renders home page
    lists = fetch_lists()

    return render_template('index.html', list_content=lists)

# Displays all the food inside the items database
@app.route('/viewfood/<int:list_id>', methods=['GET'])
def view_food(list_id):
    conn, cursor = create_connection()

    # Fetches all the data inside items table
    sql_fetch_query = """SELECT * FROM items"""
    cursor.execute(sql_fetch_query)
    items = cursor.fetchall()

    return render_template('viewFood.html', items_content=items, list_id=list_id)

# Displays users list
# If method is POST then add food to list then display
@app.route('/list/<int:list_id>', methods=['POST', 'GET'])
def disp_list(list_id):
    if request.method == 'POST':
        default_quantity = 1

        conn, cursor = create_connection()
        food_id = request.form.get('iid')

        # Checks if item already exists inside the list
        check_query = """SELECT COUNT(*) FROM ListsItems WHERE lid = ? AND iid = ?"""
        cursor.execute(check_query, (list_id, food_id,))
        count = cursor.fetchone()[0]

        # Fetches the price type (kg or ea)
        pricetype_query = """SELECT ipricetype FROM Items WHERE iid = ?"""
        cursor.execute(pricetype_query, (food_id,))
        ipricetype = cursor.fetchone()[0]

        # Sets the default_quantity based on type of pricing (kg or ea)
        if ipricetype == 'kg':
            default_quantity = 0.1
        elif ipricetype == 'ea':
            default_quantity = 1

        # Adds food item to the list with default quantity
        # If item already exists in the list the just add default quantity to item
        if count == 0:
            sql_query = """INSERT INTO ListsItems (lid, iid, lquantity) VALUES (?, ?, ?)"""
            cursor.execute(sql_query, (list_id, food_id, default_quantity,))
        else:
            update_query = """UPDATE ListsItems SET lquantity = lquantity + ? WHERE lid = ? AND iid = ?"""
            cursor.execute(update_query, (default_quantity, list_id, food_id,))

        conn.commit()
        conn.close()

    # Fetches current list information then displays list
    lists_items, list_name, total_price = fetch_list_items(list_id)

    return render_template('dispList.html',
                           list_items_content=lists_items,
                           list_name=list_name,
                           total_price=total_price,
                           list_id=list_id)

# Updates the quantity of a food item
@app.route('/updatequantity/<int:list_id>', methods=['POST'])
def update_quantity(list_id):
    conn, cursor = create_connection()

    # Receives item id and update quantity
    item_id = request.form.get('iid')
    update_quantity = float(request.form.get('update'))

    # Fetches quantity from corresponding item
    sql_fetch_query = """SELECT lquantity FROM ListsItems WHERE iid=? AND lid=?"""
    cursor.execute(sql_fetch_query, (item_id, list_id,))
    quantity = cursor.fetchone()[0]

    # Sets new quantity
    updated_quantity = quantity + update_quantity

    # If quantity is 0 then delete item from list else update to new quantity
    if updated_quantity <= 0.001:
        delete_query = """DELETE FROM ListsItems WHERE iid=? AND lid=?"""
        cursor.execute(delete_query, (item_id, list_id,))
    else:
        update_query = """UPDATE ListsItems SET lquantity = ? WHERE iid=? AND lid=?"""
        cursor.execute(update_query, (updated_quantity, item_id, list_id,))

    conn.commit()
    conn.close()

    # Fetches current list information then displays list
    lists_items, list_name, total_price = fetch_list_items(list_id)

    return render_template('dispList.html',
                           list_items_content=lists_items,
                           list_name=list_name,
                           total_price=total_price,
                           list_id=list_id)

# Deletes a list from lists table
@app.route('/deletelist/<int:list_id>', methods=['POST'])
def delete_list(list_id):
    conn, cursor = create_connection()
    cursor.execute("PRAGMA foreign_keys = ON")

    # Delete list with corresponding list id
    delete_query = """DELETE FROM Lists WHERE lid=?"""
    cursor.execute(delete_query, (list_id,))

    conn.commit()
    conn.close()

    # Fetches all the created lists then renders home page
    lists = fetch_lists()

    return render_template('index.html', list_content=lists)

if __name__ == '__main__':
    app.run()