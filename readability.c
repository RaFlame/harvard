#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <string.h>

int letter;
int word;
int sentence;


int main(void)
{

// prompt the user with the question

    string article = get_string("Text: ");

// set the length of article

    int n = strlen(article);

// add +1 if the article starts with alphanumeric letter

    if (isalnum(article[0]))
    {
        word = 1;
    }



// calculate Coleman-Liau index

    int grade = 0.0588 * (100 * letter / word) - 0.296 * (100 * sentence / word) - 15.8;
// count words

    for (int i = 0; i < n;  i++)
    {
        // count letters

        if (isalnum(article[i]))
        {
            letter++;
        }

        // count words

        if (i < n - 1 && isspace(article[i]) && isalnum(article[i + 1]))
        {
            word++;
        }

        // count sentences

        if (i > 0 && (article[i] == '!' || article[i] == '?' || article[i] == '.') && isalnum(article[i - 1]))
        {
            sentence++;
        }

    }    
// print result
    if (grade <= 1)
    {
        printf("Before Grade 1\n");
    }
    else if (grade < 100)
    {
        printf("Grade %i\n", grade);
    }
    else
    {
        printf("Grade 16+\n");
        
    }
// debugger

    printf("Letters: %i\n Words: %i\n Sentences: %i\n", letter, word, sentence);


}