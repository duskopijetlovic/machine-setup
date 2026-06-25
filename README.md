# machine-setup

Personal machine setup: dotfiles, configuration, utility scripts, and the
bootstrap to deploy them. This is the single source of truth for making a
fresh machine "mine" — clone it, run the bootstrap, and the configuration
below is put into place.

Targets: RHEL 10.x (GNOME/Wayland) on the primary machines, with FreeBSD 14
(X11/FVWM3) secondaries. Scripts aim to be POSIX-portable where practical;
GNOME/Wayland-specific pieces live under `gnome/`.

> **Formerly named `dotfiles`.** This repository was renamed to better reflect
> that it holds more than dotfiles (config, utility scripts, and setup tooling).
> Old `dotfiles` links/clones should redirect here.

## Layout

| Directory | Holds                                                    | Deploys to                                 |
|-----------|----------------------------------------------------------|--------------------------------------------|
| `shell/`  | Shell startup & aliases (`.bashrc`, `.profile`, etc.)    | symlinked into `~/`                        |
| `gnome/`  | GNOME/Wayland setup scripts (e.g. workspace keybindings) | run on demand; not on `PATH`               |
| `config/` | Files destined for XDG config (e.g. `environment.d/`)    | copied/symlinked into `~/.config/`         |
| `bin/`    | Utility scripts run as everyday commands                 | symlinked into `~/.local/bin/` (on `PATH`) |
| `x11/`    | X11/FVWM3 bits for the FreeBSD machines                  | symlinked into `~/`                        |
| `setup/`  | Bootstrap script(s) that deploy everything above         | run manually on a new machine              |

> Layout is descriptive of intent — add or drop directories as the repo grows.
> The guiding rule: split by **lifecycle/deployment**, not by file type. Things
> set up together in one pass on a new machine live here together, organized by
> directory rather than by separate repositories.

## Setup vs. utility scripts

Two categories of script live here, with different homes and habits:

- **Setup scripts** (run rarely, to *establish* state) — e.g.
  `gnome/gnome-workspace-jumps.sh`. Invoked deliberately when configuring a
  machine or changing a preference. Not placed on `PATH`.
- **Utility scripts** (run often, as commands) — e.g. a screenshot wrapper,
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

Symlink vs. copy convention: things edited in-repo (shell rc files, utility
scripts) are **symlinked** so the repo stays the master copy; things that must
be real files at their destination are **copied**.

## Notes

- Keep secrets (tokens, keys, credentials) out of tracked files; use
  `.gitignore` so they never enter history or backups.
- Reversible config scripts include a `--reset` mode and print BEFORE/AFTER
  snapshots, so each run leaves an auditable trail of what changed.
