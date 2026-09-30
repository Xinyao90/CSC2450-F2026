#include <stdio.h>
#include <unistd.h>
#include <pthread.h>

void *worker(void *arg) {
    sleep(30);
    return NULL;
}

int main() {
    pthread_t a, b;

    printf("PID: %d\n", getpid());

    pthread_create(&a, NULL, worker, NULL);
    pthread_create(&b, NULL, worker, NULL);

    sleep(30);

    pthread_join(a, NULL);
    pthread_join(b, NULL);

    return 0;
}
