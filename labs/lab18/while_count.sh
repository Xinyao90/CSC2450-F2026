#!/usr/bin/env bash
# The test runs before each iteration.
count=1
while [ "$count" -le 3 ]; do
  printf 'Pass %d\n' "$count"
  count=$((count + 1))
done
printf 'After loop: count=%d\n' "$count"
