from flask import *
from flask import Flask, render_template
from flask import request, redirect
from db_connector.db_connector import connect_to_database, execute_query
webapp = Flask(__name__)

#Dashboard pages/links for Home, Drinks, Toppings, Customers, and Order.
@webapp.route('/')
def index():
    return render_template("index.html")

# ------------------------------ START OF ORDERS PAGE ------------------------------
@webapp.route('/order', methods=['POST', 'GET'])
def order():
    # All Post Requests
    # CREATE for Order Page
    if request.method == 'POST':  # Post Forms. 
        # Create new Order Form
        if 'customer_id' in request.form: # looks for customer_id in the form, then proceeds. 
            db_connection = connect_to_database()
            customer_id = request.form['customer_id']  # Searches for element named customer_id to use as customer_id in the query.
            query = 'INSERT INTO orders (customer_id) VALUES (%s)'  # Inserts previous elements into orders table.
            execute_query(db_connection, query, customer_id)
            return redirect(url_for('order'))

        # Add Drink to Order
        if 'order_id' and 'drink_id' and 'size' and 'instance_id' and 'topping_id' in request.form: # Looks for order_id, drink_id, and size in the form, then proceeds. 
            db_connection = connect_to_database()
            order_id = request.form['order_id']  # Searches for element named order_id to use as order_id in the query.
            drink_id = request.form['drink_id']  # Searches for element named drink_id to use as drink_id in the query.
            size = request.form['size']  # Searches for element named size to use as size in the query.
            query = 'INSERT INTO drinks_instance (order_id, drink_id, size) VALUES (%s,%s,%s)'  # Inserts previous elements into drinks_instance table.
            data = (order_id, drink_id, size)
            execute_query(db_connection, query, data)

            # Gets the Order Form working as a single form instead of three form. Using .fecthone() to obtain IDs as they are created.
            instance_id_query = "SELECT MAX(instance_id) FROM drinks_instance;"
            query_instance_id =  execute_query(db_connection, instance_id_query)  # Gets the most recent instance_id from db.
            instance_id = query_instance_id.fetchone()
            topping_id = request.form.getlist('topping_id')  # Searches for element named topping_id to use as topping_id in the query.
            for topping in topping_id:
                drink_topping_query = 'INSERT INTO drinks_topping (instance_id, topping_id) VALUES (%s, %s)'  # Inserts previous elements into drinks_topping table.
                dt_data = (str(instance_id[0]), topping)
                execute_query(db_connection, drink_topping_query, dt_data)
            return redirect(url_for('order'))
           
    # All Get Requests
    # SELECT for Order Page | Shows the Order Table.
    elif request.method == 'GET':  # Get Forms. 
            db_connection = connect_to_database()

            # Table showing all of the details of the orders. 
            query = "SELECT orders.order_id, CONCAT_WS( ' ', customers.first_name, customers.last_name ) AS Customer, drinks_instance.instance_id, CONCAT_WS( ' - ', drinks_instance.instance_id, base_drinks.drink_name, IF( size = 0, '(S)', IF( size = 1, '(M)', IF(size = 2, '(L)', NULL) ) ) ) AS Drink, IF( size = 0, base_drinks.small_cost, IF( size = 1, base_drinks.medium_cost, IF( size = 2, base_drinks.large_cost, NULL ) ) ) AS 'Size Cost', toppings.topping_id, toppings.topping_name, toppings.total_cost FROM orders LEFT JOIN drinks_instance ON orders.order_id = drinks_instance.order_id LEFT JOIN customers ON orders.customer_id = customers.customer_id LEFT JOIN base_drinks ON drinks_instance.drink_id = base_drinks.drink_id LEFT JOIN drinks_topping ON drinks_instance.instance_id = drinks_topping.instance_id LEFT JOIN toppings ON drinks_topping.topping_id = toppings.topping_id ORDER BY order_id, instance_id;"
            data = execute_query(db_connection, query)

            # Dropdown menu that shows all customers to create a new order.
            cust_query = 'SELECT customer_id, first_name, last_name FROM customers'
            cust_results = execute_query(db_connection, cust_query).fetchall()
            
            # Show the most recent Order as an option to add a new drink.
            order_id_query = "SELECT MAX(order_id) FROM orders;"
            order_id =  execute_query(db_connection, order_id_query)
            
            # Shows the list of ID (names) possible to be shown on the select.
            drink_name = 'SELECT drink_id, drink_name FROM base_drinks'
            dn_result = execute_query(db_connection, drink_name).fetchall()
            
            # Show the most recent Instance ID as an option to add a new toppings.
            instance_id_query = "SELECT MAX(instance_id) FROM drinks_instance;"
            instance_id =  execute_query(db_connection, instance_id_query)
            
            # Shows the list of Toppings (names) possible to be shown on the select.
            topping_name = 'SELECT topping_id, topping_name FROM toppings'
            tn_result = execute_query(db_connection, topping_name).fetchall()
            return render_template('order.html', data = data, customers = cust_results, order_id = order_id, drinks = dn_result, instance_id = instance_id, toppings = tn_result)


