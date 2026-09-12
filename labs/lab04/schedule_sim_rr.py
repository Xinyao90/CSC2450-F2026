jobs = [
    {"name": "A", "arrival": 0, "runtime": 6},
    {"name": "B", "arrival": 0, "runtime": 3},
    {"name": "C", "arrival": 0, "runtime": 1},
    {"name": "D", "arrival": 0, "runtime": 2},
]


def round_robin(jobs, quantum):
    time = 0
    result = []

    # Keep track of remaining runtime
    queue = []

    for job in jobs:
        queue.append({
            "name": job["name"],
            "remaining": job["runtime"]
        })

    while queue:
        job = queue.pop(0)

        start = time

        run_time = min(quantum, job["remaining"])

        time = time + run_time
        job["remaining"] = job["remaining"] - run_time

        result.append((job["name"], start, time))

        # If job is not finished, put it back in the queue
        if job["remaining"] > 0:
            queue.append(job)

    return result


print(round_robin(jobs, 2))
