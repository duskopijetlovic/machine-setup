# doc/hosts/

Per-host notes: hardware, display, and config quirks specific to a single
machine, one file per host as `doc/hosts/<hostname>.md`.

## What goes here

Facts true for **one machine only** - things that depend on that box's specific
hardware or firmware and would be **wrong** if assumed elsewhere. Examples:
GPU/display cabling, VT/console behaviour, machine-specific driver or kernel
workarounds.

## What does NOT go here

- Portable config, dotfiles, scripts - those live in their normal repo homes
  (`dotfiles/`, `bin/`, `wayland/`, ...).
- Anything true across machines - if it generalises, it belongs in the relevant
  tooling doc or the top-level README, not here.

## Rules

- **Not portable.** Never copy a fix from one host file into another without
  confirming it actually applies to that hardware.
- **Scope disclaimer at the top of every host file** - state plainly which
  machine it covers and what it does *not* apply to.
- **Reference-only.** Like the rest of `doc/`, these are never deployed;
  `install.sh` does not touch them. Browsed/`grep`ped in place.
- **Re-verify after driver/kernel updates** - host quirks (especially GPU ones)
  can change under you; keep the confirmed kernel/driver version in the file so
  a stale note is recognisable.

## Index

The authoritative list of host files lives in the top-level
[`README.md`](../../README.md) under **Per-host notes** - kept there as the
single source of truth rather than duplicated here.
