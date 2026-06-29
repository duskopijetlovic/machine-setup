# machine-setup

Personal machine setup: dotfiles, configuration, utility scripts, and the
bootstrap to deploy them. This is the single source of truth for making a
fresh machine "mine" - clone it, run the bootstrap, and the configuration
below is put into place.

Targets: RHEL 10.x (GNOME/Wayland) on the primary machines, with FreeBSD 14
(X11/FVWM3) secondaries. Scripts aim to be POSIX-portable where practical;
GNOME/Wayland-specific pieces live under `wayland/gnome/`.

> **Formerly named `dotfiles`.** This repository was renamed to better reflect
> that it holds more than dotfiles (config, utility scripts, and setup tooling).
> Old `dotfiles` links/clones should redirect here.

## Config, not data

This repository holds **machinery** - configuration, scripts, and the bootstrap
that deploys them. It does **not** hold **personal data**.

Plain-text personal data (calendar, todos, journal, waiting-fors — e.g.
`~/life/LIFE.TXT`, `~/life/stacks/calendar.txt`) lives **outside this repo**, in
the sync + backup layer (Syncthing across machines, Borg/restic for backups).
Reasons this separation is strict:

- **Privacy** - personal data must never be pushed to a public host.
- **Churn** - daily-edited data would flood the repo with noise commits.
- **Clean provenance** - "how my machine is set up" and "what is in my life"
  are different concerns and belong in different places.

This repo *does* carry **example/skeleton** versions of those data files (see
`templates/`) so a new machine can be seeded with a starting structure — but the
real, live data files always live in `~/life/` (or wherever `$LIFE_DIR` points),
never under version control here.

## Layout

| Directory        | Holds                                                    | Deploys to                                      |
|------------------|----------------------------------------------------------|-------------------------------------------------|
| `shell/`         | Shell startup & aliases (`.bashrc`, `.profile`, etc.)    | symlinked into `~/`                             |
| `wayland/`       | Wayland compositor configs, grouped by desktop/WM        | (parent; see below)                             |
| `wayland/gnome/` | GNOME setup scripts (e.g. workspace keybindings)         | run on demand; not on `PATH`                    |
| `config/`        | Files destined for XDG config (e.g. `environment.d/`)    | copied/symlinked into `~/.config/`              |
| `bin/`           | Utility scripts run as everyday commands (e.g. `agenda`) | symlinked into `~/.local/bin/` (on `PATH`)      |
| `x11/`           | X11/FVWM3 bits for the FreeBSD machines                  | symlinked into `~/`                             |
| `templates/`     | Skeleton/example personal-data files (`*.example`)       | **copied** as seeds, only if absent (see below) |
| `setup/`         | Bootstrap script(s) that deploy everything above         | run manually on a new machine                   |

> Layout is descriptive of intent — add or drop directories as the repo grows.
> The guiding rule: split by **lifecycle/deployment**, not by file type. Things
> set up together in one pass on a new machine live here together, organized by
> directory rather than by separate repositories.

## Setup vs. utility scripts

Two categories of script live here, with different homes and habits:

- **Setup scripts** (run rarely, to *establish* state) - e.g.
  `wayland/gnome/gnome-workspace-jumps.sh`. Invoked deliberately when
  configuring a machine or changing a preference. Not placed on `PATH`.
- **Utility scripts** (run often, as commands) - e.g. `bin/agenda`,
  `bin/backup-repos.sh`. Kept canonical here and symlinked into
  `~/.local/bin/` so they're callable by name.

## Deploying to a new machine

```
$ git clone https://github.com/duskopijetlovic/machine-setup.git ~/machine-setup
$ cd ~/machine-setup
# Review first, then deploy:
$ ./setup/install.sh --dry-run     # show what would happen, change nothing
$ ./setup/install.sh               # create symlinks / copy config into place
```

Three deploy verbs, by kind of file:

- **Symlink** - things edited in-repo (shell rc files, utility scripts) are
  symlinked so the repo stays the master copy.
- **Copy** - config that must be a real file at its destination is copied.
- **Seed (copy-once, never overwrite)** - `templates/*.example` files are
  copied to their live location **only if no live file already exists there**.
  This bootstraps a starting `~/life/` on a fresh machine without ever
  clobbering real data on an existing one. Seeds are copied, never symlinked —
  once seeded, the live file is private data that diverges from the template
  and must not be tracked back into this repo.

## Notes

- Keep secrets (tokens, keys, credentials) out of tracked files; use
  `.gitignore` so they never enter history or backups.
- Keep personal data out of this repo entirely (see "Config, not data");
  it lives in `~/life/` under Syncthing + backup.
- Reversible config scripts include a `--reset` mode and print BEFORE/AFTER
  snapshots, so each run leaves an auditable trail of what changed.

