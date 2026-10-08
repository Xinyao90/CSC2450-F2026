/* Complete supplied demonstration. No student code changes are required. */
#include <assert.h>
#include <semaphore.h>
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

#ifndef CAPACITY
#define CAPACITY 4
#endif
#ifndef ITEMS_PER_PRODUCER
#define ITEMS_PER_PRODUCER 12
#endif
#ifndef PRODUCERS
#define PRODUCERS 2
#endif
#ifndef CONSUMERS
#define CONSUMERS 2
#endif
#if CAPACITY < 1 || CAPACITY > 64
#error "CAPACITY must be 1..64"
#endif
#if ITEMS_PER_PRODUCER < 1 || ITEMS_PER_PRODUCER > 1000 || PRODUCERS < 1 || PRODUCERS > 8 || CONSUMERS < 1 || CONSUMERS > 8
#error "Use 1..1000 items and 1..8 workers of each kind"
#endif
#define TOTAL (PRODUCERS * ITEMS_PER_PRODUCER)
#define STOP 0

static int buffer[CAPACITY], in = 0, out = 0, count = 0;
static int produced = 0, consumed = 0, max_count = 0, seen[TOTAL + 1];
static unsigned long long sum = 0;
static int verbose = 0;
static pthread_mutex_t queue_lock = PTHREAD_MUTEX_INITIALIZER;

/* Permits describe slots/items; the mutex protects the queue metadata. */
static sem_t empty_slots, full_slots;
static void syscheck(int rc, const char *operation) {
    if (rc == -1) { perror(operation); exit(EXIT_FAILURE); }
}
static void wait_permit(sem_t *s) {
    int rc;
    do { rc = sem_wait(s); } while (rc == -1 && errno == EINTR);
    syscheck(rc, "sem_wait");
}

/* These helpers are called ONLY while queue_lock is held. */
static void put_locked(int item) {
    assert(count >= 0 && count < CAPACITY);
    buffer[in] = item;
    in = (in + 1) % CAPACITY;
    count++;
    if (count > max_count) max_count = count;
    if (item != STOP) produced++;
    if (verbose) printf("PUT item=%d count=%d\n", item, count);
}
static int get_locked(void) {
    assert(count > 0 && count <= CAPACITY);
    int item = buffer[out];
    out = (out + 1) % CAPACITY;
    count--;
    if (item != STOP) {
        assert(item >= 1 && item <= TOTAL);
        assert(seen[item] == 0);
        seen[item]++;
        consumed++;
        sum += (unsigned)item;
    }
    if (verbose) printf("GET item=%d count=%d\n", item, count);
    return item;
}

static void put(int item) {
    wait_permit(&empty_slots);  /* Do not hold queue_lock while waiting here. */
    check(pthread_mutex_lock(&queue_lock), "lock queue");
    put_locked(item);
    check(pthread_mutex_unlock(&queue_lock), "unlock queue");
    syscheck(sem_post(&full_slots), "post full_slots");
}
static int get(void) {
    wait_permit(&full_slots);
    check(pthread_mutex_lock(&queue_lock), "lock queue");
    int item = get_locked();
    check(pthread_mutex_unlock(&queue_lock), "unlock queue");
    syscheck(sem_post(&empty_slots), "post empty_slots");
    return item;
}

static void *producer(void *arg) {
    int id = *(const int *)arg;
    for (int i = 1; i <= ITEMS_PER_PRODUCER; i++)
        put(id * ITEMS_PER_PRODUCER + i);
    return NULL;
}
static void *consumer(void *unused) {
    (void)unused;
    while (get() != STOP) {
        /* Real work could process the item here, outside queue_lock. */
    }
    return NULL;
}
int main(int argc, char **argv) {
    if (argc == 2 && strcmp(argv[1], "--trace") == 0) verbose = 1;
    else if (argc != 1) {
        fprintf(stderr, "Usage: %s [--trace]\n", argv[0]);
        return EXIT_FAILURE;
    }
    syscheck(sem_init(&empty_slots, 0, CAPACITY), "init empty_slots");
    syscheck(sem_init(&full_slots, 0, 0), "init full_slots");
    pthread_t p[PRODUCERS], c[CONSUMERS];
    int ids[PRODUCERS];
    for (int i = 0; i < CONSUMERS; i++)
        check(pthread_create(&c[i], NULL, consumer, NULL), "create consumer");
    for (int i = 0; i < PRODUCERS; i++) {
        ids[i] = i;
        check(pthread_create(&p[i], NULL, producer, &ids[i]), "create producer");
    }
    for (int i = 0; i < PRODUCERS; i++) check(pthread_join(p[i], NULL), "join producer");
    /* All real items have been enqueued. One STOP is consumed per consumer. */
    for (int i = 0; i < CONSUMERS; i++) put(STOP);
    for (int i = 0; i < CONSUMERS; i++) check(pthread_join(c[i], NULL), "join consumer");
    int ok = produced == TOTAL && consumed == TOTAL && count == 0 && max_count <= CAPACITY;
    for (int i = 1; i <= TOTAL; i++) if (seen[i] != 1) ok = 0;
    unsigned long long expected_sum = (unsigned long long)TOTAL * (TOTAL + 1) / 2;
    if (sum != expected_sum) ok = 0;
    printf("capacity=%d producers=%d consumers=%d\n", CAPACITY, PRODUCERS, CONSUMERS);
    printf("produced=%d consumed=%d remaining=%d max_count=%d\n", produced, consumed, count, max_count);
    printf("sum=%llu expected_sum=%llu\n", sum, expected_sum);
    printf("%s\n", ok ? "PASS: every real item consumed exactly once" : "FAIL: contract violated");
    syscheck(sem_destroy(&empty_slots), "destroy empty_slots");
    syscheck(sem_destroy(&full_slots), "destroy full_slots");
    check(pthread_mutex_destroy(&queue_lock), "destroy queue_lock");
    return ok ? EXIT_SUCCESS : EXIT_FAILURE;
}
