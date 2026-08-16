#!/bin/sh
# keyboard-layouts.sh — set GNOME's three input sources: English (US),
# Serbian Latin, Serbian Cyrillic. Mirrors x11/60-keyboard-layout-multi.conf
# on the FreeBSD/X11 machines (same three layouts, same variant).
#
# Usage:
#   ./keyboard-layouts.sh            apply the three layouts
#   ./keyboard-layouts.sh --reset    back to GNOME's single-layout default (us)
#
# BEFORE/AFTER snapshots print on every run, so each change leaves an
# auditable trail (this repo's convention for reversible config scripts;
# see README.md "Notes"). Not placed on PATH -- run on demand from the repo,
# same as the other wayland/gnome/ scripts.
#
# Deploy: nothing to symlink; just run it once per machine when setting up.

KEY_SCHEMA="org.gnome.desktop.input-sources"
KEY_NAME="sources"
DESIRED="[('xkb', 'us'), ('xkb', 'rs+latinunicode'), ('xkb', 'rs')]"
RESET_TO="[('xkb', 'us')]"

echo "BEFORE: $(gsettings get "$KEY_SCHEMA" "$KEY_NAME")"

if [ "$1" = "--reset" ]; then
    gsettings set "$KEY_SCHEMA" "$KEY_NAME" "$RESET_TO"
else
    gsettings set "$KEY_SCHEMA" "$KEY_NAME" "$DESIRED"
fi

echo "AFTER:  $(gsettings get "$KEY_SCHEMA" "$KEY_NAME")"

# ---- NOTES ----------------------------------------------------------------
#
# Switching between layouts: GNOME binds this to its own keybinding rather
# than an XKB option -- there's no GNOME equivalent of X11's
# grp:alt_shift_toggle to set here. Check the current binding with:
#   gsettings get org.gnome.desktop.wm.keybindings switch-input-source
#   gsettings get org.gnome.desktop.wm.keybindings switch-input-source-backward
# GNOME's default is commonly Super+Space (forward) / Shift+Super+Space
# (backward) -- confirm on your version with the commands above rather than
# assuming, since this has changed across GNOME releases. To customize:
#   gsettings set org.gnome.desktop.wm.keybindings switch-input-source \
#     "['<Super>space']"
#
# Layout/variant naming differs by tool, same XKB data underneath:
#   GNOME (this script):        'rs+latinunicode'   (layout+variant)
#   X11 xorg.conf.d (the .conf):'rs(latinunicode)'   (layout(variant))
