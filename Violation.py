import sqlite3

# Connect to an in-memory SQLite database
conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

# Enable foreign key support in SQLite
cursor.execute('PRAGMA foreign_keys = ON;')

# Create Customers table
cursor.execute('''
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT NOT NULL
)
''')

# Create Orders table with a foreign key referencing the Customers table
cursor.execute('''
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    order_date TEXT NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
)
''')

# Insert sample data into Customers table
cursor.execute('''
INSERT INTO customers (customer_name) 
VALUES ('John Doe')
''')

# Try inserting a valid order (customer_id exists)
try:
    cursor.execute('''
    INSERT INTO orders (customer_id, order_date) 
    VALUES (1, '2024-10-09')
    ''')
    conn.commit()
    print("Order inserted successfully.")
except sqlite3.IntegrityError as e:
    print(f"Error inserting order: {e}")

# Try inserting an order with a non-existing customer_id (customer_id = 999)
try:
    cursor.execute('''
    INSERT INTO orders (customer_id, order_date) 
    VALUES (999, '2024-10-09')
    ''')
    conn.commit()
except sqlite3.IntegrityError as e:
    print(f"Error inserting order with non-existing customer_id: {e}")

# Close the connection
conn.close()
