#!/usr/bin/env python3
"""CSC-2450 supplied labs for Lectures 20 and 21.

Run with Python 3; only the standard library is required. Students do not
need to edit this code. `setup` creates a new, tiny Lecture 20 folder.
All other commands only calculate and print teaching models in memory.

The models adapt OSTEP 39.14-39.15, 40.6, and 42.1-42.3:
https://pages.cs.wisc.edu/~remzi/OSTEP/file-intro.pdf
https://pages.cs.wisc.edu/~remzi/OSTEP/file-implementation.pdf
https://pages.cs.wisc.edu/~remzi/OSTEP/file-journaling.pdf

The word "durable" in model output means a simulated completed write.
This tool does not perform or measure real persistence, crash a machine,
read raw devices, or run a filesystem checker. It never calls fsck, mount,
mkfs, sudo, or a shell. The small real files made by setup are separate
from every simulated inode, bitmap, data block, and journal record.
"""

import argparse
from dataclasses import dataclass
from pathlib import Path
import sys


LAB_DIRECTORY = "l20-files-lab"
UPDATE_NAMES = {"I": "I[v2]", "B": "B[v2]", "D": "Db"}
ALL_UPDATES = frozenset(UPDATE_NAMES)
NOTE = (
    "CSC-2450 Lecture 20 lab. foo initially contains hello plus newline.\n"
    "Create bar as a hard link and baz as a symlink to foo.\n"
    "Only unlink the supplied foo entry after recording predictions.\n"
)


@dataclass(frozen=True)
class Snapshot:
    """An immutable home-location snapshot; no file or device is represented."""

    durable: frozenset

    @property
    def inode_version(self):
        return "I[v2]" if "I" in self.durable else "I[v1]"

    @property
    def pointers(self):
        return (4, 5) if "I" in self.durable else (4,)

    @property
    def bitmap(self):
        # Bits are printed left to right for block numbers 0 through 7.
        return "00001100" if "B" in self.durable else "00001000"

    @property
    def block5(self):
        # OLD means unspecified pre-existing bytes, not necessarily zeros.
        return "Db (new bytes)" if "D" in self.durable else "OLD (unspecified bytes)"

    @property
    def metadata_consistent(self):
        # In this intentionally tiny model, agreement concerns block 5.
        # Other real checker invariants are outside the model.
        return ("I" in self.durable) == ("B" in self.durable)

    @property
    def append_visible(self):
        return "I" in self.durable

    @property
    def complete(self):
        return self.durable == ALL_UPDATES


def subset(text):
    """Parse a set of completed model writes, never a pathname or command."""
    if text.lower() == "none":
        return frozenset()
    values = [v.strip().upper() for v in text.split(",")]
    if not values or any(v not in ALL_UPDATES for v in values):
        raise argparse.ArgumentTypeError("use none, I, B, D, or a comma-separated subset such as I,B")
    return frozenset(values)


def update_list(updates):
    return ", ".join(UPDATE_NAMES[x] for x in ("I", "B", "D") if x in updates) or "none"


def interpretation(state):
    """Explain what is observable after the chosen partial append writes."""
    if state.complete:
        return "The append is complete: inode, bitmap, and new data agree."
    if not state.durable:
        return "The old file remains; the append did not become visible."
    if state.durable == frozenset("D"):
        return "The old file remains; Db exists in a free, unreferenced block."
    if "I" in state.durable and "B" not in state.durable:
        if "D" in state.durable:
            return "The inode reaches Db, but the bitmap calls block 5 free."
        return "The inode reaches OLD bytes, and the bitmap calls block 5 free."
    if "B" in state.durable and "I" not in state.durable:
        return "Block 5 is allocated but no inode points to it: a space leak."
    return "Metadata agrees, but the new file block exposes OLD bytes."


def show_state(state, heading="Home locations"):
    print(heading + ":")
    print("  inode 2: {} size={} block(s), pointers={}".format(
        state.inode_version, len(state.pointers), list(state.pointers)))
    print("  inode bitmap: 00100000 (unchanged; bits for inodes 0..7)")
    print("  data bitmap:  {} (bits for data blocks 0..7)".format(state.bitmap))
    print("  block 4: Da (unchanged); block 5: " + state.block5)
    print("  metadata agreement: " + ("YES" if state.metadata_consistent else "NO"))
    print("  interpretation: " + interpretation(state))


def setup(args):
    """Create one new lab directory; do not overwrite or remove any entry.

    The default workspace is the current working directory. --workspace exists for
    instructor testing or an assigned alternate workspace, not device paths.
    mkdir(exist_ok=False) rejects an existing directory or symlink. File
    mode 'x' likewise rejects existing names. A failed setup leaves its
    newly made entries in place for inspection instead of deleting them.
    """
    workspace = args.workspace.expanduser().resolve()
    workspace.mkdir(parents=True, exist_ok=True)
    destination = workspace / LAB_DIRECTORY
    try:
        destination.mkdir(mode=0o700, exist_ok=False)
    except FileExistsError:
        raise SystemExit(
            "Setup stopped: {} already exists. Nothing was overwritten.\n"
            "Use the existing lab files if untouched, or choose a fresh parent with --workspace.\n"
            "No existing files will be reset automatically.".format(destination)
        )
    with (destination / "foo").open("x", encoding="utf-8", newline="\n") as stream:
        stream.write("hello\n")
    with (destination / "lab-info.txt").open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(NOTE)
    print("CREATED REAL LAB FILES (not a simulation)")
    print("Folder: " + str(destination))
    print("foo contains 6 bytes; lab-info.txt contains {} bytes.".format(len(NOTE.encode("utf-8"))))
    print("No files were overwritten or removed. No links have been made yet.")
    print("Enter the folder with: cd '{}'".format(destination))
    print("Follow the worksheet commands in this folder.")


