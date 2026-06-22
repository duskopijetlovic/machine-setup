#!/usr/bin/env bash
# gnome-workspace-jumps.sh
# Hybrid: keep dynamic workspaces, add Super+N direct-jump + Super+Shift+N move.
# Usage:  ./gnome-workspace-jumps.sh          # apply
#         ./gnome-workspace-jumps.sh --reset  # revert to defaults
set -euo pipefail

if [ "${1:-}" = "--reset" ]; then
  echo "# RESET snapshot: $(date -Is)"
  for n in $(seq 1 9); do
    gsettings reset org.gnome.shell.keybindings    "switch-to-application-$n"
    gsettings reset org.gnome.desktop.wm.keybindings "switch-to-workspace-$n"
    gsettings reset org.gnome.desktop.wm.keybindings "move-to-workspace-$n"
  done
  echo "# Reverted to defaults."
  exit 0
fi

echo "# BEFORE snapshot: $(date -Is)"
gsettings list-recursively org.gnome.shell.keybindings | grep switch-to-application
gsettings list-recursively org.gnome.desktop.wm.keybindings | grep -E 'switch-to-workspace-[0-9]|move-to-workspace-[0-9]'

for n in $(seq 1 9); do
  gsettings set "org.gnome.shell.keybindings" "switch-to-application-$n" "[]"
  if [ "$n" = "1" ]; then
    gsettings set org.gnome.desktop.wm.keybindings switch-to-workspace-1 "['<Super>1', '<Super>Home']"
    gsettings set org.gnome.desktop.wm.keybindings move-to-workspace-1   "['<Super><Shift>1', '<Super><Shift>Home']"
  else
    gsettings set "org.gnome.desktop.wm.keybindings" "switch-to-workspace-$n" "['<Super>$n']"
    gsettings set "org.gnome.desktop.wm.keybindings" "move-to-workspace-$n"   "['<Super><Shift>$n']"
  fi
done

echo "# AFTER snapshot: $(date -Is)"
gsettings list-recursively org.gnome.desktop.wm.keybindings | grep -E 'switch-to-workspace-[0-9]|move-to-workspace-[0-9]'
gsettings list-recursively org.gnome.shell.keybindings | grep switch-to-application
