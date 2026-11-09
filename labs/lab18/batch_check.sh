#!/usr/bin/env bash
# Read-only checks. A usable input is regular, readable, and nonempty.
check_file() {
  local target="$1"
  if [ ! -f "$target" ]; then
    printf 'PROBLEM: %s (not a regular file)\n' "$target"
    return 1
  fi
  if [ ! -r "$target" ]; then
    printf 'PROBLEM: %s (not readable)\n' "$target"
    return 1
  fi
  if [ ! -s "$target" ]; then
    printf 'PROBLEM: %s (empty)\n' "$target"
    return 1
  fi
  printf 'OK: %s\n' "$target"
  return 0
}

if [ "$#" -eq 0 ]; then
  printf 'Usage: %s FILE [FILE ...]\n' "$0" >&2
  exit 2
fi

ready=0
problems=0
for target in "$@"; do
  if check_file "$target"; then
    ready=$((ready + 1))
  else
    problems=$((problems + 1))
  fi
done
printf 'Ready: %d; problems: %d\n' "$ready" "$problems"

if [ "$problems" -gt 0 ]; then
  exit 1
fi
exit 0
