#!/usr/bin/env bash
# Complete supplied demonstration: no source editing is required.
# Build one program, run it ONCE, and display a small excerpt of its real output.
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
for tool in gcc timeout; do
    if ! command -v "$tool" >/dev/null 2>&1; then
        printf 'Missing %s. Use the Linux class server and ask the instructor.\n' "$tool" >&2
        exit 1
    fi
done
if [[ ! -f demos/bounded_buffer_cv.c ]]; then
    echo 'Missing supplied source. Extract the entire lab11_brief folder; do not edit the code.' >&2
    exit 1
fi
printf 'Lab 11 | One-slot producer-consumer observation\n'
printf 'Preparing the complete supplied demonstration...\n'
gcc -std=c11 -O0 -Wall -Wextra -pthread -DCAPACITY=1 \
    demos/bounded_buffer_cv.c -o buffer_one
if [[ -e demo_output.txt ]]; then
    backup=$(mktemp demo_output.previous.XXXXXX.txt)
    cp -- demo_output.txt "$backup"
    printf 'Previous run saved as %s\n' "$backup"
fi
printf 'Running once (10-second limit).\n'
rc=0
timeout 10s ./buffer_one --trace > demo_output.txt 2>&1 || rc=$?
if [[ "$rc" -ne 0 ]]; then
    cat demo_output.txt
    printf '\nRun did not complete successfully (exit %s).\n' "$rc" >&2
    printf 'Keep the output and ask the instructor; do not change C code.\n' >&2
    exit "$rc"
fi
printf '\nFirst four queue operations (excerpt; count is AFTER each operation):\n'
head -n 4 demo_output.txt
printf '\nFinal summary (after all workers finish):\n'
# Select actual summary lines; do not replace results with expected values.
grep -E '^(capacity=|produced=|PASS:|FAIL:)' demo_output.txt
printf '\nFull output saved in demo_output.txt; no full-log submission is required.\n'
printf 'Submit ONE screenshot of this screen and your THREE short answers.\n'
