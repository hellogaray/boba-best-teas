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

@webapp.route('/cart')
def cart():
    return render_template("cart.html")

@webapp.route('/topping')
def topping():
    return render_template("topping.html")


@webapp.route('/register')
def register():
    db_connection = connect_to_database()
    print("Executing a query on the database using the credentials from db_credentials.py: customer table, select all columns.")
    query = "SELECT * from customers;"
    data = execute_query(db_connection, query)
    return render_template('register.html', data = data)

@webapp.route('/register', methods=['POST'])
def customer_data():
    db_connection = connect_to_database()
    print("Added new customer!")
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    phone_number = request.form['phone_number']
    query = 'INSERT INTO customers (first_name, last_name, phone_number) VALUES (%s,%s,%s)'
    data = (first_name, last_name, phone_number)
    execute_query(db_connection, query, data)
    return redirect(url_for('register'))

@webapp.route('/drink')
def drink():
    return render_template("drink.html")

@webapp.route('/order')
def order():
    return render_template("order.html")