# DELETE Order table based on drink_id (first column).
@webapp.route('/order/<int:order_id>')
def delete_order(order_id):
    db_connection = connect_to_database()
    query = "DELETE FROM orders WHERE order_id = %s"
    data = (order_id,)
    execute_query(db_connection, query, data)
    return redirect(url_for('order'))


# DELETE Drink from Order table based on instance_id. 
@webapp.route('/instance/<int:instance_id>')
def delete_instance(instance_id):
    db_connection = connect_to_database()
    query = "DELETE FROM drinks_instance WHERE instance_id = %s"
    data = (instance_id,)
    execute_query(db_connection, query, data)
    return redirect(url_for('order'))


# DELETE Topping from Drinks_toppings based on topping_id and instance_id. 
@webapp.route('/instance/<int:instance_id>/topping/<int:topping_id>')
def delete_topping_from_instance(instance_id, topping_id):
    db_connection = connect_to_database()
    query = "DELETE FROM drinks_topping WHERE instance_id = %s AND topping_id = %s"
    data = (instance_id, topping_id,)
    execute_query(db_connection, query, data)
    return redirect(url_for('order'))

# ------------------------------ START OF DRINKS PAGE ------------------------------
@webapp.route('/drink', methods=['POST', 'GET'])
def drink():
    # All Post Requests
    # CREATE for Drinks Page
    if request.method == 'POST':  # Post Forms. 
        db_connection = connect_to_database()
        drink_name = request.form['drink_name']  # Searches for element named drink_name to use as drink_name in the query.
        small_cost = request.form['small_cost']  # Searches for element named small_cost to use as small_cost in the query.
        medium_cost = request.form['medium_cost']  # Searches for element named medium_cost to use as medium_cost in the query.
        large_cost = request.form['large_cost']  # Searches for element named large_cost to use as large_cost in the query.
        query = 'INSERT INTO base_drinks (drink_name, small_cost, medium_cost, large_cost) VALUES (%s,%s,%s,%s)'  # Inserts previous elements into base_drinks table.
        data = (drink_name, small_cost, medium_cost, large_cost)
        execute_query(db_connection, query, data)
        return redirect(url_for('drink')) 

    # All Get Requests
    # SELECT for Drinks Page | Shows the Drinks Table.
    elif request.method == 'GET':  # Get Forms. 
        db_connection = connect_to_database()
        query = "SELECT * FROM base_drinks;"
        data = execute_query(db_connection, query)
        return render_template('drink.html', data = data)


# DELETE from Drink table based on drink_id (first column).
@webapp.route('/drink/<int:drink_id>')
def delete_drink(drink_id):
    db_connection = connect_to_database()
    query = "DELETE FROM base_drinks WHERE drink_id = %s"
    data = (drink_id,)
    execute_query(db_connection, query, data)
    return redirect(url_for('drink'))


# ------------------------------ START OF UPDATE DRINKS PAGE ------------------------------
@webapp.route('/update_drink/<int:drink_id>', methods=['POST','GET'])
def update_drink(drink_id):
    db_connection = connect_to_database()
    # All Post Requests
    if request.method == 'GET':
        drinks_query = 'SELECT drink_id, drink_name, small_cost, medium_cost, large_cost from base_drinks WHERE drink_id = %s'  % (drink_id)
        drinks_results = execute_query(db_connection, drinks_query).fetchall()
        return render_template('update_drink.html', drinks_results = drinks_results)

    # All Get Requests
    # Updates a drink from base_drinks based on its drink_id.
    elif request.method == 'POST':
        drink_name = request.form['drink_name']  # Searches for element named drink_name to use as drink_name in the query.
        small_cost = request.form['small_cost']  # Searches for element named small_cost to use as small_cost in the query.
        medium_cost = request.form['medium_cost']  # Searches for element named medium_cost to use as medium_cost in the query.
        large_cost = request.form['large_cost']  # Searches for element named large_cost to use as large_cost in the query.
        drink_id = request.form['drink_id']  # Searches for element named drink_id to use as drink_id in the query.
        query = "UPDATE base_drinks SET drink_name = %s, small_cost = %s, medium_cost = %s, large_cost = %s WHERE drink_id = %s"
        data = (drink_name, small_cost, medium_cost, large_cost, drink_id)
        execute_query(db_connection, query, data)
        return redirect(url_for('drink'))


