jobs = [
    {"name": "A", "arrival": 0, "runtime": 6},
    {"name": "B", "arrival": 0, "runtime": 3},
    {"name": "C", "arrival": 0, "runtime": 1},
    {"name": "D", "arrival": 0, "runtime": 2},
]


def fcfs(jobs):
    time = 0
    result = []

    for job in jobs:
        start = max(time, job["arrival"])
        finish = start + job["runtime"]

        result.append((job["name"], start, finish))

        time = finish

    return result


print(fcfs(jobs))
