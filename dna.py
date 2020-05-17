from csv import reader, DictReader
from sys import argv

if len(argv) < 3:
    print("usage error, dna.py sequence.txt database.csv")
    exit()

# open the file and read the dna sequence
with open(argv[2]) as dnafile:
    dnareader = reader(dnafile)
    for row in dnareader:
        dnalist = row

# save in a string
dna = dnalist[0]

# For counting the sequences I create a dictionary
sequences = {}

# get the sequences from the database and put into a list
with open(argv[1]) as namesfile:
    names = reader(namesfile)
    for row in names:
        dnaSequences = row
        dnaSequences.pop(0)
        break

# duplicate the list into a dictionary where genes represents the keys
for item in dnaSequences:
    sequences[item] = 1

# go trough the dna sequence and count the repetitions
for key in sequences:
    l = len(key)
    tempMax = 0
    temp = 0
    for i in range(len(dna)):
        # making sure it will stop counting
        while temp > 0:
            temp -= 1
            continue

        # start counting repeteted keys
        if dna[i: i + l] == key:
            while dna[i - l: i] == dna[i: i + l]:
                temp += 1
                i += l

            # Compare values
            if temp > tempMax:
                tempMax = temp

    # store the longest sequences 
    sequences[key] += tempMax

# opens the names database and compare sequences
with open(argv[1], newline='') as namesfile:
    names = DictReader(namesfile)
    for person in names:
        match = 0
        # compares the sequences and print name
        for dna in sequences:
            if sequences[dna] == int(person[dna]):
                match += 1
        if match == len(sequences):
            print(person['name'])
            exit()
    # it there is no match print info
    print("No match")