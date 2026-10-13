# Lab 12 — Deadlock: Observe Before and After

**Time:** about 10 minutes. **No C writing, editing, or repair.**
Run two complete supplied programs once each, then explain their different behavior.

## Run both programs
Extract the entire `lab12_observe` folder on the Linux class server. Run:

```bash
cd lab12_observe
bash run_demo.sh
```

The script builds `deadlock_before.c` and `deadlock_after.c`, runs each once under a five-second limit, and displays both outputs and exit statuses. New output files are saved in a fresh `run_output.*` directory. Submit a screenshot; no full-log submission is required. No administrator privileges are needed.

The BEFORE demonstration intentionally cannot complete its protected work once the arranged lock cycle is reached. Do not run its executable without `timeout`. If you accidentally do so in the foreground, press Ctrl-C. The AFTER program is complete; do not modify it.

## What to observe
Look for each worker's first acquired lock, requested second lock, and whether a completion message appears. `holds` is printed after a successful first acquisition. `requests` is printed immediately before the second lock call. A/B line order and process IDs may vary.

The expected BEFORE exit status is 124 (the supplied `timeout` stopped it). The expected AFTER status is 0, with `PASS: 2 workers completed`. A timeout alone is not proof of a deadlock: explain the dependency using the held/requested locks. Keep unexpected results and ask the instructor; do not debug or edit the C source.

## Three short questions
1. Record the BEFORE and AFTER exit statuses. For each run, did either worker print `completed protected work`? Did the final PASS message appear?
2. In BEFORE, what does A hold and request? What does B hold and request? Explain why neither can reach its unlock calls.
3. In AFTER, what common lock-acquisition order do both workers follow? Explain why a worker waiting to acquire L1 cannot already be holding L2 in this program.

## Submit
One screenshot showing both runs and their exit statuses, plus the three answers (on the one-page worksheet or in Brightspace). No C files, binaries, repairs, repeated runs, or extra tests are required.

## Optional manual commands (alternative to the script, not additional work)
```bash
gcc -std=c11 -O0 -Wall -Wextra -pthread deadlock_before.c -o deadlock_before
gcc -std=c11 -O0 -Wall -Wextra -pthread deadlock_after.c -o deadlock_after

timeout --kill-after=1s 5s ./deadlock_before
echo "BEFORE exit status: $?"

timeout --kill-after=1s 5s ./deadlock_after
echo "AFTER exit status: $?"
```
Read `$?` immediately after its run, before another command changes it. The timeout is only a safety limit, not a mutex repair.

## Reading the supplied code (no implementation task)
`locks[0]` is L1 and `locks[1]` is L2. Both workers are created before either is joined.

BEFORE sets the order from each worker's ID:
```c
int first = w->id;       /* A: L1; B: L2 */
int second = 1 - w->id;  /* A: L2; B: L1 */
```
AFTER sets the same resource order for both workers:
```c
int first = 0;  /* L1 */
int second = 1; /* L2 */
```

**Supplied demonstration setup:** A barrier is a meeting point that waits until both workers arrive. BEFORE includes an extra meeting point after each worker takes its different first lock; this makes the dangerous interleaving repeatable without a sleep. AFTER omits that extra meeting point and retains only a starting meeting point before any lock is held. Students do not implement either gate. Removing the extra gate alone would not repair opposing lock order.

## Source alignment
The two-lock scenario and common acquisition-order repair follow OSTEP Chapter 32, Section 32.3 (Figure 32.6 and the circular-wait prevention discussion). The controlled gates, logging, completion counter, and run script are classroom additions, not verbatim textbook programs.

- OSTEP: https://pages.cs.wisc.edu/~remzi/OSTEP/threads-bugs.pdf
- POSIX barrier contract: https://man7.org/linux/man-pages/man3/pthread_barrier_wait.3p.html
- POSIX mutex contract: https://man7.org/linux/man-pages/man3/pthread_mutex_lock.3p.html
- GNU timeout manual: https://man7.org/linux/man-pages/man1/timeout.1.html
