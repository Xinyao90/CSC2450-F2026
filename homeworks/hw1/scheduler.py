#!/usr/bin/env python3
"""CSC-2450 CPU scheduling simulator.
Supports FIFO, SJF, and Round Robin (RR).
"""

import argparse
import random
from collections import deque


def parse_args():
    p = argparse.ArgumentParser(description="Simulate FIFO, SJF, or RR CPU scheduling")
    p.add_argument("-s", "--seed", type=int, default=0, help="random seed")
    p.add_argument("-j", "--jobs", type=int, default=3, help="number of random jobs")
    p.add_argument("-l", "--jlist", default="", help="comma-separated job lengths, e.g. 5,10,15")
    p.add_argument("-m", "--maxlen", type=int, default=10, help="maximum random job length")
    p.add_argument("-p", "--policy", default="FIFO", choices=["FIFO", "SJF", "RR"], help="scheduling policy")
    p.add_argument("-q", "--quantum", type=float, default=1, help="RR time quantum")
    p.add_argument("-c", "--solve", action="store_true", help="show execution trace and answers")
    return p.parse_args()


def make_jobs(args):
    if args.jlist:
        lengths = [float(x.strip()) for x in args.jlist.split(",") if x.strip()]
    else:
        random.seed(args.seed)
        lengths = [float(random.randint(1, args.maxlen)) for _ in range(args.jobs)]
    return [{"id": i, "runtime": t} for i, t in enumerate(lengths)]


def show_problem(args, jobs):
    print(f"ARG policy {args.policy}")
    if args.policy == "RR":
        print(f"ARG quantum {args.quantum:g}")
    print("\nJob List:")
    for j in jobs:
        print(f"  Job {j['id']}: length = {j['runtime']:g}")


def simulate_fifo_or_sjf(jobs, policy):
    order = list(jobs)
    if policy == "SJF":
        order.sort(key=lambda j: (j["runtime"], j["id"]))

    time = 0.0
    trace = []
    stats = {}

    for j in order:
        start = time
        finish = start + j["runtime"]
        response = start
        turnaround = finish
        wait = start
        trace.append((start, finish, j["id"]))
        stats[j["id"]] = (response, turnaround, wait)
        time = finish

    return trace, stats


def simulate_rr(jobs, quantum):
    if quantum <= 0:
        raise ValueError("quantum must be greater than 0")

    q = deque({"id": j["id"], "remaining": j["runtime"], "runtime": j["runtime"]} for j in jobs)
    first_start = {j["id"]: None for j in jobs}
    finish = {}
    time = 0.0
    trace = []

    while q:
        j = q.popleft()
        if first_start[j["id"]] is None:
            first_start[j["id"]] = time

        run_for = min(quantum, j["remaining"])
        start = time
        time += run_for
        j["remaining"] -= run_for
        trace.append((start, time, j["id"]))

        if j["remaining"] > 1e-12:
            q.append(j)
        else:
            finish[j["id"]] = time

    stats = {}
    for j in jobs:
        jid = j["id"]
        response = first_start[jid]
        turnaround = finish[jid]
        wait = turnaround - j["runtime"]
        stats[jid] = (response, turnaround, wait)

    return trace, stats


def print_solution(jobs, trace, stats):
    print("\nExecution Trace:")
    for start, finish, jid in trace:
        print(f"  time {start:g} -> {finish:g}: Job {jid}")

    print("\nFinal statistics:")
    total_r = total_t = total_w = 0.0
    for j in jobs:
        r, t, w = stats[j["id"]]
        total_r += r
        total_t += t
        total_w += w
        print(f"  Job {j['id']}: Response {r:.2f}  Turnaround {t:.2f}  Wait {w:.2f}")

    n = len(jobs)
    print(f"\n  Average: Response {total_r/n:.2f}  Turnaround {total_t/n:.2f}  Wait {total_w/n:.2f}")


def main():
    args = parse_args()
    jobs = make_jobs(args)
    show_problem(args, jobs)

    if not args.solve:
        print("\nCompute response, turnaround, and waiting time yourself.")
        print("Then run the same command again with -c to check your work.")
        return

    if args.policy in ("FIFO", "SJF"):
        trace, stats = simulate_fifo_or_sjf(jobs, args.policy)
    else:
        trace, stats = simulate_rr(jobs, args.quantum)

    print_solution(jobs, trace, stats)


if __name__ == "__main__":
    main()

