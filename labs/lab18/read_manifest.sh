#!/usr/bin/env bash
# Run from this folder. The supplied manifest ends every line with LF.
line_number=0
while IFS= read -r target; do
  line_number=$((line_number + 1))
  printf '%d: <%s>\n' "$line_number" "$target"
done < manifest.txt
printf 'Lines read: %d\n' "$line_number"