def lookup(args):
    """Trace the book's cold path lookup without touching a real /foo/bar."""
    print("SIMULATION ONLY - OSTEP 40.6; no filesystem reads or writes")
    print("Assume: mounted FS, superblock in memory, cold inode/directory cache.")
    print("Assume: each directory fits in one data block; /foo/bar already exists.")
    steps = [
        "Read root inode 2: obtain the location of root directory data.",
        "Read root directory data: find name foo mapped to inode 44.",
        "Read inode 44: obtain the location of foo's directory data.",
        "Read foo's directory data: find name bar and its inode number.",
        "Read bar's inode: check access and obtain size and block pointers.",
    ]
    for number, step in enumerate(steps, 1):
        print("{}. {}".format(number, step))
    print("open returns a process-local file descriptor; this is not an inode number.")
    print("Count: 5 logical reads for this cold open; allocation bitmaps: 0.")
    print("Next reads use bar's inode pointers for its three 4 KiB data blocks.")
    print("The book's uncached timeline also includes inode access and atime writes.")
    print("A warm cache and actual atime policy can change real device traffic.")


def append(args):
    print("SIMULATION ONLY - OSTEP 42.1; no filesystem reads or writes")
    print("I=inode update; B=bitmap update; D=new data Db in block 5.")
    print("A durable model write is complete and atomic; OLD bytes are unspecified.")
    if args.all:
        combinations = ["none", "I", "B", "D", "I,B", "I,D", "B,D", "I,B,D"]
        print("Completed writes | Metadata agrees | Result")
        for value in combinations:
            state = Snapshot(subset(value))
            print("{} | {} | {}".format(
                value, "YES" if state.metadata_consistent else "NO", interpretation(state)))
    else:
        state = Snapshot(args.durable)
        print("Completed model writes: " + update_list(state.durable))
        show_state(state)
    print("A metadata checker cannot reconstruct intended bytes that never persisted.")


def journal_recover(home, committed):
    """Redo is assignment of the logged after-image, so replay is idempotent."""
    return Snapshot(ALL_UPDATES) if committed else home


def journal(args):
    print("SIMULATION ONLY - OSTEP 42.3 data journaling; no real journal access")
    print("Protocol: persist TxB + I[v2] + B[v2] + Db; then persist TxE;")
    print("          then checkpoint to home locations; only later free the log.")
    print("Assume: atomic block writes, valid matching records, required waits obeyed.")
    committed = args.crash != "before-commit"
    home_updates = {
        "before-commit": frozenset(),
        "after-commit": frozenset(),
        "mid-checkpoint": frozenset("I"),
        "after-checkpoint": ALL_UPDATES,
    }[args.crash]
    home = Snapshot(home_updates)
    print("Crash point: " + args.crash)
    print("Durable model log: TxB, I[v2], B[v2], Db" + (", TxE" if committed else "; NO TxE"))
    print("Completed checkpoint writes: " + update_list(home_updates))
    show_state(home, "Home locations before recovery")
    if args.replay:
        recovered = journal_recover(home, committed)
        if committed:
            print("Recovery: REDO the valid committed transaction to all home locations.")
        else:
            print("Recovery: SKIP the uncommitted transaction; keep the old file.")
        show_state(recovered, "Home locations after recovery")
        repeated = journal_recover(recovered, committed)
        print("Repeating recovery changes the result: " + ("NO (idempotent)" if repeated == recovered else "YES"))
    else:
        print("Predict recovery, then rerun with --replay to check your explanation.")


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="CSC-2450 tiny file lab and in-memory filesystem teaching models.",
        epilog="Only setup writes real files. All other commands print deterministic simulations."
    )
    commands = parser.add_subparsers(dest="command", required=True)
    make = commands.add_parser("setup", help="create a new Lecture 20 directory with a 6-byte foo")
    make.add_argument("--workspace", type=Path, default=Path.cwd(),
                      help="parent workspace; default: current working directory")
    make.set_defaults(run=setup)
    read = commands.add_parser("lookup", help="trace the book's cold open of /foo/bar")
    read.set_defaults(run=lookup)
    crash = commands.add_parser("append", help="inspect a partial append without journaling")
    choice = crash.add_mutually_exclusive_group()
    choice.add_argument("--durable", type=subset, default=frozenset(),
                        help="completed model writes: none, I, B, D, or a subset such as I,B")
    choice.add_argument("--all", action="store_true", help="show all eight subsets, including no/all writes")
    crash.set_defaults(run=append)
    recover = commands.add_parser("journal", help="inspect a data-journal crash and optional recovery")
    recover.add_argument("--crash", choices=["before-commit", "after-commit", "mid-checkpoint", "after-checkpoint"],
                         default="after-commit")
    recover.add_argument("--replay", action="store_true", help="print the recovery result and idempotence check")
    recover.set_defaults(run=journal)
    args = parser.parse_args(argv)
    try:
        args.run(args)
    except OSError as error:
        parser.exit(1, "Operation stopped: {}\n".format(error))


if __name__ == "__main__":
    main()
