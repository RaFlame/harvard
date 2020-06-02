from cs50 import get_string
letter = 0
sentence = 0
word = 1
# Ask the user for the text
text = get_string("Text: ")
# calculate words, sentences & letters
n = len(text)
for i in range(n):
    if text[i].isalnum() == True:
        letter = letter+1
for i in range(n):
    if text[i].isspace() == True and text[i+1].isalnum() == True:
        word = word+1
for i in range(n):
    # include calculation for symbols 
    if text[i] == "?" or text[i] == "." or text[i] == "!" or text[i] == ":":
        sentence = sentence+1
# set up the coleman-liau index formula
grade = round(0.0588 * ((100 * letter) / word) - 0.296 * ((100 * sentence) / word) - 15.8)
if grade < 1:
    print("Before Grade 1")
elif grade < 16:
    print(f"Grade {grade}")
else:
    print("Grade 16+")