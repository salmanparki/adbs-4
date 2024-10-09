import sqlite3

# Connect to an in-memory SQLite database
conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

# Create Products table with a CHECK constraint on the price column
cursor.execute('''
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL,
    price REAL CHECK (price > 0)
)
''')

# Insert sample data into Products table
try:
    cursor.execute('''
    INSERT INTO products (product_name, price) 
    VALUES (?, ?)
    ''', ('Laptop', 999.99))

    cursor.execute('''
    INSERT INTO products (product_name, price) 
    VALUES (?, ?)
    ''', ('Smartphone', 499.99))

    # Try inserting a product with a non-positive price
    cursor.execute('''
    INSERT INTO products (product_name, price) 
    VALUES (?, ?)
    ''', ('Free Sample', -10.00))  # This should violate the CHECK constraint

    conn.commit()
except sqlite3.IntegrityError as e:
    print(f"Error inserting product: {e}")

# Query to fetch all products
cursor.execute('SELECT * FROM products')
products = cursor.fetchall()
print("\nProducts:")
for product in products:
    print(product)

# Close the connection
conn.close()
