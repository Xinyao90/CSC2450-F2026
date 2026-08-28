#include <stdio.h>      // printf()
#include <stdlib.h>     // exit()
#include <unistd.h>     // fork(), getpid(), getppid(), sleep()
#include <sys/wait.h>   // wait()

int main()
{
    printf("Before fork:\n");
    printf("Current process PID = %d\n\n", getpid());

    // fork() creates a new process
    pid_t pid = fork();

    if (pid < 0) {

        // fork() failed
        printf("ERROR: fork failed\n");
        exit(1);
    }

    else if (pid == 0) {

        // ------------------------
        // CHILD PROCESS
        // ------------------------

        printf("CHILD:\n");
        printf("  My PID  = %d\n", getpid());
        printf("  My PPID = %d\n", getppid());

        printf("  Child is working...\n");

        sleep(5);

        printf("  Child finished.\n");

        exit(0);
    }

    else {

        // ------------------------
        // PARENT PROCESS
        // ------------------------

        printf("PARENT:\n");
        printf("  My PID       = %d\n", getpid());
        printf("  Child PID    = %d\n", pid);

        printf("  Parent is waiting for child...\n");

        // Wait until the child finishes
        wait(NULL);

        printf("  Parent: child finished.\n");
    }

    return 0;
}
