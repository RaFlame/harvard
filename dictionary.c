// Implements a dictionary's functionality
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <strings.h>
#include <ctype.h>
#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 676;

// Hash table
node *table[N];

//Counter Variable
int  counter = 0;

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    int index = hash(word);
    node *cursor = malloc(sizeof(node));
    do
    {
        cursor = table[index];
        if (strcasecmp(cursor->word, word) == 0)
        {
            return true;
        }
        cursor = cursor->next;
    }
    while (cursor != NULL);
    free(cursor);
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
     unsigned int a1, a2;
    a1 = tolower(word[0]) - 97;
    a2 = tolower(word[1]) - 97;
    return ((26 * a1) + a2);
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
   char tword[LENGTH + 1];
    int index;
    node *n;
    FILE* dic = fopen(dictionary, "r");
    if (dic == NULL)
    {
        return false;
    }
    while ((fscanf(dic, "%s", tword)) != EOF)
    {
        index = hash(tword);
        n = malloc(sizeof(node));
        if (n == NULL)
        {
            return false;
        }
        strcpy(n->word, tword);
        if (table[index] == NULL)
        {
            table[index] = n;
            n->next = NULL;
        }
        else
        {
            n->next = table[index];
            table[index] = n;
        }

        counter++;
    }
    fclose(dic);
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    return counter;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
     // TODO node *cursor; node *temp;

for (int i = 0; i < N; i++)
    {
        node *cursor = table[i];
        do
        {
            node *temp = cursor;
            cursor = temp->next;
            free(temp);
        }
        while (cursor != NULL);
        free(cursor);
    }
    free(table);
    return true;
}
