# Lab 11 — One-Slot Buffer: Observe and Explain

CSC 2450 · Operating Systems Administration  
**Time: about 10 minutes. No C writing or editing.**

## Run once (2 minutes)

Extract this package into your own workspace on the Linux class server. Then run:

```bash
cd lab11_brief
bash run_demo.sh
```

The script compiles and runs ONE complete demonstration. It uses two producers,
two consumers, and a buffer with capacity ONE. Each producer supplies 12 real
items. This is the previous lab's completed condition-variable program, now used
only for one observation; no synchronization implementation is assigned.

## Observe (3 minutes)

Read the four displayed PUT/GET lines and the final summary. PUT inserts an item;
GET removes it. `count` is the number of items currently in the buffer AFTER
that operation. The first four lines are an excerpt, not the whole execution.
Item IDs and the schedule may vary; a different result is NOT required.
The complete output is saved automatically, but you do not need to submit it.

## Answer (5 minutes)

1. Copy the final values: produced = ___; consumed = ___; remaining = ___.
2. When the one-slot buffer is FULL, which side must wait before its next buffer
   operation: producer or consumer? When it is EMPTY, which side must wait?
3. Consumer C1 is signaled because an item is available. Before C1 resumes,
   consumer C2 removes that only item. Should C1 consume immediately or recheck
   and wait if the buffer is empty? Explain in one sentence.

## Submit

**ONE terminal screenshot** showing the displayed excerpt and final summary,
plus **answers to the three questions** in the worksheet or Brightspace text box.
No C source, executables, full logs, repeated trials, or long trace tables.
If a command fails, keep the message and ask the instructor; do not edit C.

The repeated runs, capacity-four comparison, semaphore experiment, and full
textbook-trace analysis are not part of this brief in-class lab.

## Reading basis

Lecture 11: one-slot predicates; the two-consumer wakeup example; recheck with
while (slides titled "Begin with one slot and two predicates", "Why if is unsafe
after a notification", and "Use while because the predicate is the authority").
The wakeup scenario restates the lecture's Figure 30.9 discussion. The workload,
finite shutdown, and validation are supplied classroom demonstrations, not extra
textbook requirements.
