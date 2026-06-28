#!/usr/bin/env bash

# Tested on RHEL 10.2 
#
# screenshot - a small, portable wrapper around gnome-screenshot-tool.
#
# Usage:
#   screenshot [mode] [delay_seconds]
#
# Modes:
#   full     Entire screen                           [default]
#   win      A window (grab a window)
#   area     A rectangular area you select
#
# delay_seconds: whole number of seconds to wait before capture.
#                Default 5.
#                Use 0 for immediate.
#
# Examples:
#   screenshot                 # full screen, 5s delay
#   screenshot win             # window, 5s delay
#   screenshot win 3           # window, 3s delay
#   screenshot area 0          # area select, no delay
#
# The mouse pointer is included by default (handy for hover captures).
# Set NO_POINTER=1 to leave it out, e.g.  NO_POINTER=1 screenshot full
#
# Output: ~/Pictures/Screenshots/screenshot-<mode>-YYYY-MM-DD_HH-MM-SS.png
# Override the directory with the SHOT_DIR environment variable.
#
# For viewing images:
#   xdg-open ~/Pictures/Screenshots/screenshot-<mode>-YYYY-MM-DD_HH-MM-SS.png
#
# Opens in whatever your default viewer is


set -euo pipefail

# --- configuration -----------------------------------------------------------
OUTDIR="${SHOT_DIR:-$HOME/Pictures/Screenshots}"
TOOL="gnome-screenshot-tool"

# --- argument parsing --------------------------------------------------------
mode="${1:-full}"
delay_s="${2:-5}"

# --- preflight checks --------------------------------------------------------
if ! command -v "$TOOL" >/dev/null 2>&1; then
    echo "error: $TOOL is not installed or not in PATH." >&2
    exit 1
fi

if ! [[ "$delay_s" =~ ^[0-9]+$ ]]; then
    echo "error: delay must be a whole number of seconds (got '$delay_s')." >&2
    exit 1
fi

mkdir -p "$OUTDIR"
stamp="$(date +%F_%H-%M-%S)"

# Include the pointer unless NO_POINTER is set.
pointer_flag=(--include-pointer)
if [[ "${NO_POINTER:-0}" == "1" ]]; then
    pointer_flag=()
fi

# --- mode -> tool flags ------------------------------------------------------
case "$mode" in
    full)
        out="$OUTDIR/screenshot-full-$stamp.png"
        "$TOOL" --delay "$delay_s" "${pointer_flag[@]}" --file "$out"
        ;;
    win)
        out="$OUTDIR/screenshot-win-$stamp.png"
        "$TOOL" --window --delay "$delay_s" "${pointer_flag[@]}" --file "$out"
        ;;
    area)
        out="$OUTDIR/screenshot-area-$stamp.png"
        "$TOOL" --area --delay "$delay_s" "${pointer_flag[@]}" --file "$out"
        ;;
    -h|--help|help)
        sed -n '2,30p' "$0" | sed 's/^# \{0,1\}//'
        exit 0
        ;;
    *)
        echo "error: unknown mode '$mode'." >&2
        echo "valid modes: full, win, area  (try: screenshot --help)" >&2
        exit 1
        ;;
esac

echo "saved: $out"
