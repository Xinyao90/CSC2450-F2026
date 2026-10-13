#!/usr/bin/env bash
# Lab 12: build and run both COMPLETE programs, once each.
# No source editing, sudo, or background jobs are needed.
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"

for tool in gcc timeout; do
    if ! command -v "$tool" >/dev/null 2>&1; then
        printf 'Missing %s. Use the Linux class server; ask the instructor.\n' "$tool" >&2
        exit 1
    fi
done

printf 'Lab 12 | Deadlock: before and after\n'
printf 'Building the two complete supplied programs...\n'
gcc -std=c11 -O0 -Wall -Wextra -pthread deadlock_before.c -o deadlock_before
gcc -std=c11 -O0 -Wall -Wextra -pthread deadlock_after.c -o deadlock_after

# New directory per run: previous evidence is not overwritten.
log_dir=$(mktemp -d run_output.XXXXXX)
printf '\nBEFORE: running with a 5-second limit. Please wait.\n'
status=0
timeout --kill-after=1s 5s ./deadlock_before > "$log_dir/before.txt" 2>&1 || status=$?
cat "$log_dir/before.txt"
printf 'BEFORE exit status: %s\n' "$status" | tee -a "$log_dir/before.txt"

# A timeout by itself is not proof of deadlock: also require both
# ownership/request messages from the controlled demonstration.
if [[ "$status" -ne 124 ]] ||
   ! grep -Fq 'A holds L1' "$log_dir/before.txt" ||
   ! grep -Fq 'B holds L2' "$log_dir/before.txt" ||
   ! grep -Fq 'A requests L2 (still holds L1)' "$log_dir/before.txt" ||
   ! grep -Fq 'B requests L1 (still holds L2)' "$log_dir/before.txt" ||
   grep -Fq 'completed protected work' "$log_dir/before.txt"; then
    printf 'Unexpected result. Keep the output and ask the instructor; do not edit C.\n' >&2
    exit 1
fi
printf 'Time limit ended the BEFORE process; it did not repair the locks.\n'

printf '\nAFTER: running with a 5-second safety limit.\n'
status=0
timeout --kill-after=1s 5s ./deadlock_after > "$log_dir/after.txt" 2>&1 || status=$?
cat "$log_dir/after.txt"
printf 'AFTER exit status: %s\n' "$status" | tee -a "$log_dir/after.txt"
if [[ "$status" -ne 0 ]] ||
   ! grep -Fq 'A completed protected work' "$log_dir/after.txt" ||
   ! grep -Fq 'B completed protected work' "$log_dir/after.txt" ||
   ! grep -Fq 'PASS: 2 workers completed' "$log_dir/after.txt"; then
    printf 'Unexpected result. Keep the output and ask the instructor; do not edit C.\n' >&2
    exit 1
fi

printf '\nOutputs saved in %s/\n' "$log_dir"
printf 'Submit a screenshot showing BOTH runs and answer the THREE questions.\n'
