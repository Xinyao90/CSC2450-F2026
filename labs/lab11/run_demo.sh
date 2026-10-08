#!/usr/bin/env bash
# Run seven bounded tests and save their actual output to results.txt.
# This script contains no programming task for students.
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
if ! command -v timeout >/dev/null 2>&1; then
    echo "This script needs Linux timeout. Use the Linux class server." >&2
    exit 1
fi
for program in buffer_cv buffer_one buffer_sem; do
    if [[ ! -x "./$program" ]]; then
        echo "Missing $program. Run: bash build.sh" >&2
        exit 1
    fi
done
if [[ -e results.txt ]]; then
    backup=$(mktemp results.previous.XXXXXX.txt)
    cp -- results.txt "$backup"
    echo "Previous evidence kept in $backup."
fi
failed=0
run_case() {
    local label=$1 program=$2 rc
    printf '\n=== %s ===\n' "$label"
    printf '$ timeout 10s ./%s\n' "$program"
    if timeout 10s "./$program"; then
        rc=0
    else
        rc=$?
        failed=$((failed + 1))
    fi
    printf 'Exit status: %s\n' "$rc"
    if [[ "$rc" -eq 124 ]]; then
        echo 'TIME LIMIT reached. Keep this output and ask the instructor; do not edit the source.'
    elif [[ "$rc" -ne 0 ]]; then
        echo 'UNEXPECTED RESULT. Keep this output and ask the instructor.'
    fi
}
{
    printf 'Lab 11 - actual execution evidence\n'
    printf 'User: %s\n' "${USER:-unknown}"
    printf 'Time: %s\n' "$(date -Iseconds)"
    for trial in 1 2 3 4 5; do
        run_case "CV capacity 4, trial $trial" buffer_cv
    done
    run_case 'CV capacity 1, trial 6' buffer_one
    run_case 'Semaphore capacity 4, trial 7' buffer_sem
    printf '\nCompleted seven tests; nonzero exits: %s\n' "$failed"
    if [[ "$failed" -ne 0 ]]; then
        exit 1
    fi
} 2>&1 | tee results.txt
