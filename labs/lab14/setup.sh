#!/usr/bin/env bash
# Copy supplied data to a NEW student-owned workspace. Does not install anything.
set -euo pipefail
if (( $# > 1 )); then
  printf 'Usage: bash %s [NEW_WORKSPACE_UNDER_HOME]\n' "$0" >&2
  exit 2
fi
src="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)/data"
dest="${1:-$HOME/csc2450-work/labs/lab14}"
# Resolve parent symlinks as well as .. components before checking the boundary.
home_real="$(realpath -- "$HOME")"
dest_real="$(realpath -m -- "$dest")"
case "$dest_real" in
  "$home_real"/*) ;;
  *) printf 'Choose a new destination inside your home directory.\n' >&2; exit 2 ;;
esac
if [[ -e "$dest_real" || -L "$dest_real" ]]; then
  printf 'Refusing to overwrite existing workspace: %s\n' "$dest_real" >&2
  printf 'Choose a new destination as the optional argument.\n' >&2
  exit 2
fi
mkdir -p -- "$(dirname -- "$dest_real")"
mkdir -- "$dest_real"
cp -R -- "$src/." "$dest_real/"
printf 'Workspace ready: %s\n' "$dest_real"
printf 'Next: cd -- "%s"\n' "$dest_real"
