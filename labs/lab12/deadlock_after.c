/* Lab 12 AFTER: complete lock-order repair.
 * Both workers acquire the SAME lock objects in the order L1 then L2.
 * Students run this supplied version; no C editing is required.
 */
#define _XOPEN_SOURCE 700
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

/* Array index 0 is L1; array index 1 is L2. */
static pthread_mutex_t locks[2];
static int completed = 0;  /* Updated only while both locks are held. */

typedef struct {
    int id;               /* A = 0, B = 1 */
    const char *name;
} Worker;

static void check(int rc, const char *operation) {
    if (rc != 0) {
        fprintf(stderr, "%s: %s\n", operation, strerror(rc));
        exit(EXIT_FAILURE);
    }
}

/* Supplied demonstration helper: wait until BOTH workers reach this gate. */
static void gate(pthread_barrier_t *barrier) {
    int rc = pthread_barrier_wait(barrier);
    if (rc != 0 && rc != PTHREAD_BARRIER_SERIAL_THREAD) {
        check(rc, "barrier wait");
    }
}

static pthread_barrier_t start_gate;

static void *worker(void *arg) {
    const Worker *w = arg;
    int first = 0;            /* Every worker acquires L1 first. */
    int second = 1;           /* Every worker then acquires L2. */

    gate(&start_gate);        /* Both arrive BEFORE acquiring any mutex. */
    check(pthread_mutex_lock(&locks[first]), "first lock");
    printf("%s holds L%d\n", w->name, first + 1);

    /* No held_gate here: waiting for both workers while holding L1
     * would prevent the other worker from reaching that gate.
     */
    printf("%s requests L%d (still holds L%d)\n",
           w->name, second + 1, first + 1);
    check(pthread_mutex_lock(&locks[second]), "second lock");
    completed++;
    printf("%s completed protected work\n", w->name);
    check(pthread_mutex_unlock(&locks[second]), "unlock second");
    check(pthread_mutex_unlock(&locks[first]), "unlock first");
    return NULL;
}

int main(void) {
    if (setvbuf(stdout, NULL, _IONBF, 0) != 0) {
        fputs("Cannot configure stdout.\n", stderr);
        return EXIT_FAILURE;
    }
    printf("AFTER: PID=%ld; both workers use L1->L2\n", (long)getpid());

    /* Use ordinary, non-recursive mutexes explicitly. */
    pthread_mutexattr_t attr;
    check(pthread_mutexattr_init(&attr), "mutex attribute init");
    check(pthread_mutexattr_settype(&attr, PTHREAD_MUTEX_NORMAL),
          "select normal mutex");
    for (int i = 0; i < 2; i++) {
        check(pthread_mutex_init(&locks[i], &attr), "mutex init");
    }
    check(pthread_mutexattr_destroy(&attr), "mutex attribute destroy");

    check(pthread_barrier_init(&start_gate, NULL, 2), "start gate init");

    Worker args[2] = {{0, "A"}, {1, "B"}};
    pthread_t threads[2];
    /* Create BOTH workers before joining either worker. */
    for (int i = 0; i < 2; i++) {
        check(pthread_create(&threads[i], NULL, worker, &args[i]), "create");
    }
    for (int i = 0; i < 2; i++) {
        check(pthread_join(threads[i], NULL), "join");
    }

    /* All updating workers have been successfully joined. */
    int ok = (completed == 2);
    printf("%s: %d workers completed\n", ok ? "PASS" : "FAIL", completed);
    check(pthread_barrier_destroy(&start_gate), "start gate destroy");
    for (int i = 0; i < 2; i++) {
        check(pthread_mutex_destroy(&locks[i]), "mutex destroy");
    }
    return ok ? EXIT_SUCCESS : EXIT_FAILURE;
}
