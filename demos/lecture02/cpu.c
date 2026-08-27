// cpu.c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/time.h>

// Busy-wait for approximately "seconds" seconds.
// This intentionally uses the CPU.
void Spin(int seconds)
{
    struct timeval start, now;

    gettimeofday(&start, NULL);

    while (1) {
        gettimeofday(&now, NULL);

        double elapsed =
            (now.tv_sec - start.tv_sec) +
            (now.tv_usec - start.tv_usec) / 1000000.0;

        if (elapsed >= seconds)
            break;
    }
}

int main(int argc, char *argv[])
{
    if (argc != 2) {
        fprintf(stderr, "usage: cpu <string>\n");
        exit(1);
    }

    while (1) {
        Spin(1);

        printf("PID %d: %s\n",
               getpid(), argv[1]);
    }

    return 0;
}
