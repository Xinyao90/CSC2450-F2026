#!/usr/bin/env bash
report_label='Class report'
printf 'Without double quotes:\n'
# Deliberately unquoted here so we can observe word splitting.
printf '<%s>\n' $report_label
printf 'With double quotes:\n'
printf '<%s>\n' "$report_label"
printf 'Literal text: %s\n' '$report_label'
