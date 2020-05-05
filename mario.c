// Prints a right angled pyramid
#include <cs50.h>
#include <stdio.h>

int get_positive_int(void);
// Here i choose the data type 
int main(void)

{
//adding names to data type to create the variables
    int n, i, k, j;
    do
    {
// Creating a do loop to request user for integer
        n = get_int("Size: ");
    }
//Making sure user can only input values between the positive integers 1 and 8
    while (n < 1 || n > 8);
    for (i = 0; i < n; i++)
    {
// this for loop makes sure the pyramid will be angled to the right       
        for (k = 7; k >= j; k--)
        {
            printf(" ");
        }
        for (j = 0; j <= i; j++)
        {
            printf("#");
            
        
        }
        printf("\n");
        
    }
}
    


