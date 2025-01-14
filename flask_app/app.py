# Project Group 136
# Michelle Cheng


# THIS PROJECT USES CODE BASED FROM THE CS340 FLASK GUIDE STARTER APP
# https://github.com/osu-cs340-ecampus/flask-starter-app
# DATE: 12/04/2022


# -----------------------------------------------------------------------------
from flask import Flask, render_template, redirect, request
import os
import pymysql
from dotenv import load_dotenv, find_dotenv




# Configuration
app = Flask(__name__)

load_dotenv(find_dotenv())
host = os.environ.get("340DBHOST")
user = os.environ.get("340DBUSER")
passwd = os.environ.get("340DBPW")
db = os.environ.get("340DB")
port = os.environ.get("MyPort")

app.config["MYSQL_HOST"] = os.environ.get("340DBHOST")
app.config["MYSQL_USER"] = os.environ.get("340DBUSER")
app.config["MYSQL_PASSWORD"] = os.environ.get("340DBPW")
app.config["MYSQL_DB"] = os.environ.get("340DB")
app.config["MYSQL_PORT"] = port
app.config["MYSQL_CURSORCLASS"] = "DictCursor" # To get results as a dictionary

def connect_to_db(host = host, user = user, passwd = passwd, db = db, ssl_mode = 2):
    timeout = 10
    connection = pymysql.connect(
        charset="utf8mb4",
        connect_timeout=timeout,
        cursorclass=pymysql.cursors.DictCursor,
        db=db,
        host=host,
        password=passwd,
        read_timeout=timeout,
        port= port,
        user=user,
        write_timeout=timeout,
    )
    return connection


db_connection = connect_to_db()
# -------------------------------------------------------------------------------


# Routes  -----------------------------------------------------------------------

# ------ HOME PAGE --------------------------------------------------------------
@app.route('/')
def root():
    return render_template("main.j2")


# ------ CUSTOMERS -----------------------------------------------------------
@app.route('/customers', methods=["POST", "GET"])
def customers():
    if request.method == "GET":
        query = "SELECT customer_id, first_name, last_name, email, birthdate FROM Customers"
        cur = db_connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        return render_template("customers.j2", Customers=data)

    if request.method == "POST":
        # executes when user presses add button
        if request.form.get("add_customer"):
            first_name = request.form["insert_first_name_field"]
            last_name = request.form["insert_last_name_field"]
            email = request.form["insert_email_field"]
            birthdate = request.form["insert_birthdate_field"]

            query = "INSERT INTO Customers (first_name, last_name, email, birthdate) VALUES (%s, %s,%s,%s)"
            cur = db_connection.cursor()
            cur.execute(query, (first_name, last_name, email, birthdate))
            db_connection.commit()

            # return to page
            return redirect("/customers")


@app.route("/delete_customer/<int:customer_id>")
def delete_customer(customer_id):
    query = "DELETE FROM Customers WHERE customer_id = %s"
    cur = db_connection.cursor()
    cur.execute(query, (customer_id,))
    db_connection.commit()

    # return to page
    return redirect("/customers")


@app.route("/edit_customer/<int:customer_id>", methods=["POST", "GET"])
def edit_customer(customer_id):
    if request.method == "GET":
        # grab info of passed id
        query = "SELECT * FROM Customers WHERE customer_id = %s" % (customer_id)
        cur = db_connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # render edit page
        return render_template("edit_customer.j2", Customers=data)

    if request.method == "POST":
        # executes when user presses edit button
        if request.form.get("edit_customer"):
            customer_id = request.form["customer_id"]
            first_name = request.form["first_name"]
            last_name = request.form["last_name"]
            email = request.form["email"]
            birthdate = request.form["birthdate"]

            query = "UPDATE Customers SET Customers.first_name = %s, Customers.last_name = %s, Customers.email = %s, Customers.birthdate = %s WHERE Customers.customer_id = %s"
            cur = db_connection.cursor()
            cur.execute(query, (first_name, last_name, email, birthdate, customer_id))
            db_connection.commit()

        # redirect back to customers page
        return redirect("/customers")


# customer SEARCH
@app.route("/customers/search_last_name", methods=["POST"])
def search_last_name():
    last_name = request.form['search']
    query = "SELECT customer_id, first_name, last_name, email, birthdate FROM Customers WHERE last_name LIKE '%s'" % (last_name)
    cur = db_connection.cursor()
    cur.execute(query)
    res = cur.fetchall()

    return render_template('customers.j2', Customers=res)

