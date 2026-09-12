jobs = [
    {"name": "A", "arrival": 0, "runtime": 6},
    {"name": "B", "arrival": 0, "runtime": 3},
    {"name": "C", "arrival": 0, "runtime": 1},
    {"name": "D", "arrival": 0, "runtime": 2},
]


def sjf(jobs):
    time = 0
    result = []

    # Shortest runtime first
    sorted_jobs = sorted(jobs, key=lambda job: job["runtime"])

    for job in sorted_jobs:
        start = max(time, job["arrival"])
        finish = start + job["runtime"]

        result.append((job["name"], start, finish))

        time = finish

    return result


print(sjf(jobs))
