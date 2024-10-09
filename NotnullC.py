import sqlite3

# Connect to an in-memory SQLite database
conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

# Create Users table with NOT NULL constraints on username and email fields
cursor.execute('''
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT NOT NULL
)
''')

# Insert sample data into Users table
try:
    cursor.execute('INSERT INTO users (username, email) VALUES (?, ?)', ('Alice', 'alice@example.com'))
    cursor.execute('INSERT INTO users (username, email) VALUES (?, ?)', ('Bob', 'bob@example.com'))
    
    # Try inserting a user with a NULL username
    cursor.execute('INSERT INTO users (username, email) VALUES (?, ?)', (None, 'charlie@example.com'))  # This should violate the NOT NULL constraint
    
    # Try inserting a user with a NULL email
    cursor.execute('INSERT INTO users (username, email) VALUES (?, ?)', ('Dave', None))  # This should also violate the NOT NULL constraint

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
