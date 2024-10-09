import sqlite3

# Connect to an in-memory SQLite database
conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

# Create Students table
cursor.execute('''
CREATE TABLE students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_name TEXT NOT NULL
)
''')

# Create Courses table
cursor.execute('''
CREATE TABLE courses (
    course_id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_name TEXT NOT NULL
)
''')

# Create Student Courses table with composite primary key
cursor.execute('''
CREATE TABLE student_courses (
    student_id INTEGER,
    course_id INTEGER,
    PRIMARY KEY (student_id, course_id)  -- Composite primary key
)
''')

# Insert sample data into Students table
cursor.execute('INSERT INTO students (student_name) VALUES (?)', ('Alice',))
cursor.execute('INSERT INTO students (student_name) VALUES (?)', ('Bob',))

# Insert sample data into Courses table
cursor.execute('INSERT INTO courses (course_name) VALUES (?)', ('Mathematics',))
cursor.execute('INSERT INTO courses (course_name) VALUES (?)', ('Science',))

# Insert sample data into Student Courses table
try:
    cursor.execute('INSERT INTO student_courses (student_id, course_id) VALUES (?, ?)', (1, 1))  # Alice enrolled in Mathematics
    cursor.execute('INSERT INTO student_courses (student_id, course_id) VALUES (?, ?)', (1, 2))  # Alice enrolled in Science
    cursor.execute('INSERT INTO student_courses (student_id, course_id) VALUES (?, ?)', (2, 1))  # Bob enrolled in Mathematics
    
    # Try inserting a duplicate enrollment for Alice in Mathematics
    cursor.execute('INSERT INTO student_courses (student_id, course_id) VALUES (?, ?)', (1, 1))  # This should violate the primary key constraint
    conn.commit()
except sqlite3.IntegrityError as e:
    print(f"Error inserting student_course: {e}")

# Query to fetch all student courses
cursor.execute('SELECT students.student_name, courses.course_name FROM student_courses '
               'JOIN students ON student_courses.student_id = students.student_id '
               'JOIN courses ON student_courses.course_id = courses.course_id')

student_courses = cursor.fetchall()
print("\nStudent Courses:")
for student_course in student_courses:
    print(f"{student_course[0]} is enrolled in {student_course[1]}")

# Close the connection
conn.close()
