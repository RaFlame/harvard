// Prints a right angled pyramid
#include <cs50.h>
#include <stdio.h>

// Here i choose the data type 
int main(void)
{
//adding names to data type to create the variables
    int n;
    do
    {
// Creating a do loop to request user for integer
        n = get_int("Height: ");
    }
//Making sure user can only input values between the positive integers 1 and 8
    while (n < 1 || n > 8);
    
    for (int i = 0; i < n; i++)
    {
// this for loop makes sure the pyramid will be angled to the right       
        for (int j = 0; j < n; j++)
        {
            if (i + j < n - 1)
                printf(" ");
            else
                printf("#");
        }
        printf("\n");
    }
}
    


