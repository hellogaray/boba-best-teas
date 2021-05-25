from flask import *
from flask import Flask, render_template
from flask import request, redirect
from db_connector.db_connector import connect_to_database, execute_query
webapp = Flask(__name__)

#Dashboard pages/links for Home, Drinks, Toppings, Customers, and Order.
@webapp.route('/')
def index():
    return render_template("index.html")

# ------ ORDERS ------
# SELECT for Order Page | Shows the Order Table.
@webapp.route('/order')
def order():
    db_connection = connect_to_database()
    # Prints message to console.
    print("Executing a query on the database using the credentials from db_credentials.py: orders table, select all columns.")  # Prints message to console.
    # Table showing all of the details of the orders. 
    query = "SELECT orders.order_id, orders.customer_id, customers.first_name, customers.last_name, drinks_instances.instance_id, base_drinks.drink_name, drinks_instances.size, IF( size = 0, base_drinks.small_cost, IF( size = 1, base_drinks.medium_cost, IF( size = 2, base_drinks.large_cost, NULL ) ) ) AS 'Size Cost' FROM orders LEFT JOIN drinks_instances ON orders.order_id = drinks_instances.order_id LEFT JOIN customers ON orders.customer_id = customers.customer_id LEFT JOIN base_drinks ON drinks_instances.drink_id = base_drinks.drink_id LEFT JOIN drinks_toppings ON drinks_instances.instance_id = drinks_toppings.instance_id ORDER BY order_id;"
    data = execute_query(db_connection, query)
    cust_query = 'SELECT customer_id, first_name, last_name FROM customers'
    cust_results = execute_query(db_connection, cust_query).fetchall()
    # Show the most recent Order as an option to add a new drink.
    order_id_query = "SELECT MAX(order_id) FROM orders;"
    order_id =  execute_query(db_connection, order_id_query)
    # Shows the list of ID (names) possible to be shown on the select.
    drink_name = 'SELECT drink_id, drink_name FROM base_drinks'
    dn_result = execute_query(db_connection, drink_name).fetchall()
    # Show the most recent Instance ID as an option to add a new toppings.
    instance_id_query = "SELECT MAX(instance_id) FROM drinks_instances;"
    instance_id =  execute_query(db_connection, instance_id_query)
    # Shows the list of Toppings (names) possible to be shown on the select.
    topping_name = 'SELECT topping_id, topping_name FROM toppings'
    tn_result = execute_query(db_connection, topping_name).fetchall()
    return render_template('order.html', data = data, customers = cust_results, order_id = order_id, drinks = dn_result, instance_id = instance_id, toppings = tn_result)

# CREATE for Order Page
@webapp.route('/order', methods=['POST', 'GET'])
def order_create():
    # All Post Requests
    if request.method == 'POST':  # Post Forms. 
        # Create new Order Form
        if 'customer_id' in request.form: # looks for customer_id in the form, then proceeds. 
            db_connection = connect_to_database()
            customer_id = request.form['customer_id']  # Searches for element named customer_id to use as customer_id in the query.
            query = 'INSERT INTO orders (customer_id) VALUES (%s)'  # Inserts previous elements into orders table.
            data = (customer_id)
            print("Added new order!") # Prints to console that a new order was added.
            execute_query(db_connection, query, data)
            return redirect(url_for('order'))
        # Add Drink to Order
        if 'order_id' and 'drink_id' and 'size' in request.form: # Looks for order_id, drink_id, and size in the form, then proceeds. 
            db_connection = connect_to_database()
            order_id = request.form['order_id']  # Searches for element named order_id to use as order_id in the query.
            drink_id = request.form['drink_id']  # Searches for element named drink_id to use as drink_id in the query.
            size = request.form['size']  # Searches for element named size to use as size in the query.
            query = 'INSERT INTO drinks_instances (order_id, drink_id, size) VALUES (%s,%s,%s)'  # Inserts previous elements into drinks_instances table.
            data = (order_id, drink_id, size)
            execute_query(db_connection, query, data)
            print("Added new drinks_instances!")# Prints to console that a new drink was added.
            return redirect(url_for('order'))
        # Add Toppings to Drinks
        if 'instance_id' and 'topping_id' in request.form:  # looks for instance_id and topping_id in the form, then proceeds. 
            db_connection = connect_to_database()
            instance_id = request.form['instance_id']  # Searches for element named instance_id to use as instance_id in the query.
            topping_id = request.form['topping_id']  # Searches for element named topping_id to use as topping_id in the query.
            query = 'INSERT INTO drinks_toppings (instance_id, topping_id) VALUES (%s,%s)'  # Inserts previous elements into drinks_toppings table.
            data = (instance_id, topping_id)
            execute_query(db_connection, query, data)
            print("Added new drinks_toppings!")  # Prints to console that a new drink was added.
            return redirect(url_for('order'))            
    # All Get Requests
    elif request.method == 'GET':  # Get Forms. 
        return redirect(url_for('order'))

