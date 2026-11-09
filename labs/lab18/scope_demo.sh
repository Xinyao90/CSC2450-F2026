#!/usr/bin/env bash
target=outside
show_target() {
  local target="$1"
  printf 'Inside: %s\n' "$target"
}
show_target "weekly notes.txt"
printf 'Outside: %s\n' "$target"
