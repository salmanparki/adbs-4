import sqlite3

# Connect to an in-memory SQLite database
conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

# Create Courses table with a composite primary key on course_id and department_id
cursor.execute('''
CREATE TABLE courses (
    course_id INTEGER NOT NULL,
    course_name TEXT NOT NULL,
    department_id INTEGER NOT NULL,
    PRIMARY KEY (course_id, department_id)
)
''')

# Insert sample data into Courses table
try:
    cursor.execute('''
    INSERT INTO courses (course_id, course_name, department_id) 
    VALUES (?, ?, ?)
    ''', (101, 'Introduction to Programming', 1))

    cursor.execute('''
    INSERT INTO courses (course_id, course_name, department_id) 
    VALUES (?, ?, ?)
    ''', (102, 'Data Structures', 1))

    cursor.execute('''
    INSERT INTO courses (course_id, course_name, department_id) 
    VALUES (?, ?, ?)
    ''', (101, 'Advanced Programming', 2))  # Same course_id but different department_id

    # Try inserting a course with a duplicate composite key
    cursor.execute('''
    INSERT INTO courses (course_id, course_name, department_id) 
    VALUES (?, ?, ?)
    ''', (101, 'Intro to Programming', 1))  # This should violate the primary key constraint

    conn.commit()
except sqlite3.IntegrityError as e:
    print(f"Error inserting course: {e}")

# Query to fetch all courses
cursor.execute('SELECT * FROM courses')
courses = cursor.fetchall()
print("\nCourses:")
for course in courses:
    print(course)

# Close the connection
conn.close()
