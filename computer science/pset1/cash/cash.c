#include <cs50.h>
#include <stdio.h>
#include <math.h>

int main(void)
{
    //Set datatype to float to handle dollars and cents
    float dollars;
    do
    {
        //We get the dollar amount from the user until you get a valid input, inluding negative amount
        dollars = get_float("Change owed: ");
    }
    while (dollars < 0);
    
    // rounding the cents to the nearest penny using the math library
    int cents = round(dollars * 100);
    int coins = 0;
    
    int denominations[] = {25, 10, 5, 1};
    int size = 4;
    for (int i = 0; i < size; i++)
    {
        coins += cents / denominations[i];
        cents %= denominations[i];
    }
    printf("%i\n", coins);    
}