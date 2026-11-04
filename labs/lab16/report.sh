#!/usr/bin/env bash
report_title='Practice log report'
log_file='service.log'
report_file='session report.txt'
current_user=$(whoami)
line_count=$(wc -l < "$log_file")
printf '%s\n' "$report_title" > "$report_file"
printf 'User: %s\n' "$current_user" >> "$report_file"
printf 'Log lines: %s\n' "$line_count" >> "$report_file"
printf 'Saved: %s\n' "$report_file"
