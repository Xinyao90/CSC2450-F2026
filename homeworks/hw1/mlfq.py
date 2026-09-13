#!/usr/bin/env python3
"""CSC-2450 MLFQ simulator.

It supports multiple queues, per-queue quanta/allotments, I/O, priority
boosts, the older stay-after-I/O rule (-S), and I/O front-of-queue (-I).
"""

import argparse
import random
from collections import deque, defaultdict


def int_list(text):
    return [int(x.strip()) for x in text.split(",") if x.strip()]


def parse_args():
    p = argparse.ArgumentParser(description="Simulate a Multi-Level Feedback Queue scheduler")
    p.add_argument("-s", "--seed", type=int, default=0, help="random seed")
    p.add_argument("-n", "--numQueues", type=int, default=3, help="number of queues")
    p.add_argument("-q", "--quantum", type=int, default=10, help="same quantum for every queue")
    p.add_argument("-Q", "--quantumList", default="", help="quanta high-to-low, e.g. 5,10,20")
    p.add_argument("-a", "--allotment", type=int, default=1, help="number of quanta allowed at each level")
    p.add_argument("-A", "--allotmentList", default="", help="allotments high-to-low, e.g. 1,2,4")
    p.add_argument("-j", "--numJobs", type=int, default=3, help="number of random jobs")
    p.add_argument("-m", "--maxlen", type=int, default=100, help="maximum random runtime")
    p.add_argument("-M", "--maxio", type=int, default=10, help="maximum random I/O frequency; 0 disables I/O")
    p.add_argument("-B", "--boost", type=int, default=0, help="boost all jobs every N ticks; 0 disables")
    p.add_argument("-i", "--iotime", type=int, default=5, help="fixed I/O duration")
    p.add_argument("-S", "--stay", action="store_true", help="old rule: after I/O, stay/reset at same priority")
    p.add_argument("-I", "--iobump", action="store_true", help="put I/O-completed job at front of its queue")
    p.add_argument("-l", "--jlist", default="", help="jobs as start,runtime,ioFreq:start,runtime,ioFreq")
    p.add_argument("-c", "--solve", action="store_true", help="show execution trace and answers")
    return p.parse_args()


def build_levels(args):
    if args.quantumList:
        q_high_to_low = int_list(args.quantumList)
        n = len(q_high_to_low)
    else:
        n = args.numQueues
        q_high_to_low = [args.quantum] * n

    if n < 1 or any(q <= 0 for q in q_high_to_low):
        raise ValueError("queues and quantum values must be positive")

    if args.allotmentList:
        a_high_to_low = int_list(args.allotmentList)
        if len(a_high_to_low) != n:
            raise ValueError("-A must have the same number of entries as queues")
    else:
        a_high_to_low = [args.allotment] * n

    if any(a <= 0 for a in a_high_to_low):
        raise ValueError("allotments must be positive")

    # Internal priorities: 0 = lowest, n-1 = highest.
    quantum = {n - 1 - i: q for i, q in enumerate(q_high_to_low)}
    allot = {n - 1 - i: a for i, a in enumerate(a_high_to_low)}
    return n, quantum, allot


def make_jobs(args):
    jobs = []
    if args.jlist:
        specs = args.jlist.split(":")
        for jid, spec in enumerate(specs):
            parts = [int(x.strip()) for x in spec.split(",")]
            if len(parts) != 3:
                raise ValueError("Each -l job must be start,runtime,ioFreq")
            start, runtime, io_freq = parts
            jobs.append({"id": jid, "start": start, "runtime": runtime, "io_freq": io_freq})
    else:
        random.seed(args.seed)
        for jid in range(args.numJobs):
            runtime = random.randint(1, max(1, args.maxlen))
            io_freq = 0 if args.maxio <= 0 else random.randint(0, args.maxio)
            jobs.append({"id": jid, "start": 0, "runtime": runtime, "io_freq": io_freq})
    return jobs


def print_problem(args, jobs, n, quantum, allot):
    print("OPTIONS")
    print(f"  jobs: {len(jobs)}")
    print(f"  queues: {n}")
    for p in range(n - 1, -1, -1):
        print(f"  priority {p}: quantum={quantum[p]} allotment={allot[p]} quantum(s)")
    print(f"  boost: {args.boost}")
    print(f"  ioTime: {args.iotime}")
    print(f"  stayAfterIO: {args.stay}")
    print(f"  ioBumpFront: {args.iobump}")

    print("\nJob List:")
    for j in jobs:
        print(f"  Job {j['id']}: startTime={j['start']} runTime={j['runtime']} ioFreq={j['io_freq']}")


