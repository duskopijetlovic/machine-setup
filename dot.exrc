Craig Bruces' Handy "vi" Setup Guide

CONFIGURATION ("~/.exrc" file)

My ".exrc" file has the following lines in it.  Note that the "^M"s are
actually real carriage returns.

:set noautoindent wrapmargin=0 tabstop=4 shiftwidth=4
map ^[OP 1G!Gexpand -4^M
map ^[OQ !}fmt -79^M
map ^[OR :set noautoindent wrapmargin=0 tabstop=8 shiftwidth=8^M
map ^[OS :set noautoindent wrapmargin=0 tabstop=4 shiftwidth=4^M

This makes it so that my sessions default to a 4-character-position TAB
spacing and so that I have the following function keys:

PF1  expand all of the TABs in the file to space characters, for 4-space TABs
PF2  reformat the paragraph that the cursor is on to use 78-char lines
PF3  set the TAB spacing to eight characters
PF4  set the TAB spacing back to four characters
