#!/usr/bin/env bash
# Print each supplied argument as one item.
for target in "$@"; do
  printf 'Item: <%s>\n' "$target"
done
