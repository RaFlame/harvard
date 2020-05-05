// Prints 3-by-3 grid of bricks
#include <cs50.h>
#include <stdio.h>

int main(void)

{
    int n,i,k,j;
    do
    {
        n = get_int("Size: ");
    }
    while (n < 1 || n > 8);
    for(i = 0; i < n; i++)
    {
        for(k = 7; k >= j; k--)
        
            printf(" ");
        
        for(j = 0; j <= i; j++)
        {
            printf("#");
        
        }
        
        printf("\n");
    }
}
    


