#include <stdio.h>      // printf(), fgets()
#include <stdlib.h>     // exit()
#include <string.h>     // strlen()
#include <unistd.h>     // fork(), execlp(), getpid()
#include <sys/wait.h>   // waitpid()

int main()
{
    char cmd[256];

    while (1) {

        // -------------------------------
        // 1. Read a command from the user
        // -------------------------------
        printf("myshell> ");

        // Read one line from the keyboard.
        if (fgets(cmd, sizeof(cmd), stdin) == NULL) {
            break;
        }

        // Remove the newline added by pressing Enter.
        cmd[strcspn(cmd, "\n")] = '\0';

        // Allow the user to exit our shell.
        if (strcmp(cmd, "exit") == 0) {
            printf("Exiting shell.\n");
            break;
        }

        // Ignore an empty command.
        if (strlen(cmd) == 0) {
            continue;
        }


        // -------------------------------
        // 2. Create a new process
        // -------------------------------
        pid_t pid = fork();


        // -------------------------------
        // 3. Child process
        // -------------------------------
        if (pid == 0) {

            printf("Child PID: %d\n", getpid());

            /*
             * Replace the child process with
             * the program requested by the user.
             *
             * /bin/sh -c cmd
             *
             * means:
             * "Ask the system shell to run cmd."
             *
             * Example:
             *     cmd = "ls -l"
             */
            execlp(
                "/bin/sh",
                "sh",
                "-c",
                cmd,
                (char *) NULL
            );

            /*
             * IMPORTANT:
             *
             * If exec succeeds, this code is NEVER reached.
             *
             * exec replaces the child process's current
             * program with the requested program.
             */
            printf("ERROR: could not execute %s\n", cmd);

            exit(1);
        }


        // -------------------------------
        // 4. Parent process
        // -------------------------------
        else if (pid > 0) {

            printf("Parent waiting for child PID %d...\n", pid);

            /*
             * Wait until this child process finishes.
             */
            waitpid(pid, NULL, 0);

            printf("Child finished.\n");
        }


        // -------------------------------
        // 5. fork() failed
        // -------------------------------
        else {

            printf("ERROR: fork failed\n");
            exit(1);
        }
    }

    return 0;
}
