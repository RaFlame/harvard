#include <stdio.h>
#include <stdlib.h>
#include <cs50.h>
#include <stdint.h>
//define a byte to be dist data byte
typedef uint8_t BYTE;
//define block size to be 512
#define BLOCK_SIZE 512
//string size defined to 8
#define FILE_NAME_SIZE 8

//create a jpeg function
bool is_start_new_jpeg(BYTE buffer[]);
int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }
    // we open a card image and check if it is NULL or not
    FILE *infile = fopen(argv[1], "r");
    if (infile == NULL)
    {
        printf("file not found\n");
        return 1;
    }
    
    //Define BYTE array (512)
    BYTE buffer[BLOCK_SIZE];
    int file_index = 0;
    bool have_found_first_jpg = false; 
    FILE *outfile;
    //Read from the infile to the buffer
    while (fread(buffer, BLOCK_SIZE, 1, infile))
    {
        if (is_start_new_jpeg(buffer))
        {
            if (!have_found_first_jpg)
            {
                have_found_first_jpg = true;
            }
                
            else 
            {
                fclose(outfile);
            }
            
            char filename[FILE_NAME_SIZE];
            sprintf(filename, "%03i.jpg", file_index++);
            //then i use the outfile for the output from the buffer into the oufile
            outfile = fopen(filename, "w");
            if (outfile == NULL)
            {
                return 1;
            }
                
            fwrite(buffer, BLOCK_SIZE, 1, outfile);
            
        }
        else if (have_found_first_jpg)
        {
            //run the previous file
            fwrite(buffer, BLOCK_SIZE, 1, outfile);
        }
    }
    
    //then we close the out- and in-files
    fclose(outfile);
    fclose(infile);
}
bool is_start_new_jpeg(BYTE buffer[])
{
    return buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0;
}
