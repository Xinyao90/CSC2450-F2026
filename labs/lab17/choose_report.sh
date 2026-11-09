#!/usr/bin/env bash

if [ "$#" -gt 1 ]; then
  printf 'Usage: %s [disk|memory|help]\n' "$0" >&2
  exit 2
fi

topic=${1:-help}
case "$topic" in
  disk) df -h . ;;
  memory) free -h ;;
  help) printf 'Choices: disk or memory\n' ;;
  *) printf 'Unknown choice: %s\n' "$topic" >&2
     exit 2 ;;
esac
