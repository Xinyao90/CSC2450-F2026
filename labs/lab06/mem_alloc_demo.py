# mem_alloc_demo.py
import mmap, os, time

MB = 1024 * 1024
SIZE = 512 * MB
PAGE = os.sysconf("SC_PAGE_SIZE")

def show(label):
    print("
---", label, "pid", os.getpid(), "---")
    with open(f"/proc/{os.getpid()}/status") as f:
        for line in f:
            if line.startswith(("VmSize", "VmRSS", "VmData")):
                print(line.strip())

show("start")
buf = mmap.mmap(-1, SIZE)
show("after mmap reservation")
time.sleep(20)

for i in range(0, SIZE, PAGE):
    buf[i:i+1] = b"x"
show("after touching each page")
time.sleep(60)