# ------ ITEMS ----------------------------------------------------------------
@app.route("/items", methods=["POST", "GET"])
def items():
    if request.method == "GET":
        query = "SELECT item_id, item_name, item_price FROM Items"
        cur = db_connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        return render_template("items.j2", Items=data)

    if request.method == "POST":
        # executes if user presses Add Item button
        if request.form.get("add_item"):
            item_name = request.form["item_name"]
            item_price = request.form["item_price"]

            query = "INSERT INTO Items (item_name, item_price) VALUES (%s, %s)"
            cur = db_connection.cursor()
            cur.execute(query, (item_name, item_price))
            db_connection.commit()

            # redirect back to items page
            return redirect("/items")


@app.route("/delete_item/<int:item_id>")
def delete_item(item_id):
    query = "DELETE FROM Items WHERE item_id = %s"
    cur = db_connection.cursor()
    cur.execute(query, (item_id,))
    db_connection.commit()

    # redirect back to items page
    return redirect("/items")


@app.route("/edit_item/<int:item_id>", methods=["POST", "GET"])
def edit_item(item_id):
    if request.method == "GET":
        # grab info of passed id
        query = "SELECT * FROM Items WHERE item_id = %s" % (item_id)
        cur = db_connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # render edit_people page
        return render_template("edit_item.j2", Items=data)

    if request.method == "POST":
        # executes when user presses edit button
        if request.form.get("edit_item"):
            item_id = request.form["item_id"]
            item_name = request.form["item_name"]
            item_price = request.form["item_price"]

            query = "UPDATE Items SET Items.item_name = %s, Items.item_price= %s WHERE Items.item_id = %s"
            cur = db_connection.cursor()
            cur.execute(query, (item_name, item_price, item_id))
            db_connection.commit()

        # redirect back to items page
        return redirect("/items")
        


# ------ LOCATIONS -------------------------------------------------------------
@app.route("/locations", methods=["POST", "GET"])
def locations():
    if request.method == "GET":
        query = "SELECT location_id, location_name FROM Locations ORDER BY location_id"
        cur = db_connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        return render_template("locations.j2", Locations=data)

    if request.method == "POST":
        # executes when user presses add button
        if request.form.get("add_location"):
            location_name = request.form["location_name"]

            query = "INSERT INTO Locations (location_name) VALUES (%s)"
            cur = db_connection.cursor()
            cur.execute(query, (location_name,))
            db_connection.commit()

            # return to page
            return redirect("/locations")


@app.route("/delete_location/<int:location_id>")
def delete_location(location_id):
    query = "DELETE FROM Locations WHERE location_id = %s"
    cur = db_connection.cursor()
    cur.execute(query, (location_id,))
    db_connection.commit()

    # return to page
    return redirect("/locations")


@app.route("/edit_location/<int:location_id>", methods=["POST", "GET"])
def edit_location(location_id):
    # grabs info of passed id
    if request.method == "GET":
        query = "SELECT * FROM Locations WHERE location_id = %s" % (location_id)
        cur = db_connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        return render_template("edit_location.j2", Locations=data)

    if request.method == "POST":
        # executes when user clicks edit button
        if request.form.get("edit_location"):
            location_id = request.form["location_id"]
            location_name = request.form["location_name"]

            query = "UPDATE Locations SET Locations.location_name = %s WHERE Locations.location_id = %s"
            cur = db_connection.cursor()
            cur.execute(query, (location_name, location_id))
            db_connection.commit()

        # return to page
        return redirect("/locations")



# ------ ORDERS -------------------------------------------------------------
@app.route("/orders", methods=["POST", "GET"])
def orders():
    # display table and dropdowns
    if request.method == "GET":

        query = "SELECT order_id, order_date, Locations.location_name, CONCAT(Customers.first_name, ' ', Customers.last_name), order_total FROM Orders LEFT JOIN Customers ON Orders.customer_id = Customers.customer_id INNER JOIN Locations ON Orders.location_id = Locations.location_id ORDER BY order_id"
        cur = db_connection.cursor()
        cur.execute(query)
        orders = cur.fetchall()

        # display drop down of Locations
        query = "SELECT * FROM Locations"
        cur = db_connection.cursor()
        cur.execute(query)
        locations = cur.fetchall()

        # display drop down of Customers
        query = "SELECT * FROM Customers"
        cur = db_connection.cursor()
        cur.execute(query)
        customers = cur.fetchall()


        return render_template("orders.j2", Orders=orders, Locations=locations, Customers=customers)
    
    # add order
    if request.method == "POST":
        if request.form.get("add_order"):
            
            location_id = request.form["location_id"]
            customer_id = request.form["customer_id"]

            # if customer_id is NULL
            if customer_id == "":
                query = "INSERT INTO Orders (order_date, location_id) VALUES (DATE(NOW()), %s)"
                cur = db_connection.cursor()
                cur.execute(query, (location_id,))
                db_connection.commit()

            else:
                query = "INSERT INTO Orders (order_date, location_id, customer_id) VALUES (DATE(NOW()), %s, %s)"
                cur = db_connection.cursor()
                cur.execute(query, (location_id, customer_id))
                db_connection.commit()

            # return to page
            return redirect("/orders")


