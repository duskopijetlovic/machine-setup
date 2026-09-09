# .bashrc
# Deploy: cp dot.bashrc ~/.bashrc

# Source global definitions
if [ -f /etc/bashrc ]; then
    . /etc/bashrc
fi

# User specific environment
if ! [[ "$PATH" =~ "$HOME/.local/bin:$HOME/bin:" ]]; then
    PATH="$HOME/.local/bin:$HOME/bin:$PATH"
fi
export PATH

# Uncomment the following line if you don't like systemctl's auto-paging feature:
# export SYSTEMD_PAGER=

# User specific aliases and functions
if [ -d ~/.bashrc.d ]; then
    for rc in ~/.bashrc.d/*; do
        if [ -f "$rc" ]; then
            . "$rc"
        fi
    done
fi
unset rc

# --- Personal customizations ---

# Minimal prompt: $ for regular user
PS1='$ '

# vi-style command line editing
set -o vi

# Useful aliases
alias ll='ls -lh'
alias la='ls -lah'
alias ..='cd ..'

# rsync with verbose, compression, progress, and itemized change summary.
# Usage: rsyncv [rsync-options] SRC DEST
alias rsyncv='rsync -avz --progress --itemize-changes'

# Confirm environment vars are set (belt-and-suspenders for Ptyxis):
export EDITOR=vi
export VISUAL=vi
export MANWIDTH=80

# History
# NOTE: bash 4.3+ accepts -1 for truly unlimited. However, since this dotfile
# may also be deployed on legacy systems (RHEL 5 = bash 3.2, RHEL 6 = bash
# 4.1.2), a large explicit value is used for broadest compatibility.
HISTSIZE=1000000
HISTFILESIZE=1000000
HISTCONTROL=ignoredups    # skip consecutive duplicate commands
HISTTIMEFORMAT='%F %T  '  # timestamp each entry: 2026-09-09  14:23:01