# ------------------------------ START OF TOPPINGS PAGE ------------------------------
@webapp.route('/topping', methods=['POST', 'GET'])
def topping():
    # All Post Requests
    # CREATE for Topping Page
    if request.method == 'POST':  # Post Forms. 
        db_connection = connect_to_database()
        topping_name = request.form['topping_name']  # Searches for element named topping_name to use as topping_name in the query.
        total_cost = request.form['total_cost']  # Searches for element named total_cost to use as total_cost in the query.
        query = 'INSERT INTO toppings (topping_name, total_cost) VALUES (%s,%s)'  # Inserts previous elements into toppings table.
        data = (topping_name, total_cost)
        execute_query(db_connection, query, data)
        return redirect(url_for('topping'))

    # All Get Requests
    # SELECT for Topping Page | Shows the Topping Table.
    elif request.method == 'GET':  # Get Forms. 
        db_connection = connect_to_database()
        query = "SELECT * FROM toppings;"
        data = execute_query(db_connection, query)
        return render_template('topping.html', data = data)


# DELETE from Topping table based on topping_id (first column).
@webapp.route('/topping/<int:topping_id>')
def delete_topping(topping_id):
    db_connection = connect_to_database()
    query = "DELETE FROM toppings WHERE topping_id = %s"
    data = (topping_id,)
    execute_query(db_connection, query, data)
    return redirect(url_for('topping'))


# ------------------------------ START OF UPDATE TOPPINGS PAGE ------------------------------
@webapp.route('/update_topping/<int:topping_id>', methods=['POST','GET'])
def update_topping(topping_id):
    db_connection = connect_to_database()
    # All Post Requests
    if request.method == 'GET':
        toppings_query = 'SELECT topping_id, topping_name, total_cost from toppings WHERE topping_id = %s'  % (topping_id)
        toppings_results = execute_query(db_connection, toppings_query).fetchall()
        return render_template('update_topping.html', toppings_results = toppings_results)

    # All Get Requests
    # Updates a topping from toppings based on its topping_id.
    elif request.method == 'POST':
        topping_name = request.form['topping_name']  # Searches for element named topping_name to use as topping_name in the query.
        total_cost = request.form['total_cost']  # Searches for element named total_cost to use as total_cost in the query.
        topping_id = request.form['topping_id']  # Searches for element named topping_id to use as topping_id in the query.
        query = "UPDATE toppings SET topping_name = %s, total_cost = %s WHERE topping_id = %s"
        data = (topping_name, total_cost, topping_id)
        execute_query(db_connection, query, data)
        return redirect(url_for('topping'))


# ------------------------------ START OF CUSTOMERS PAGE ------------------------------
@webapp.route('/customer', methods=['POST', 'GET'])
def customer():
    # All Post Requests
    # CREATE for Customer Page
    if request.method == 'POST':  # Post Forms. 
        if 'first_name' and 'last_name' and 'phone_number' in request.form: # looks for customer_id in the form, then proceeds. 
            db_connection = connect_to_database()
            first_name = request.form['first_name']  # Searches for element named first_name to use as first_name in the query.
            last_name = request.form['last_name']  # Searches for element named last_name to use as last_name in the query.
            phone_number = request.form['phone_number']  # Searches for element named phone_number to use as phone_number in the query.
            query = 'INSERT INTO customers (first_name, last_name, phone_number) VALUES (%s,%s,%s)'  # Inserts previous elements into customers table.
            data = (first_name, last_name, phone_number)
            execute_query(db_connection, query, data)
            return redirect(url_for('customer'))    

    # All Get Requests
    # SELECT for Customer Page | Shows the Customer Table.
    elif request.method == 'GET':  # Get Forms. 
        db_connection = connect_to_database()
        query = "SELECT * FROM customers;"
        data = execute_query(db_connection, query)
        return render_template('customer.html', data = data)


# DELETE from Customer table based on customer_id (first column).
@webapp.route('/customer/<int:customer_id>')
def delete_customer(customer_id):
    db_connection = connect_to_database()
    query = "DELETE FROM customers WHERE customer_id = %s"
    data = (customer_id,)
    execute_query(db_connection, query, data)
    return redirect(url_for('customer'))


# ------------------------------ START OF UPDATE CUSTOMERS PAGE ------------------------------
@webapp.route('/update_customer/<int:customer_id>', methods=['POST','GET'])
def update_customer(customer_id):
    db_connection = connect_to_database()
    # All Post Requests
    if request.method == 'GET':
        customer_query = 'SELECT customer_id, first_name, last_name, phone_number from customers WHERE customer_id = %s'  % (customer_id)
        customer_results = execute_query(db_connection, customer_query).fetchall()
        return render_template('update_customer.html', customer_results = customer_results)

    # All Get Requests
    # Updates a customer from customers based on its customer_id.
    elif request.method == 'POST':
        first_name = request.form['first_name']  # Searches for element named first_name to use as first_name in the query.
        last_name = request.form['last_name']  # Searches for element named last_name to use as last_name in the query.
        phone_number = request.form['phone_number']  # Searches for element named phone_number to use as phone_number in the query.
        customer_id = request.form['customer_id']  # Searches for element named customer_id to use as customer_id in the query.
        query = "UPDATE customers SET first_name = %s, last_name = %s, phone_number = %s WHERE customer_id = %s"
        data = (first_name, last_name, phone_number, customer_id)
        execute_query(db_connection, query, data)
        return redirect(url_for('customer'))