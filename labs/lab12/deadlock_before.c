/* Lab 12 BEFORE: complete, intentionally deadlocking demonstration.
 * Run on Linux ONLY with a time limit, for example:
 *   timeout --kill-after=1s 5s ./deadlock_before
 * Students observe the result; no C editing is required.
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

static pthread_barrier_t start_gate, held_gate;

static void *worker(void *arg) {
    const Worker *w = arg;
    int first = w->id;         /* A: L1 first; B: L2 first. */
    int second = 1 - w->id;    /* A: L2 next;  B: L1 next. */

    gate(&start_gate);         /* Nobody holds a mutex at this gate. */
    check(pthread_mutex_lock(&locks[first]), "first lock");
    printf("%s holds L%d\n", w->name, first + 1);

    /* TEST SETUP ONLY: each worker now holds a DIFFERENT first lock.
     * Both must reach this gate before either requests its second lock.
     * This arranges the dangerous schedule WITHOUT relying on sleep().
     */
    gate(&held_gate);

    printf("%s requests L%d (still holds L%d)\n",
           w->name, second + 1, first + 1);
    check(pthread_mutex_lock(&locks[second]), "second lock");
    /* Neither worker can reach this point in the intended run. */
    completed++;
    printf("%s completed protected work\n", w->name);
    check(pthread_mutex_unlock(&locks[second]), "unlock second");
    check(pthread_mutex_unlock(&locks[first]), "unlock first");
    return NULL;
}

int main(void) {
    /* Keep diagnostic lines visible even when output is redirected. */
    if (setvbuf(stdout, NULL, _IONBF, 0) != 0) {
        fputs("Cannot configure stdout.\n", stderr);
        return EXIT_FAILURE;
    }
    printf("BEFORE: PID=%ld; A uses L1->L2, B uses L2->L1\n", (long)getpid());

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
    check(pthread_barrier_init(&held_gate, NULL, 2), "held gate init");

    Worker args[2] = {{0, "A"}, {1, "B"}};
    pthread_t threads[2];
    /* Create BOTH workers before joining either worker. */
    for (int i = 0; i < 2; i++) {
        check(pthread_create(&threads[i], NULL, worker, &args[i]), "create");
    }
    for (int i = 0; i < 2; i++) {
        check(pthread_join(threads[i], NULL), "join");
    }

    /* Unreachable in the intended deadlock: timeout ends this process. */
    fprintf(stderr, "UNEXPECTED: %d workers completed.\n", completed);
    return EXIT_FAILURE;
}
