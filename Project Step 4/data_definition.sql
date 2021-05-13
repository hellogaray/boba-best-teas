/* **********************************
Project Step 4 Draft Version
GROUP 100 | Boba Best-Teas |
Garrick Chan & Leonel Garay
********************************** */

/* WARNING:
Running this file will refresh the database. */
DROP
  TABLE IF EXISTS customers;
DROP
  TABLE IF EXISTS orders;
DROP
  TABLE IF EXISTS base_drinks;
DROP
  TABLE IF EXISTS drinks_instances;
DROP
  TABLE IF EXISTS toppings;
DROP
  TABLE IF EXISTS drinks_toppings;

/* TABLE customers:
This table keeps track of the customers. */
CREATE TABLE customers (
  customer_id INT(10) NOT NULL AUTO_INCREMENT UNIQUE,
  first_name VARCHAR(255) NOT NULL,
  last_name VARCHAR(255) NOT NULL,
  phone_number VARCHAR(25) UNIQUE,
  PRIMARY KEY(customer_id)
);

/* Example Data for Table customers */
INSERT INTO customers (first_name, last_name, phone_number)
VALUES
  ('Tony', 'Stark', '555-555-0000'),
  ('Peter', 'Parker', '555-555-0001'),
  ('Stephen', 'Strage', '555-555-0002'),
  ('Steve', 'Rogers', '555-555-0003'),
  ('Brunce', 'Banner', '555-555-0004');

/* TABLE orders:
Tracks the customers to which the order belongs. */
CREATE TABLE orders (
  order_id INT(10) NOT NULL AUTO_INCREMENT UNIQUE,
  customer_id INT(10) NOT NULL,
  PRIMARY KEY(order_id),
  FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE ON UPDATE CASCADE
);

/* Example Data for Table orders */
INSERT INTO orders (customer_id)
VALUES
  -- Tony Stark --
  (1),
  -- Tony Stark --
  (1),
  -- Peter Parker --
  (2),
  -- Stephen Strage --
  (3),
  -- Brunce Banner --
  (5);

/* TABLE base_drinks:
Tracks drinks on the menu and the cost of each based on the size. */
CREATE TABLE base_drinks (
  drink_id INT(10) NOT NULL AUTO_INCREMENT UNIQUE,
  drink_name VARCHAR(255) NOT NULL,
  small_cost DECIMAL(4, 2) NOT NULL,
  medium_cost DECIMAL(4, 2) NOT NULL,
  large_cost DECIMAL(4, 2) NOT NULL,
  PRIMARY KEY (drink_id)
);

/* Example Data for Table orders */
INSERT INTO base_drinks (drink_name, small_cost, medium_cost, large_cost)
VALUES
  ('Boba Tealicious', '4.50', '6.50', '8.00'),
  ('Double Bubble', '4.50', '6.50', '8.00' ),
  ('So ThirstTea', '5.00', '7.50', '8.00'),
  ('Best Boobas', '4.50', '6.50', '8.00'),
  ('Boba is Your Uncle', '7.00', '8.50','10.00');

/* TABLE drinks_instances:
When a customer orders a particular drink from base_drinks a drink instance is created. */
CREATE TABLE drinks_instances (
  instance_id INT(10) NOT NULL AUTO_INCREMENT UNIQUE,
  order_id INT(10) NOT NULL,
  drink_id INT(10) NOT NULL,
  size INT(1) NOT NULL,
  PRIMARY KEY (instance_id),
  FOREIGN KEY (order_id) REFERENCES orders (order_id) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (drink_id) REFERENCES base_drinks (drink_id) ON DELETE CASCADE ON UPDATE CASCADE
);

/* Example Data for Table orders */
INSERT INTO drinks_instances (order_id, drink_id, size)
VALUES
  -- Order #1: Boba Tealicious, Medium --
  (1, 1, 1),
  -- Order #1: Boba Tealicious, Large --
  (1, 1, 2),
  -- Order #2: So ThirstTea, Small --
  (2, 3, 0),
  -- Order #2: Boba is Your Uncle, Small --
  (2, 5, 0),
  -- Order #3: Double Bubble, Large --
  (3, 2, 2);

/* TABLE toppings:
Information for toppings that can be added to drinks_instances. */
CREATE TABLE toppings (
  topping_id INT(10) NOT NULL AUTO_INCREMENT UNIQUE,
  topping_name VARCHAR(255) NOT NULL,
  total_cost DECIMAL(4, 2) NOT NULL,
  PRIMARY KEY (topping_id)
);

/* Example Data for Table toppings */
INSERT INTO toppings (topping_name, total_cost)
VALUES
  ('Black Boba', 0.25),
  ('Popping Boba', 0.50),
  ('Coconut Jelly', 0.40),
  ('Aloe', 0.60),
  ('Red Bean', 0.50);

/* TABLE drinks_toppings:
Tracks what toppings are to be added to a particular ordered drink. */
CREATE TABLE drinks_toppings (
  instance_id INT(10) NOT NULL,
  topping_id INT(10) NOT NULL,
  PRIMARY KEY (instance_id, topping_id)
  FOREIGN KEY (instance_id) REFERENCES drinks_instances (instance_id) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (topping_id) REFERENCES toppings (topping_id) ON DELETE CASCADE ON UPDATE CASCADE
);

/* Example Data for Table drinks_toppings */
INSERT INTO toppings (instance_id, topping_id)
VALUES
  -- Add Black Boba to Boba Tealicious
  (1, 1),
  -- Add Popping Boba to Boba Tealicious
  (1, 2),
  -- Add Coconut Jelly to So ThirstTea
  (3, 3),
  -- Add Aloe to Boba is Your Uncle
  (4, 4),
  -- Add Red Bean to Boba is Your Uncle
  (4, 5);
