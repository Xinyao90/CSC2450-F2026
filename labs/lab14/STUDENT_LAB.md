# Lab 14 — Inspect, select, recover

Work only in your own workspace. Do not use sudo or change storage/network configuration.

## Setup
```bash
bash ~/CSC2450-F2026/labs/lab14/setup.sh
cd ~/csc2450-work/labs/lab14
pwd
```
The instructor must publish the files first. If this workspace exists, choose a new path under your home as setup.sh's optional argument; do not delete prior work.

## A. Observe
Run `dpkg -s bash` and `mount`. Record the package Status and Version; select one mount line and identify device, mount point, filesystem type. If unavailable, read samples/package.txt and samples/mount.txt, labeling your work as sample-based.

## B. Predict and search
Predict the number of log files, empty files, and directories, then run:
```bash
find playground -type f -name '*.log' -print
find playground -type f -empty -print
find playground -type d -print
```
Write and run a command selecting only .txt regular files. Explain the quotes around the wildcard. Results need not be in a particular order.

## C. Archive and recover
```bash
tar -czf practice.tar.gz playground
tar -tzf practice.tar.gz
mkdir restored
tar -xzf practice.tar.gz -C restored
diff -r playground restored/playground
printf 'comparison exit status: %s\n' "$?"
```
The status command must immediately follow diff. A clean content comparison has no differences and status 0. Use a fresh restore directory for another attempt.

## Submit
Two screenshots: (1) inspection/search evidence, (2) archive/restoration/comparison evidence. Three explanations: why quote '*.log'; why list the archive; why use a fresh restore destination. A same-machine practice archive does not protect against loss of the whole server.

## Optional
If rsync is already available: `mkdir mirror`; `rsync -avn playground/ mirror/`; inspect the preview before `rsync -av playground/ mirror/`. Explain the source slash. Do not add --delete.
