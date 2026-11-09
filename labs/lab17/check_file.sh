#!/usr/bin/env bash

if [ "$#" -ne 1 ]; then
  printf 'Usage: %s PATH\n' "$0" >&2
  exit 2
fi

file=$1

if [ ! -f "$file" ]; then
  printf 'ERROR: not a regular file: %s\n' "$file" >&2
  exit 2
elif [ ! -r "$file" ]; then
  printf 'ERROR: cannot read: %s\n' "$file" >&2
  exit 2
elif [ ! -s "$file" ]; then
  printf 'EMPTY: %s\n' "$file"
  exit 1
else
  printf 'READY: %s\n' "$file"
  exit 0
fi
