import sqlite3

# Connect to an in-memory SQLite database
conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

# Create Authors table with author_id and author_name
cursor.execute('''
CREATE TABLE authors (
    author_id INTEGER PRIMARY KEY AUTOINCREMENT,
    author_name TEXT NOT NULL
)
''')

# Create Books table with book_id, book_title, and author_id (foreign key referencing authors table)
cursor.execute('''
CREATE TABLE books (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_title TEXT NOT NULL,
    author_id INTEGER,
    FOREIGN KEY (author_id) REFERENCES authors(author_id)
)
''')

# Insert sample data into Authors table
cursor.executemany('''
INSERT INTO authors (author_name)
VALUES (?)
''', [
    ('George Orwell',),
    ('J.K. Rowling',),
    ('J.R.R. Tolkien',)
])

# Insert sample data into Books table
cursor.executemany('''
INSERT INTO books (book_title, author_id)
VALUES (?, ?)
''', [
    ('1984', 1),          # George Orwell
    ('Harry Potter', 2),   # J.K. Rowling
    ('The Hobbit', 3)      # J.R.R. Tolkien
])

# Query to check the Books with their respective Authors
print("\nBooks and their respective authors:")
cursor.execute('''
SELECT books.book_title, authors.author_name
FROM books
JOIN authors ON books.author_id = authors.author_id
''')
for row in cursor.fetchall():
    print(row)

# Close the connection
conn.close()