# ------ DRINKS ------
# SELECT for Drinks Page | Shows the Drinks Table.
@webapp.route('/drink')
def drink():
    db_connection = connect_to_database()
    print("Executing a query on the database using the credentials from db_credentials.py: base_drinks table, select all columns.")  # Prints message to console.
    query = "SELECT * FROM base_drinks;"
    data = execute_query(db_connection, query)
    return render_template('drink.html', data = data)

# CREATE for Drinks Page
@webapp.route('/drink', methods=['POST', 'GET'])
def base_drinks_create():
    # All Post Requests
    if request.method == 'POST':  # Post Forms. 
        db_connection = connect_to_database()
        drink_name = request.form['drink_name']  # Searches for element named drink_name to use as drink_name in the query.
        small_cost = request.form['small_cost']  # Searches for element named small_cost to use as small_cost in the query.
        medium_cost = request.form['medium_cost']  # Searches for element named medium_cost to use as medium_cost in the query.
        large_cost = request.form['large_cost']  # Searches for element named large_cost to use as large_cost in the query.
        query = 'INSERT INTO base_drinks (drink_name, small_cost, medium_cost, large_cost) VALUES (%s,%s,%s,%s)'  # Inserts previous elements into base_drinks table.
        print("Added new drink!")  # Prints to console that a new drink was added.
        data = (drink_name, small_cost, medium_cost, large_cost)
        execute_query(db_connection, query, data)
        return redirect(url_for('drink'))
    # All Get Requests
    elif request.method == 'GET':  # Get Forms. 
        return redirect(url_for('order'))

# ------ TOPPINGS ------
# SELECT for Topping Page | Shows the Topping Table.
@webapp.route('/topping')
def topping():
    db_connection = connect_to_database()
    print("Executing a query on the database using the credentials from db_credentials.py: toppings table, select all columns.")  # Prints message to console.
    query = "SELECT * FROM toppings;"
    data = execute_query(db_connection, query)
    return render_template('topping.html', data = data)

# CREATE for Topping Page
@webapp.route('/topping', methods=['POST', 'GET'])
def topping_create():
    # All Post Requests
    if request.method == 'POST':  # Post Forms. 
        db_connection = connect_to_database()
        topping_name = request.form['topping_name']  # Searches for element named topping_name to use as topping_name in the query.
        total_cost = request.form['total_cost']  # Searches for element named total_cost to use as total_cost in the query.
        query = 'INSERT INTO toppings (topping_name, total_cost) VALUES (%s,%s)'  # Inserts previous elements into toppings table.
        data = (topping_name, total_cost)
        print("Added new topping!")  # Prints to console that a new topping was added.
        execute_query(db_connection, query, data)
        return redirect(url_for('topping'))
    # All Get Requests
    elif request.method == 'GET':  # Get Forms. 
        return redirect(url_for('order'))

# ------ CUSTOMERS ------
# SELECT for Customer Page | Shows the Customer Table.
@webapp.route('/customer')
def customer():
    db_connection = connect_to_database()
    print("Executing a query on the database using the credentials from db_credentials.py: customer table, select all columns.")  # Prints message to console.
    query = "SELECT * FROM customers;"
    data = execute_query(db_connection, query)
    return render_template('customer.html', data = data)

# CREATE for Customer Page
@webapp.route('/customer', methods=['POST', 'GET'])
def customer_create():
    # All Post Requests
    if request.method == 'POST':  # Post Forms. 
        db_connection = connect_to_database()
        first_name = request.form['first_name']  # Searches for element named first_name to use as first_name in the query.
        last_name = request.form['last_name']  # Searches for element named last_name to use as last_name in the query.
        phone_number = request.form['phone_number']  # Searches for element named phone_number to use as phone_number in the query.
        query = 'INSERT INTO customers (first_name, last_name, phone_number) VALUES (%s,%s,%s)'  # Inserts previous elements into customers table.
        data = (first_name, last_name, phone_number)
        print("Added new customer!") # Prints to console that a new customer was added.
        execute_query(db_connection, query, data)
        return redirect(url_for('customer'))
    # All Get Requests
    elif request.method == 'GET':  # Get Forms. 
        return redirect(url_for('order'))