def simulate(args, jobs, n, quantum, allot):
    highest = n - 1
    ready = {p: deque() for p in range(n)}
    io_done = defaultdict(list)
    arrivals = defaultdict(list)
    for j in jobs:
        arrivals[j["start"]].append(j["id"])

    state = {}
    for j in jobs:
        state[j["id"]] = {
            **j,
            "remaining": j["runtime"],
            "priority": highest,
            "ticks_left": quantum[highest],
            "allot_left": allot[highest],
            "cpu_since_io": 0,
            "response": None,
            "finish": None,
            "blocked": False,
            "done": False,
        }

    trace = []
    time = 0
    finished = 0

    def enqueue(jid, front=False):
        p = state[jid]["priority"]
        if front:
            ready[p].appendleft(jid)
        else:
            ready[p].append(jid)

    while finished < len(jobs):
        # Periodic priority boost.
        if args.boost > 0 and time > 0 and time % args.boost == 0:
            collected = []
            for p in range(n):
                while ready[p]:
                    collected.append(ready[p].popleft())
            for jid, st in state.items():
                if not st["done"]:
                    st["priority"] = highest
                    st["ticks_left"] = quantum[highest]
                    st["allot_left"] = allot[highest]
            for jid in collected:
                ready[highest].append(jid)
            trace.append(f"[ time {time} ] PRIORITY BOOST")

        # New arrivals.
        for jid in arrivals.get(time, []):
            enqueue(jid)
            trace.append(f"[ time {time} ] JOB {jid} BEGINS at PRIORITY {highest}")

        # I/O completions.
        for jid in io_done.get(time, []):
            st = state[jid]
            st["blocked"] = False
            enqueue(jid, front=args.iobump)
            trace.append(f"[ time {time} ] IO DONE for JOB {jid}; ready at PRIORITY {st['priority']}")

        # Choose the highest non-empty ready queue.
        p = None
        for candidate in range(highest, -1, -1):
            if ready[candidate]:
                p = candidate
                break

        if p is None:
            trace.append(f"[ time {time} ] IDLE")
            time += 1
            continue

        jid = ready[p].popleft()
        st = state[jid]
        if st["response"] is None:
            st["response"] = time - st["start"]

        # Run exactly one tick.
        st["remaining"] -= 1
        st["ticks_left"] -= 1
        st["cpu_since_io"] += 1
        trace.append(
            f"[ time {time} ] Run JOB {jid} at PRIORITY {p} "
            f"[ ticksLeft={st['ticks_left']} allotLeft={st['allot_left']} remaining={st['remaining']} ]"
        )
        time += 1

        # Job completes.
        if st["remaining"] == 0:
            st["done"] = True
            st["finish"] = time
            finished += 1
            trace.append(f"[ time {time} ] JOB {jid} DONE")
            continue

        # Job requests I/O.
        if st["io_freq"] > 0 and st["cpu_since_io"] >= st["io_freq"]:
            st["cpu_since_io"] = 0
            st["blocked"] = True
            if args.stay:
                # Older Rules 4a/4b: return with a fresh time slice/allotment.
                st["ticks_left"] = quantum[st["priority"]]
                st["allot_left"] = allot[st["priority"]]
            done_at = time + args.iotime
            if args.iotime == 0:
                st["blocked"] = False
                enqueue(jid, front=args.iobump)
                trace.append(f"[ time {time} ] JOB {jid} IO_START and IO_DONE immediately")
            else:
                io_done[done_at].append(jid)
                trace.append(f"[ time {time} ] JOB {jid} IO_START; completes at {done_at}")
            continue

        # Quantum expires.
        if st["ticks_left"] == 0:
            st["allot_left"] -= 1
            if st["allot_left"] == 0 and st["priority"] > 0:
                st["priority"] -= 1
                st["allot_left"] = allot[st["priority"]]
                st["ticks_left"] = quantum[st["priority"]]
                trace.append(f"[ time {time} ] JOB {jid} moves DOWN to PRIORITY {st['priority']}")
            else:
                st["ticks_left"] = quantum[st["priority"]]
                if st["allot_left"] == 0:  # lowest queue: remain there
                    st["allot_left"] = allot[st["priority"]]
            enqueue(jid)
        else:
            # Continue same quantum next tick unless a higher-priority job appears.
            ready[st["priority"]].appendleft(jid)

    return trace, state, time


def print_solution(trace, state, jobs):
    print("\nExecution Trace:")
    for line in trace:
        print(" ", line)

    print("\nFinal statistics:")
    total_r = total_t = 0.0
    for j in jobs:
        st = state[j["id"]]
        response = st["response"] if st["response"] is not None else 0
        turnaround = st["finish"] - st["start"]
        total_r += response
        total_t += turnaround
        print(f"  Job {j['id']}: response={response} turnaround={turnaround}")

    n = len(jobs)
    print(f"\n  Average: response={total_r/n:.2f} turnaround={total_t/n:.2f}")


def main():
    args = parse_args()
    try:
        n, quantum, allot = build_levels(args)
        jobs = make_jobs(args)
    except ValueError as e:
        raise SystemExit(f"Error: {e}")

    print_problem(args, jobs, n, quantum, allot)

    if not args.solve:
        print("\nCompute the execution trace yourself.")
        print("Then run the same command again with -c to check your work.")
        return

    trace, state, _ = simulate(args, jobs, n, quantum, allot)
    print_solution(trace, state, jobs)


if __name__ == "__main__":
    main()

