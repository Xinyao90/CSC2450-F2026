import os
import time

print("Memory Allocation Demo")
print("----------------------")
print("PID:", os.getpid())

input("\nPress Enter to start...")

chunks = []

# Allocate memory in steps
for i in range(5):
    print(f"\nStep {i + 1}: allocating 100 MB...")

    # Allocate 100 MB and touch the memory
    block = bytearray(100 * 1024 * 1024)

    # Touch one byte on each 4 KB page
    # so physical memory is actually committed
    for j in range(0, len(block), 4096):
        block[j] = 1

    chunks.append(block)

    print(f"Total allocated: {(i + 1) * 100} MB")
    print("Check memory usage now.")
    print(f"Try: pmap -x {os.getpid()} | tail")
    print(f"Or:  ps -o pid,vsz,rss,cmd -p {os.getpid()}")

    input("Press Enter to allocate another 100 MB...")

print("\nFinished allocating 500 MB.")
print("The memory will stay allocated until the program exits.")

input("Press Enter to release the memory and exit...")

chunks.clear()

print("Memory released.")
