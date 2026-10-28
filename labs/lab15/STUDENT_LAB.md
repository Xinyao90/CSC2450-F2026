# Lab 15 — A verified service report

All records are synthetic. No printer, external network, sudo, or C implementation is required.

## Setup
```bash
bash ~/CSC2450-F2026/labs/lab15/setup.sh
cd ~/csc2450-work/labs/lab15
export LC_ALL=C
cat -n events.txt
cat names.txt
```
Use a new destination under your home if the default already exists. The locale setting is for this shell session, not your permanent shell configuration.

## A. Predict and test
Write expected matches before running:
```bash
grep '^zip' names.txt
grep 'zip$' names.txt
grep -E '^.zip$' names.txt
grep -n '^ERROR:' events.txt
```
Explain one pattern in ordinary language.

## B. Count by service
```bash
grep '^ERROR:' events.txt > errors.txt
cut -d ':' -f2 errors.txt | sort | uniq -c | sort -nr > counts.txt
cat counts.txt
grep -c '^ERROR:' events.txt
```
Add the group counts by hand and compare to the independently selected record count. This counts records, not distinct message strings.

## C. Transform and format
```bash
sed 's/timeout/TIMEOUT/g' errors.txt > normalized.txt
diff -u errors.txt normalized.txt
printf '%s\n' 'ERROR RECORDS BY SERVICE' > report.txt
printf '%s\n' 'COUNT SERVICE' >> report.txt
cat counts.txt >> report.txt
nl -ba report.txt
```
Keep the source input unchanged. diff is expected to report intentional differences; that is not a crash.

## Optional supplied build
Read hello-project/README and INSTALL. In that directory run make, ./hello, make again, then sleep 1; touch hello.c; make. Explain the rebuild. No configure script or install target is provided. If tools are unavailable, read ../samples/build.txt from hello-project (or samples/build.txt from the lab workspace) and label the limitation.

## Submit
Two screenshots: (1) pattern checks, (2) counts/total check/diff/report. Explain anchors, sort before uniq, and why sed did not edit the source. Include a brief build observation only if attempting the optional part.
