# safer_pressure.py
# Start small on the class server.
# Stop with Ctrl-C if the system becomes slow.

import os
import time

MB = 1024 * 1024

CHUNK_MB = 64
ROUNDS = 8

chunks = []

print("PID:", os.getpid())

# Gives you time to open another terminal
# and start vmstat, free, or pmap.
time.sleep(5)

for i in range(ROUNDS):

    # Allocate 64 MB
    block = bytearray(CHUNK_MB * MB)

    # Touch one byte in every 4 KiB page
    # so the pages become resident in physical memory.
    for j in range(0, CHUNK_MB * MB, 4096):
        block[j] = 1

    # Keep the block alive.
    chunks.append(block)

    print(
        "allocated and touched",
        (i + 1) * CHUNK_MB,
        "MB"
    )

    time.sleep(5)

print("holding memory for observation")
print("Press Ctrl-C to stop.")

time.sleep(120)
