#
# .cshrc - csh resource script, read at beginning of execution by each shell
# Deploy: cp dot.cshrc ~/.cshrc
#
# see also csh(1), environ(7).
# more examples available at /usr/share/examples/csh/
#
alias h		history 25
alias j		jobs -l
alias la	ls -aF
alias lf	ls -FA
alias ll	ls -lAF

# rsync with verbose, compression, progress, and itemized change summary.
# Usage: rsyncv [rsync-options] SRC DEST
# Note: trailing args are appended automatically -- no \!* needed here since
# the expansion point is the end of the command.
alias rsyncv	'rsync -avz --progress --itemize-changes'

# These are normally set through /etc/login.conf.  You may override them here
# if wanted.
# set path = (/sbin /bin /usr/sbin /usr/bin /usr/local/sbin /usr/local/bin $HOME/bin)
set path = (/sbin /bin /usr/sbin /usr/bin /usr/local/sbin /usr/local/bin $HOME/bin /mnt/usbflashdrive/bin)
# A righteous umask
# umask 22
setenv	EDITOR	vi
setenv	VISUAL	vi
setenv	PAGER	less
setenv  BLOCKSIZE       K
setenv  LC_ALL  ""
setenv  LC_CTYPE        en_CA.UTF-8
setenv  LC_MESSAGES     en_CA.UTF-8
setenv  LC_TIME en_CA.UTF-8
setenv  LANG    en_CA.UTF-8
setenv  MANWIDTH        80
setenv  TASKRC                /mnt/usbflashdrive/mydotfiles/.taskrc
setenv  CHEAT_CONFIG_PATH     /mnt/usbflashdrive/mydotfiles/cheat/conf.yml
setenv  GEM_HOME              "$HOME/gems"
set nobeep
# Confirm before execution of 'rm *'.
set rmstar
bindkey -v
if ($?prompt) then
	# An interactive shell -- set some stuff up
        set prompt = "%# "      # Original was: set prompt = "%N@%m:%~ %# "
	set promptchars = "%#"  # If you want to change it from % to $, use
                                #   set promptchars = '$#'
                                # Also note single quotes instead of double
	set filec
	set history = 1000000
	set savehist = (1000000 merge)
	set autolist = ambiguous
	# Use history to aid expansion
	set autoexpand
	set autorehash
	set mail = (/var/mail/$USER)
	if ( $?tcsh ) then
		bindkey "^W" backward-delete-word
		bindkey -k up history-search-backward
		bindkey -k down history-search-forward
	endif
endif
