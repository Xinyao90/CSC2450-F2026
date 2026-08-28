#include <stdio.h>      // printf()
#include <unistd.h>     // getpid(), getppid(), sleep()

int main()
{
    // PID = ID of this running process
    printf("My PID  = %d\n", getpid());

    // PPID = ID of the process that started this process
    // Usually this is the shell
    printf("My PPID = %d\n", getppid());

    printf("Process is running for 300 seconds...\n");

    // Keep the process alive long enough to inspect it
    sleep(300);

    printf("Process finished.\n");

    return 0;
}
