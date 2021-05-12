/* **********************************
Project Step 4 Draft Version
GROUP 100 | Boba Best-Teas | 
Garrick Chan & Leonel Garay
********************************** */

/* Basic queries that select all columns from one of the tables:
Select all from customers, orders, base_drinks, drinks_instances, and toppings.  */
SELECT * FROM customers;
SELECT * FROM orders;
SELECT * FROM base_drinks;
SELECT * FROM drinks_instances;
SELECT * FROM toppings;

/* Basic queries that insert needed values to one of the tables:
Insert all needd values to customers, orders, base_drinks, drinks_instances, and toppings.  */
INSERT INTO customers (first_name, last_name, phone_number) VALUES (first_name, last_name, phone_number);
INSERT INTO orders (customer_id) VALUES (customer_id);
INSERT INTO base_drinks (drink_name, small_cost, medium_cost, large_cost) VALUES (drink_name, small_cost, medium_cost, large_cost);
INSERT INTO drinks_instances (order_id, drink_id, size) VALUES (order_id, drink_id, size);
INSERT INTO toppings (topping_name, total_cost) VALUES (topping_name, total_cost);

/* Basic queries that delete from one of the tables:
Delete ID from customers, orders, base_drinks, drinks_instances, and toppings.  */
DELETE FROM customers WHERE customer_id = customer_id;
DELETE FROM orders WHERE order_id = order_id;
DELETE FROM base_drinks WHERE drink_id = drink_id;
DELETE FROM drinks_instances WHERE instance_id = instance_id;
DELETE FROM toppings WHERE topping_id = topping_id;

/* Basic queries that update values from one of the tables:
Update values from customers, orders, base_drinks, drinks_instances, and toppings.  */
UPDATE customers SET first_name = first_name, last_name = last_name, phone_number = phone_number WHERE drink_id = drink_id;
UPDATE orders SET customer_id = customer_id WHERE order_id = order_id;
UPDATE base_drinks SET drink_name = drink_name, small_cost = small_cost, medium_cost = medium_cost, large_cost = large_cost WHERE drink_id = drink_id;
UPDATE drinks_instances SET size = size WHERE instance_id = instance_id;
UPDATE toppings SET topping_name = topping_name, total_cost = total_cost WHERE topping_id = topping_id;