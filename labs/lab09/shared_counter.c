#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

#define ITERATIONS 1000000

typedef struct {
    int value;
} Counter;

/* Shared counter */
Counter counter = {0};

/* Code executed by each worker thread */
void *worker(void *arg) {
    for (int i = 0; i < ITERATIONS; i++) {
        counter.value++;
    }

    return NULL;
}

int main() {
    pthread_t a, b;

    printf("Expected final value: %d\n", 2 * ITERATIONS);

    /* Create two worker threads */
    pthread_create(&a, NULL, worker, NULL);
    pthread_create(&b, NULL, worker, NULL);

    /* Wait for both workers to finish */
    pthread_join(a, NULL);
    pthread_join(b, NULL);

    printf("Actual final value:   %d\n", counter.value);

    return 0;
}
