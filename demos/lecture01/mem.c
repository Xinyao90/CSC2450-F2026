#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <assert.h> 
#include "common.h"

int main(int argc, char *argv[])
{
    // Create space in memory for one integer.
    // p stores the address of that memory.
    int *p = malloc(sizeof(int));

    // Make sure memory was created successfully.
    assert(p != NULL);

    // Print the process ID and memory address.
    printf("(%d) address pointed to by p: %p\n",
           getpid(), p);

    // Put 0 into that memory location.
    *p = 0;

    while (1) {

        // Wait about one second.
        Spin(1);

        // Increase the value by 1.
        *p = *p + 1;

        // Print the process ID and current value.
        printf("(%d) p: %d\n",
               getpid(), *p);
    }

    return 0;
}
