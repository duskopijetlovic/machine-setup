#!/bin/sh
# rsync-backup.sh -- mirror /mnt/usbflashdrive to /mnt/usbflashdrive2.
# Minimal and deliberate: one rsync call, no sync/backup app layer. See
# README.md "Config, not data" for why this exists and what it protects.
#
# Usage:
#   ./rsync-backup.sh              run the mirror
#   ./rsync-backup.sh --dry-run    show what would change, write nothing
#
# Safety: refuses to run if either side looks unmounted (missing or empty),
# so an unmounted drive can never masquerade as "empty" to rsync and trigger
# --delete against a destination that's actually still full of real data.
# Heuristic, not a true mount check (portable across FreeBSD/RHEL without
# GNU/BSD-specific stat flags) -- good enough for a drive that's never
# legitimately empty once it has a life/ directory on it.

SRC=/mnt/usbflashdrive/
DST=/mnt/usbflashdrive2
LOG="$DST/backup.log"

is_nonempty_dir() {
    [ -d "$1" ] && [ -n "$(ls -A "$1" 2>/dev/null)" ]
}

if ! is_nonempty_dir "$SRC"; then
    echo "rsync-backup: refusing to run -- $SRC missing or empty" \
         "(unmounted?)" >&2
    exit 1
fi
if ! is_nonempty_dir "$DST"; then
    echo "rsync-backup: refusing to run -- $DST missing or empty" \
         "(unmounted?)" >&2
    exit 1
fi

opts="--delete -rav"
mode="live"
if [ "$1" = "--dry-run" ]; then
    opts="$opts -n"
    mode="dry-run"
fi

ts=$(date +'%Y-%m-%d %H:%M:%S')
echo "[$ts] rsync-backup: starting ($mode)" | tee -a "$LOG"

# rc must be captured via a temp file, not `$?` after the pipe -- in a
# POSIX pipeline, `$?` reflects tee's exit status (last in the pipe), not
# rsync's, since tee itself almost always succeeds regardless of what fed
# it. Without this, a failed rsync would still report success.
rc_file=$(mktemp)
{ rsync $opts "$SRC" "$DST"; echo $? > "$rc_file"; } 2>&1 | tee -a "$LOG"
rc=$(cat "$rc_file")
rm -f "$rc_file"

ts=$(date +'%Y-%m-%d %H:%M:%S')
if [ "$rc" -eq 0 ]; then
    echo "[$ts] rsync-backup: done" | tee -a "$LOG"
else
    echo "[$ts] rsync-backup: FAILED (rsync exit $rc)" | tee -a "$LOG"
fi

exit "$rc"
