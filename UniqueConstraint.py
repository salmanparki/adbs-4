import sqlite3

# Connect to an in-memory SQLite database
conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

# Create Users table with a unique constraint on the email column
cursor.execute('''
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
)
''')

# Insert sample data into Users table
try:
    cursor.execute('''
    INSERT INTO users (user_name, email) 
    VALUES (?, ?)
    ''', ('Alice', 'alice@example.com'))

    cursor.execute('''
    INSERT INTO users (user_name, email) 
    VALUES (?, ?)
    ''', ('Bob', 'bob@example.com'))

    # Try inserting a duplicate email
    cursor.execute('''
    INSERT INTO users (user_name, email) 
    VALUES (?, ?)
    ''', ('Charlie', 'alice@example.com'))  # This should violate the unique constraint

    conn.commit()
except sqlite3.IntegrityError as e:
    print(f"Error inserting user: {e}")

# Query to fetch all users
cursor.execute('SELECT * FROM users')
users = cursor.fetchall()
print("\nUsers:")
for user in users:
    print(user)

# Close the connection
conn.close()
