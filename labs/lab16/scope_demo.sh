#!/usr/bin/env bash
printf 'Child received: <%s>\n' "$course_label"
course_label='Changed inside script'
printf 'Child now has: <%s>\n' "$course_label"
