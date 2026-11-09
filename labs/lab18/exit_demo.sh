#!/usr/bin/env bash
report_issue() {
  printf 'Inside function\n'
  exit 1
  printf 'Unreachable inside function\n'
}
report_issue
result=$?
printf 'After function; status=%d\n' "$result"
exit 0
