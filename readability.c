#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <string.h>
#include <math.h>

int letter;
int word;
int sentence;


int main(void)
{

// prompt the user with the question

    string s = get_string("Text: ");
    int num_words, num_sentences, num_letters;
    num_words = num_sentences = num_letters = 0;
    for (int i = 0, len = strlen(s); i < len; i++)
    {
        if (isalpha(s[i]))
            num_letters++;
        if ((i == 0 && s[i] != ' ') 
        || (i != len - 1 && s[i] == ' ' && s[i+ 1] != ' '))
            num_words++;
        if (s[i] == '.' || s[i] == '?' || s[i] == '!')
            num_sentences++;
    }
    float L = (num_letters / (float) num_words) * 100;
    float S = (num_sentences / (float) num_words) * 100;
    int index = round(0.0588 * L - 0.296 * S - 15.8);
    if (index < 1)
        printf("Before Grade 1\n");
    else if (index >= 16)
        printf("Grade 16+\n");
    else 
        printf("Grade %i\n", index);

}