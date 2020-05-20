from cs50 import SQL
from csv import reader
from sys import argv

# Interact with sql database to use later in the program
db = SQL("sqlite:///students.db")

# Check Commandline arguments
if len(argv) < 2:
        print("Error, import.py characters.csv")
        exit()
    
# Open CSV file and start reading it line by line
with open(argv[1], newline='') as charactersFile:
    characters = reader(charactersFile)
    for character in characters:
        if character[0] == 'name':
            continue
        
        # Organize the names
        fullName = character[0].split()
        if len(fullName) < 3:
            db.execute("INSERT INTO students(first, middle, last, house, birth) VALUES(?, ?, ?, ?, ?)", fullName [0], None, fullName[1], character[1], character[2])
        else: db.execute("INSERT INTO students(first, middle, last, house, birth) VALUES(?, ?, ?, ?, ?)", fullName[0], fullName[1], fullName[2], character[1], character[2])