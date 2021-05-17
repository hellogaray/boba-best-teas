from flask import *
from flask import Flask, render_template
from flask import request, redirect
from db_connector.db_connector import connect_to_database, execute_query
#create the web application
webapp = Flask(__name__)

#Dashboard pages/links for Home, Drinks, Toppings, Customers, Order, and Cart.
@webapp.route('/')
def index():
    return render_template("index.html")


# ------ ORDERS ------
@webapp.route('/order')
def order():
    db_connection = connect_to_database()
    print("Executing a query on the database using the credentials from db_credentials.py: orders table, select all columns.")
    query = "SELECT * FROM orders;"
    data = execute_query(db_connection, query)
    return render_template('order.html', data = data)


# ------ DRINKS ------
# SELECT for Drinks Page
@webapp.route('/drink')
def drink():
    db_connection = connect_to_database()
    print("Executing a query on the database using the credentials from db_credentials.py: base_drinks table, select all columns.")
    query = "SELECT * FROM base_drinks;"
    data = execute_query(db_connection, query)
    return render_template('drink.html', data = data)

# CREATE for Drinks Page
@webapp.route('/drink', methods=['POST'])
def base_drinks_create():
    db_connection = connect_to_database()
    print("Added new drink!")
    drink_name = request.form['drink_name']
    small_cost = request.form['small_cost']
    medium_cost = request.form['medium_cost']
    large_cost = request.form['large_cost']
    query = 'INSERT INTO base_drinks (drink_name, small_cost, medium_cost, large_cost) VALUES (%s,%s,%s,%s)'
    data = (drink_name, small_cost, medium_cost, large_cost)
    execute_query(db_connection, query, data)
    return redirect(url_for('drink'))

# ------ TOPPINGS ------
# SELECT for Topping Page
@webapp.route('/topping')
def topping():
    db_connection = connect_to_database()
    print("Executing a query on the database using the credentials from db_credentials.py: toppings table, select all columns.")
    query = "SELECT * FROM toppings;"
    data = execute_query(db_connection, query)
    return render_template('topping.html', data = data)

# CREATE for Topping Page
@webapp.route('/topping', methods=['POST'])
def topping_create():
    db_connection = connect_to_database()
    print("Added new topping!")
    topping_name = request.form['topping_name']
    total_cost = request.form['total_cost']
    query = 'INSERT INTO toppings (topping_name, total_cost) VALUES (%s,%s)'
    data = (topping_name, total_cost)
    execute_query(db_connection, query, data)
    return redirect(url_for('topping'))

# UPDATE for Topping Page
# DELETE for Topping Page

# ------ CUSTOMERS ------
# SELECT for Customer Page
@webapp.route('/customer')
def register():
    db_connection = connect_to_database()
    print("Executing a query on the database using the credentials from db_credentials.py: customer table, select all columns.")
    query = "SELECT * FROM customers;"
    data = execute_query(db_connection, query)
    return render_template('customer.html', data = data)

# CREATE for Customer Page
@webapp.route('/customer', methods=['POST'])
def customer_create():
    db_connection = connect_to_database()
    print("Added new customer!")
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    phone_number = request.form['phone_number']
    query = 'INSERT INTO customers (first_name, last_name, phone_number) VALUES (%s,%s,%s)'
    data = (first_name, last_name, phone_number)
    execute_query(db_connection, query, data)
    return redirect(url_for('customer'))

# UPDATE for Customer Page
# DELETE for Customer Page