@app.route("/delete_order/<int:order_id>")
def delete_order(order_id):
    query = "DELETE FROM Orders WHERE order_id = %s"
    cur = db_connection.cursor()
    cur.execute(query, (order_id,))
    db_connection.commit()

    # return to page
    return redirect("/orders")


@app.route("/edit_order/<int:order_id>", methods=["POST", "GET"])
def edit_order(order_id):
    if request.method == "GET":
        # grab info of passed id
        query = "SELECT order_id, order_date, Locations.location_name, CONCAT(Customers.first_name, ' ', Customers.last_name), order_total FROM Orders LEFT JOIN Customers ON Orders.customer_id = Customers.customer_id INNER JOIN Locations ON Orders.location_id = Locations.location_id WHERE order_id = %s" % (order_id)
        cur = db_connection.cursor()
        cur.execute(query)
        orders = cur.fetchall()

        # display drop down of Locations
        query = "SELECT * FROM Locations"
        cur = db_connection.cursor()
        cur.execute(query)
        locations = cur.fetchall()

        # display drop down of Customers
        query = "SELECT * FROM Customers"
        cur = db_connection.cursor()
        cur.execute(query)
        customers = cur.fetchall()

        return render_template("edit_order.j2", Orders=orders, Locations=locations, Customers=customers)

    if request.method == "POST":
        # executes when user presses edit button
        if request.form.get("edit_order"):
            order_id = request.form["order_id"]
            location_id = request.form["location_id"]
            customer_id = request.form["customer_id"]

            # if customer_id is NULL
            if customer_id == "":
                query = "UPDATE Orders SET Orders.location_id = %s, Orders.customer_id = NULL WHERE Orders.order_id = %s"
                cur = db_connection.cursor()
                cur.execute(query, (location_id, order_id))
                db_connection.commit()

            else:
                query = "UPDATE Orders SET Orders.location_id = %s, Orders.customer_id = %s WHERE Orders.order_id = %s"
                cur = db_connection.cursor()
                cur.execute(query, (location_id, customer_id, order_id))
                db_connection.commit()

        # redirect back to orders page
        return redirect("/orders")



# ------ ORDER DETAILS --------------------------------------------------------
@app.route("/order_details", methods=["POST", "GET"])
def order_details():
    if request.method == "GET":
        query = "SELECT order_detail_id, Orders.order_id, Items.item_name, item_quantity, unit_cost, item_total FROM Order_Details LEFT JOIN Orders ON Order_Details.order_id = Orders.order_id LEFT JOIN Items ON Order_Details.item_id = Items.item_id ORDER BY order_detail_id"
        cur = db_connection.cursor()
        cur.execute(query)
        order_details = cur.fetchall()

        # display drop down of Orders
        query = "SELECT * FROM Orders"
        cur = db_connection.cursor()
        cur.execute(query)
        orders = cur.fetchall()

        # display drop down of Items
        query = "SELECT * FROM Items"
        cur = db_connection.cursor()
        cur.execute(query)
        items = cur.fetchall()

        return render_template("order_details.j2", Order_Details=order_details, Orders=orders, Items=items)

    # add order_detail
    if request.method == "POST":
        if request.form.get("add_order_detail"):
            
            order_id = request.form["order_id"]
            item_id = request.form["item_id"]
            item_quantity = request.form["item_quantity"]

            query = "INSERT INTO Order_Details (order_id, item_id, item_quantity) VALUES (%s, %s, %s)"
            cur = db_connection.cursor()
            cur.execute(query, (order_id, item_id, item_quantity))
            db_connection.commit()

            # update unit cost
            query = "UPDATE Order_Details SET unit_cost = (SELECT item_price FROM Items INNER JOIN Order_Details ON Items.item_id = Order_Details.item_id WHERE order_detail_id = (SELECT MAX(order_detail_id) FROM Order_Details)) WHERE order_detail_id = (SELECT MAX(order_detail_id) FROM Order_Details)"
            cur = db_connection.cursor()
            cur.execute(query,)
            db_connection.commit()

            #update item total
            query = "UPDATE Order_Details SET item_total = (SELECT unit_cost * item_quantity as item_total FROM Order_Details WHERE order_detail_id = (SELECT MAX(order_detail_id) FROM Order_Details) ) WHERE order_detail_id = (SELECT MAX(order_detail_id) FROM Order_Details)"
            cur = db_connection.cursor()
            cur.execute(query,)
            db_connection.commit()            

            # update order total on Orders page for corresponding order id
            query = "UPDATE Orders SET order_total = (SELECT SUM(Order_Details.item_total) FROM Order_Details WHERE order_id = %s ) WHERE order_id = %s"
            cur = db_connection.cursor()
            cur.execute(query, (order_id, order_id))
            db_connection.commit()       
            
            # return to page
            return redirect("/order_details")


