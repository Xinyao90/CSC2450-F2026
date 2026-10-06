# Lab 10 — Shared-counter mutex repair

Complete TODO 1 and TODO 2 in `increment()` using the same `counter_lock`.
Preserve one shared counter and create-all-then-join-all worker structure.
The plain counter before repair has a C data race; its numeric result is not guaranteed.

```bash
gcc -std=c11 -O0 -Wall -Wextra -pthread shared_counter.c -o shared_counter
# After repair:
for run in 1 2 3 4 5; do
    ./shared_counter 2 1000000
done
./shared_counter 4 250000
./shared_counter 1 1000000
```

Arguments are worker count and increments per worker. The expected total is their
product. Correct completed repaired runs should match; different outputs are not
required. Include the command and result in your screenshot. Use the worksheet
for the record table, four explanation questions, and submission checklist.
