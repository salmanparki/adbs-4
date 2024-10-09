import sqlite3

# Connect to an in-memory SQLite database
conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

# Create Customers table with customer_id and customer_name
cursor.execute('''
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT NOT NULL
)
''')

# Create Orders table with order_id, customer_id (foreign key), and product_id
cursor.execute('''
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    product_id INTEGER,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
)
''')

# Create Products table to simulate multiple joins
cursor.execute('''
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL,
    price REAL NOT NULL
)
''')

# Insert sample data into Customers table
cursor.executemany('''
INSERT INTO customers (customer_name)
VALUES (?)
''', [
    ('Salman',),
    ('rasul',),
    ('ramees',)
])

# Insert sample data into Products table
cursor.executemany('''
INSERT INTO products (product_name, price)
VALUES (?, ?)
''', [
    ('Lays', 1000),
    ('Pringles', 800),
    ('Doritos', 600),
    ('Nachos', 200)
])

# Insert sample data into Orders table (product_id corresponds to products)
cursor.executemany('''
INSERT INTO orders (customer_id, product_id)
VALUES (?, ?)
''', [
    (1, 1),  
    (2, 2),  
    (1, 3),  
    (3, 4)   
])

# 1. INNER JOIN: Fetch records where there's a match in both tables
print("\n1.INNER JOIN:")
cursor.execute('''
SELECT orders.order_id, orders.product_id, customers.customer_name
FROM orders
INNER JOIN customers 
ON orders.customer_id = customers.customer_id
''')
for row in cursor.fetchall():
    print(row)

# 2. LEFT JOIN: Fetch all records from customers and matching orders (if any)
print("\n2.LEFT JOIN:")
cursor.execute('''
SELECT customers.customer_name, orders.product_id
FROM customers
LEFT JOIN orders 
ON customers.customer_id = orders.customer_id
''')
for row in cursor.fetchall():
    print(row)

# 3. RIGHT JOIN (Simulated): Same as LEFT JOIN but with reverse
print("\n3.RIGHT JOIN (Simulated):")
cursor.execute('''
SELECT orders.product_id, customers.customer_name
FROM orders
LEFT JOIN customers ON orders.customer_id = customers.customer_id
WHERE customers.customer_name IS NULL
UNION ALL
SELECT orders.product_id, customers.customer_name
FROM orders
LEFT JOIN customers ON orders.customer_id = customers.customer_id
WHERE customers.customer_name IS NOT NULL
''')
for row in cursor.fetchall():
    print(row)

# 4. FULL OUTER JOIN (Simulated): UNION of LEFT JOIN and RIGHT JOIN
print("\n4. FULL OUTER JOIN (Simulated):")
cursor.execute('''
SELECT customers.customer_name, orders.product_id
FROM customers
LEFT JOIN orders ON customers.customer_id = orders.customer_id
UNION
SELECT customers.customer_name, orders.product_id
FROM orders
LEFT JOIN customers ON orders.customer_id = customers.customer_id
WHERE customers.customer_name IS NULL
''')
for row in cursor.fetchall():
    print(row)

# 5. CROSS JOIN: Every row in customers is combined with every row in orders
print("\n5. CROSS JOIN:")
cursor.execute('''
SELECT customers.customer_name, products.product_name
FROM customers
CROSS JOIN products
''')
for row in cursor.fetchall():
    print(row)

# 6. SELF JOIN: Join the customers table with itself
print("\n6. SELF JOIN:")
cursor.execute('''
SELECT A.customer_name, B.customer_name
FROM customers A, customers B
WHERE A.customer_id != B.customer_id
AND A.customer_name LIKE B.customer_name
''')
for row in cursor.fetchall():
    print(row)

# 7. NATURAL JOIN (Simulated using explicit join on customer_id)
print("\n7. NATURAL JOIN:")
cursor.execute('''
SELECT customers.customer_name, products.product_name
FROM customers
JOIN orders ON customers.customer_id = orders.customer_id
JOIN products ON orders.product_id = products.product_id
''')
for row in cursor.fetchall():
    print(row)

# 8. INNER JOIN with AGGREGATION: Total number of orders per customer
print("\n8. INNER JOIN with AGGREGATION (Total Orders per Customer):")
cursor.execute('''
SELECT customers.customer_name, COUNT(orders.order_id) AS total_orders
FROM customers
INNER JOIN orders ON customers.customer_id = orders.customer_id
GROUP BY customers.customer_name
''')
for row in cursor.fetchall():
    print(row)

# 9. LEFT JOIN with AGGREGATION: Total amount spent by each customer
print("\n9. LEFT JOIN with AGGREGATION (Total Amount Spent per Customer):")
cursor.execute('''
SELECT customers.customer_name, SUM(products.price) AS total_spent
FROM customers
LEFT JOIN orders ON customers.customer_id = orders.customer_id
LEFT JOIN products ON orders.product_id = products.product_id
GROUP BY customers.customer_name
''')
for row in cursor.fetchall():
    print(row)

# 10. Multiple JOINs: Customer, order, and product details
print("\n10. Multiple JOINs (Customer Orders with Product Details):")
cursor.execute('''
SELECT customers.customer_name, products.product_name, products.price
FROM customers
JOIN orders ON customers.customer_id = orders.customer_id
JOIN products ON orders.product_id = products.product_id
''')
for row in cursor.fetchall():
    print(row)

# 11. LEFT JOIN with AGGREGATION and HAVING: Average spent by customers with >1 order
print("\n11. LEFT JOIN with AGGREGATION and HAVING (Avg Spent by Customers with >1 Order):")
cursor.execute('''
SELECT customers.customer_name, AVG(products.price) AS avg_spent
FROM customers
LEFT JOIN orders ON customers.customer_id = orders.customer_id
LEFT JOIN products ON orders.product_id = products.product_id
GROUP BY customers.customer_name
HAVING COUNT(orders.order_id) > 1
''')
for row in cursor.fetchall():
    print(row)

# Close the connection
conn.close()
