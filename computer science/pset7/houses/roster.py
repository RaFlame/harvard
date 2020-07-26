from cs50 import SQL
from sys import argv

# Check Commandline arguments
if len(argv) < 2:
    print("Error, roster.py houseName")
    exit()
    
# Open the database and run query
db = SQL("sqlite:///students.db")
students = db.execute("SELECT * FROM students WHERE house = (?) ORDER BY last", argv[1])

# Display the list with the students information
for student in students:
    if student['middle'] != None:
        print(f"{student['first']} {student['middle']} {student['last']}, born {student['birth']}")
    else:
        print(f"{student['first']} {student['last']}, born {student['birth']}")

