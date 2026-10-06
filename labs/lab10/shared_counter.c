#include <errno.h>
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* pthread functions return an error number; they do not use errno here. */
static void check(int rc, const char *operation) {
    if (rc != 0) {
        fprintf(stderr, "%s: %s\n", operation, strerror(rc));
        exit(EXIT_FAILURE);
    }
}

/* LAB 10 STARTER: INTENTIONALLY UNSAFE UNTIL YOU ADD THE TWO MUTEX CALLS.
 * Concurrent counter++ operations without synchronization cause a C data race
 * and undefined behavior. Do not infer a guaranteed numeric outcome from it.
 * counter_lock is supplied; use that SAME mutex for every worker.
 */
static unsigned long long counter = 0;
static pthread_mutex_t counter_lock = PTHREAD_MUTEX_INITIALIZER;
static long iterations = 1000000;

static long positive(const char *s, long max, const char *name) {
    char *end = NULL;
    errno = 0;
    long n = strtol(s, &end, 10);
    if (errno || *s == '\0' || *end != '\0' || n < 1 || n > max) {
        fprintf(stderr, "%s must be between 1 and %ld\n", name, max);
        exit(EXIT_FAILURE);
    }
    return n;
}

static void increment(void) {
    /* TODO 1: acquire counter_lock before reading/modifying counter. */
    counter++;
    /* TODO 2: release counter_lock after the complete increment. */
}

static void *worker(void *unused) {
    (void)unused;
    for (long i = 0; i < iterations; i++) {
        increment();
    }
    return NULL;
}

int main(int argc, char **argv) {
    if (argc > 3) {
        fprintf(stderr, "Usage: %s [workers 1..16] [iterations 1..1000000]\n", argv[0]);
        return EXIT_FAILURE;
    }
    int workers = argc > 1 ? (int)positive(argv[1], 16, "workers") : 2;
    if (argc > 2) iterations = positive(argv[2], 1000000, "iterations");
    pthread_t threads[16];
    unsigned long long expected = (unsigned long long)workers * (unsigned long long)iterations;
    for (int i = 0; i < workers; i++)
        check(pthread_create(&threads[i], NULL, worker, NULL), "create");
    for (int i = 0; i < workers; i++)
        check(pthread_join(threads[i], NULL), "join");

    /* Workers have all finished. This read does not overlap their updates. */
    printf("workers=%d iterations=%ld expected=%llu actual=%llu\n",
           workers, iterations, expected, counter);
    int ok = counter == expected;
    printf("%s\n", ok ? "PASS: total matches" : "FAIL: lost or incorrect updates");
    check(pthread_mutex_destroy(&counter_lock), "destroy");
    return ok ? EXIT_SUCCESS : EXIT_FAILURE;
}
