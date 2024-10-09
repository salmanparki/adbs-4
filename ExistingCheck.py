import sqlite3

# Connect to an in-memory SQLite database
conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

# Step 1: Create the original employees table
cursor.execute('''
CREATE TABLE employees (
    employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_name TEXT NOT NULL,
    salary REAL
)
''')

# Insert sample data into employees table
cursor.execute('INSERT INTO employees (employee_name, salary) VALUES (?, ?)', ('Alice', 50000))
cursor.execute('INSERT INTO employees (employee_name, salary) VALUES (?, ?)', ('Bob', -30000))  # Invalid salary
cursor.execute('INSERT INTO employees (employee_name, salary) VALUES (?, ?)', ('Charlie', 70000))

# Step 2: Create a new employees table with CHECK constraint
cursor.execute('''
CREATE TABLE new_employees (
    employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_name TEXT NOT NULL,
    salary REAL CHECK (salary > 0)
)
''')

# Step 3: Copy data from old table to new table
cursor.execute('''
INSERT INTO new_employees (employee_id, employee_name, salary)
SELECT employee_id, employee_name, salary
FROM employees
WHERE salary > 0
''')

# Step 4: Drop the old employees table
cursor.execute('DROP TABLE employees')

# Step 5: Rename the new table to employees
cursor.execute('ALTER TABLE new_employees RENAME TO employees')

# Query to fetch all employees from the updated table
cursor.execute('SELECT * FROM employees')
employees = cursor.fetchall()
print("\nEmployees:")
for employee in employees:
    print(employee)

# Close the connection
conn.close()
