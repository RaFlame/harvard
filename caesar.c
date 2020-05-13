#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <cs50.h>
#include <ctype.h>

int main(int argc, string argv[])
{


// check there is only 1 arguments and it is a number else returns instructions
    if (argc == 2 && isdigit(*argv[1]))
        
    {
// chech for non-numeric key
int len_of_argv = strlen(argv[1]);

for (int i = 0; i < len_of_argv; i ++)
{
    int restz = isalpha(argv[1][i]);
    if (restz != 0)
    {
        printf("Usage: ./caesar key \n");
        return 1;
    }
}
        int k = atoi(argv[1]); // get the ceasar KEY value convert into integar

        string s = get_string("plaintext: "); // get text
        printf("ciphertext: "); // print out cipher

// iterate through plain text letter by letter
        for (int i = 0, n = strlen(s) ; i < n; i++)
        {
            // checking if it is lowercase 97 = a to 112 = z and if it + 13 characters along.
            if (s[i] >= 'a' && s[i] <= 'z')
            {
                printf("%c", (((s[i] - 'a') + k) % 26) + 'a'); // print out lowercase with key
            } // if it it between uppercase A and C
            else if (s[i] >= 'A' && s[i] <= 'Z')
            {
                printf("%c", (((s[i] - 'A') + k) % 26) + 'A'); // print out uppercase with key
            }

            else

            {
                printf("%c", s[i]);
            }
        }

        printf("\n");
        return 0;
    }

    else
    {
        printf("Usage: ./caesar k\n");
        return 1;

    }

}