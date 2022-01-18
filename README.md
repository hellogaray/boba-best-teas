
# Boba Best-Teas
> Introduction to Database's Project: Oregon State University - CS 340<p>
> A boba store order management system and database, built for the web using mainly Python and SQL.



## 💻 Authors

######  Leonel Garay
[![github](https://img.shields.io/badge/github-FFF?style=for-the-badge&logo=github&logoColor=black)](https://www.github.com/HelloGaray)
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/hellogaray)
[![twitter](https://img.shields.io/badge/twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)](https://twitter.com/hellogaray)
######  Garrick Chan
[![github](https://img.shields.io/badge/github-FFF?style=for-the-badge&logo=github&logoColor=black)](https://www.github.com/ChanGarrickT)

## 🛠 Technology Stack
| Front-End     | Back-End      |
| ------------- | ------------- |
| HTML          | Python        |
| CSS           | MySQL         |
| Bootstrap     | Jinja         |
Cancel changes
## ⚙️ Database Outline
<img src='https://raw.githubusercontent.com/hellogaray/cs340-project/main/Project/static/ss-diagram.png' width='700'>

## ⛓ Entities
- **customers**: Keeps track of the customer using the following attributes:
  - Customer ID (customer_id - INT, PK, NOT NULL, AUTO INCREMENT, UNIQUE)
  - First Name (first_name - VARCHAR, NOT NULL): First name of the customer.
  - Last Name (last_name - VARCHAR, NOT NULL): Last name of the customer.
  - Phone Number (phone_number - VARCHAR): Using this format ###-###-####. Phone numbers must be unique, no two customers can have the same number.

- **orders**: Tracks the customers to which the orders belong.
  - Order ID (order_id - INT, PK, NOT NULL, AUTO INCREMENT, UNIQUE)
  - Customer (customer_id - INT, FK, NOT NULL): ID of the customer who made this order. 
- **drinks_instances**: When a customer orders a particular drink from base_drinks, a drink instance is created. This instance is then connected to any toppings the customer wants to add. This allows a customer to order multiple of the same base drink, each with different toppings or sizes.
  - Instance ID (instance_id - INT, PK, NOT NULL, AUTO INCREMENT, UNIQUE)
  - Order ID (order_id - INT, FK, NOT NULL): References the order this instance is part of.
  - Drink ID (drink_id - INT, FK, NOT NULL): References the base drink.
  - Size (size - INT, NOT NULL): 0 for Small, 1 for Medium, and 2 for Large.
- **toppings**: Toppings can be added to drinks_instances
  - Topping ID (topping_id - INT, PK, NOT NULL, AUTO INCREMENT, UNIQUE)
  - Topping Name (topping_name - VARCHAR, NOT NULL): The name of the topping.
  - Cost (total_cost, DECIMAL [4,2], NOT NULL): Price of the topping.
 - **base_drinks**: Tracks drinks on the menu and the cost of each, based on size.
   - Drink ID (drink_id - INT, PK, NOT NULL, AUTO INCREMENT, UNIQUE)
   - Name (drink_name - VARCHAR, NOT NULL): The name of the base drink.
   - Small Cost (small_cost - DECIMAL [4,2], NOT NULL): Price of a small drink.
   - Medium Cost (medium_cost - DECIMAL [4,2], NOT NULL): Price of a medium drink.
   - Large Cost (large_cost - DECIMAL [4,2], NOT NULL): Price of a large drink.

## ↔️ Relationships
 - A 1:M relationship between customers and orders. An order made by exactly one customer, and a customer can place many orders.
 - A 1:M relationship between orders and drinks_instances. An order is composed of at least one drink instance, and any given drink instance belongs to exactly one order.
 - A M:M relationship between drinks_instances and toppings. Drinks instances can have 0 or more toppings. Toppings can be in 0 or more drinks instances. A table called drinks_toppings, containing foreign keys to drinks_instances and toppings, is used to achieve the M:M relationship between drinks_instances and toppings.
 - A 1:M relationship between base_drinks and drinks_instances. Any given drink instance is based on exactly one base drink. A base drink can be the basis of 0 or more drink instances