@app.route("/delete_order_detail/<int:order_detail_id>")
def delete_order_detail(order_detail_id):

    # save order id
    query = "SELECT Order_Details.order_id FROM Order_Details INNER JOIN Orders ON Order_Details.order_id = Orders.order_id WHERE Order_Details.order_detail_id = %s"
    cur = db_connection.cursor()
    cur.execute(query, (order_detail_id, ))
    order_id = cur.fetchone()['order_id']


    # delete row
    query = "DELETE FROM Order_Details WHERE order_detail_id = %s"
    cur = db_connection.cursor()
    cur.execute(query, (order_detail_id,))
    db_connection.commit()


    # save the sum to check
    query = "SELECT SUM(Order_Details.item_total) AS 'sum' FROM Order_Details WHERE order_id = %s"
    cur = db_connection.cursor()
    cur.execute(query, (order_id,))
    sum = cur.fetchone()['sum']

    #update total to 0.00 if sum is NULL
    if not sum:
        query = "UPDATE Orders SET order_total = 0.00 WHERE order_id = %s"
        cur = db_connection.cursor()
        cur.execute(query, (order_id,))
        db_connection.commit()     
    # else update total normally
    else:
        query = "UPDATE Orders SET order_total = (SELECT SUM(Order_Details.item_total) FROM Order_Details WHERE order_id = %s ) WHERE order_id = %s"
        cur = db_connection.cursor()
        cur.execute(query, (order_id, order_id))
        db_connection.commit()     
    
    # return to page
    return redirect("/order_details")


@app.route("/edit_order_detail/<int:order_detail_id>", methods=["POST", "GET"])
def edit_order_detail(order_detail_id):
    if request.method == "GET":
        # grab info of passed id
        query = "SELECT order_detail_id, order_id, Items.item_name, item_quantity, unit_cost, item_total FROM Order_Details INNER JOIN Items ON Order_Details.item_id = Items.item_id WHERE Order_Details.order_detail_id = %s" % (order_detail_id)
        cur = db_connection.cursor()
        cur.execute(query)
        order_details = cur.fetchall()

        return render_template("edit_order_detail.j2", Order_Details = order_details)

    if request.method == "POST":
        # executes when user presses edit button
        if request.form.get("edit_order_detail"):
            order_detail_id = request.form["order_detail_id"]
            item_quantity = request.form["item_quantity"]
            unit_cost = request.form["unit_cost"]

            # save order id
            query = "SELECT Order_Details.order_id FROM Order_Details INNER JOIN Orders ON Order_Details.order_id = Orders.order_id WHERE Order_Details.order_detail_id = %s"
            cur = db_connection.cursor()
            cur.execute(query, (order_detail_id, ))
            order_id = cur.fetchone()['order_id']

            # update order detail row
            query = "UPDATE Order_Details SET Order_Details.item_quantity = %s, Order_Details.unit_cost = %s WHERE Order_Details.order_detail_id = %s"
            cur = db_connection.cursor()
            cur.execute(query, (item_quantity, unit_cost, order_detail_id))
            db_connection.commit()

            # update item total column
            query = "UPDATE Order_Details SET item_total = (SELECT unit_cost * item_quantity as item_total FROM Order_Details WHERE order_detail_id = %s ) WHERE order_detail_id = %s"
            cur = db_connection.cursor()
            cur.execute(query, (order_detail_id, order_detail_id))
            db_connection.commit()

            #update order total column in Orders page for correspoding order id
            query = "UPDATE Orders SET order_total = (SELECT SUM(Order_Details.item_total) FROM Order_Details WHERE order_id = %s ) WHERE order_id = %s"
            cur = db_connection.cursor()
            cur.execute(query, (order_id, order_id))
            db_connection.commit()      

        # return to page
        return redirect("/order_details")




# Listener ----------------------------------------------------------------------
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 3000))
    app.run(port=port, debug=True)
