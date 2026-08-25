#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <assert.h>
#include "common.h"

int main(int argc, char *argv[])
{
    // Python equivalent:
    // if len(sys.argv) != 2:
    if (argc != 2) {
        fprintf(stderr, "usage: cpu <string>\n");
        exit(1);
    }

    // argv[1] is like sys.argv[1] in Python
    char *str = argv[1];

    // Python equivalent: while True:
    while (1) {
        Spin(1);          // wait one second
        printf("%s\n", str);
    }

    return 0;
}