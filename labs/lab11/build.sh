#!/usr/bin/env bash
# Build all complete supplied demonstrations. Do not edit the C files.
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
if ! command -v gcc >/dev/null 2>&1; then
    echo "GCC is not available. Use the Linux class server or ask the instructor." >&2
    exit 1
fi
flags=(-std=c11 -O0 -Wall -Wextra -pthread)
build() {
    printf '\nBuilding:'
    printf ' %q' gcc "${flags[@]}" "$@"
    printf '\n'
    gcc "${flags[@]}" "$@"
}
build demos/bounded_buffer_cv.c -o buffer_cv
build -DCAPACITY=1 demos/bounded_buffer_cv.c -o buffer_one
build demos/bounded_buffer_sem.c -o buffer_sem
printf '\nReady: buffer_cv (capacity 4), buffer_one (capacity 1), buffer_sem (capacity 4).\n'
printf 'Next: bash run_tests.sh\n'
