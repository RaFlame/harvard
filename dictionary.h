// Declares a dictionary's functionality

#ifndef DICTIONARY_H
#define DICTIONARY_H

#include <stdbool.h>

// Maximum length for a word
// (e.g., pneumonoultramicroscopicsilicovolcanoconiosis)
#define LENGTH 45

// Prototypes
//Returns true if word is in dictionary else false
bool check(const char *word);


unsigned int hash(const char *word);

//Loads dictionary into memory. Returns true if succssfule else false.
bool load(const char *dictionary);

//Returns number of words in dictionary if loaded else 0 if not yet loaded.
unsigned int size(void);

//Unloads dictionary from memory. Returns true if successfule else false.
bool unload(void);

#endif // DICTIONARY_H
