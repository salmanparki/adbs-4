import sqlite3

# Connect to an in-memory SQLite database
conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

# Enable foreign key support in SQLite (this is necessary for cascading deletes to work)
cursor.execute('PRAGMA foreign_keys = ON;')

# Create Categories table with category_id and category_name
cursor.execute('''
CREATE TABLE categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT NOT NULL
)
''')

# Create Products table with product_id, product_name, and category_id (foreign key with ON DELETE CASCADE)
cursor.execute('''
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL,
    category_id INTEGER,
    FOREIGN KEY (category_id) REFERENCES categories(category_id) ON DELETE CASCADE
)
''')

# Insert sample data into Categories table
cursor.executemany('''
INSERT INTO categories (category_name)
VALUES (?)
''', [
    ('Electronics',),
    ('Furniture',),
    ('Clothing',)
])

# Insert sample data into Products table
cursor.executemany('''
INSERT INTO products (product_name, category_id)
VALUES (?, ?)
''', [
    ('Laptop', 1),      # Electronics
    ('Sofa', 2),        # Furniture
    ('T-shirt', 3),     # Clothing
    ('Smartphone', 1)   # Electronics
])

# Query to check the Products before deletion
print("\nProducts before deleting a category:")
cursor.execute('''
SELECT products.product_name, categories.category_name
FROM products
JOIN categories ON products.category_id = categories.category_id
''')
for row in cursor.fetchall():
    print(row)

# Delete a category (e.g., Electronics) from the Categories table
cursor.execute('''
DELETE FROM categories WHERE category_name = 'Electronics'
''')

# Query to check the Products after deleting the Electronics category
print("\nProducts after deleting the 'Electronics' category (should be removed due to cascade delete):")
cursor.execute('''
SELECT products.product_name, categories.category_name
FROM products
JOIN categories ON products.category_id = categories.category_id
''')
for row in cursor.fetchall():
    print(row)

# Close the connection
conn.close()
