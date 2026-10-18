UNICODE CLI TOOLS
=================

A small suite of command-line tools for Unicode character lookup, string
inspection, and escape sequence encoding/decoding.

    unichar.py   Look up a character, convert a hex code point, or search
                 Unicode names.

    unistr       Show Unicode info for every character in a string.

    uniesc.py    Encode text to Unicode escape sequences, or decode them back.


SETUP
-----

All three tools require Python 3. No third-party packages needed -- only
stdlib (unicodedata, argparse, html, re).

Make them executable:

    chmod +x unichar.py uniesc.py unistr

NOTE: unistr  expects  unichar.py  to be in the **same directory**. 

Neither tool needs to be on your PATH -- you can keep them in a scripts 
directory and call them with their full or relative path.

Note for tcsh/csh users: unistr is a #!/bin/sh script. 
Run it as a script (./unistr or with its full path); do not paste it directly 
into a tcsh or csh session, as "while read" is sh syntax.


------------------------------------------------------------------------
unichar.py
------------------------------------------------------------------------

Three subcommands: info, char, search.


info -- character -> details
............................

    ./unichar.py info '🐱'

    Char: 🐱
    Name: CAT FACE
    Code: U+1F431
    Category: So

    ./unichar.py info 'ñ'

    Char: ñ
    Name: LATIN SMALL LETTER N WITH TILDE
    Code: U+00F1
    Category: Ll

Non-printable characters are shown as their Python repr with an explanation:

    printf '\xc2\xa0' | ./unichar.py info

    Char: '\xa0'  (not directly displayable - shown as its Python repr;
                   space separator - a blank/whitespace character with no
                   visible mark)
    Name: NO-BREAK SPACE
    Code: U+00A0
    Category: Zs

Also reads from stdin:

    echo '€' | ./unichar.py info


char -- hex code point -> character
....................................

Accepts U+XXXX, u+xxxx, or bare hex digits, with or without leading zeros:

    ./unichar.py char U+1F431
    ./unichar.py char 1F431
    ./unichar.py char 1f431

    Char: 🐱
    Name: CAT FACE
    Code: U+1F431
    Category: So

Noncharacters and unassigned code points get distinct messages:

    ./unichar.py char U+FFFE     # noncharacter

    Char: '\ufffe'  (not directly displayable - shown as its Python repr;
                     Unicode noncharacter - permanently reserved; guaranteed
                     never to be assigned a character)
    Name: UNKNOWN
    Code: U+FFFE
    Category: Cn

    ./unichar.py char U+0378     # unassigned (but not a noncharacter)

    Char: '\u0378'  (not directly displayable - shown as its Python repr;
                     unassigned code point - not currently assigned a
                     character (may be in a future Unicode version))
    Name: UNKNOWN
    Code: U+0378
    Category: Cn


search -- term -> matching characters
......................................

Searches all ~1.1 million Unicode code points by name. Takes a few seconds.

    ./unichar.py search cat

    Char: 🐱
    Name: CAT FACE
    Code: U+1F431
    Category: So
    --------------------
    Char: 😸
    Name: GRINNING CAT FACE WITH SMILING EYES
    Code: U+1F638
    Category: So
    --------------------
    ...

Search is case-insensitive and matches substrings:

    ./unichar.py search 'latin small letter a'
    echo 'snowman' | ./unichar.py search

Note: substring matching means common terms return many results. "search cat"
also returns characters whose names contain "cat" as a substring (e.g.
PREDICATE, INDICATOR). Narrow the term to reduce noise: "search 'cat face'"
returns only the cat emoji set.


------------------------------------------------------------------------
unistr
------------------------------------------------------------------------

Shows unichar.py info output for every character in a string, in sequence.

    ./unistr 'Iñtërnâtiônàlizætiøn'

    Char: I
    Name: LATIN CAPITAL LETTER I
    Code: U+0049
    Category: Lu
    --------------------
    Char: ñ
    Name: LATIN SMALL LETTER N WITH TILDE
    Code: U+00F1
    Category: Ll
    --------------------
    Char: t
    Name: LATIN SMALL LETTER T
    Code: U+0074
    Category: Ll
    --------------------
    ...

Also reads from stdin:

    echo 'café' | ./unistr
    printf '🐱🐶' | ./unistr


------------------------------------------------------------------------
uniesc.py
------------------------------------------------------------------------

Encodes Unicode text to escape sequences, or decodes them back.
Two required flags: direction (--encode / --decode) and format.


Formats
.......

By default, ASCII characters (U+0000-U+007F) pass through unchanged and
only non-ASCII characters are encoded. Use --all (or -a) to encode every
character including ASCII.

    --python    Python/JS style. BMP characters use \uXXXX (4 hex digits);
                non-BMP characters use \UXXXXXXXX (8 hex digits).
                Example for e-acute: \u00e9

    --uplus     Unicode standard notation. Non-ASCII characters encoded as
                U+XXXX; ASCII passes through.
                Example for e-acute: U+00E9

    --html      HTML/XML hex numeric entities.
                Example for e-acute: &#xE9;

    --cbytes    Raw UTF-8 byte sequences, not code points.
                Example for e-acute: \xc3\xa9


--encode
........

    ./uniesc.py --encode --python  'café 🐱'   ->  caf\u00e9 \U0001f431
    ./uniesc.py --encode --uplus   'café 🐱'   ->  cafU+00E9 U+1F431
    ./uniesc.py --encode --html    'café 🐱'   ->  caf&#xE9; &#x1F431;
    ./uniesc.py --encode --cbytes  'café 🐱'   ->  caf\xc3\xa9 \xf0\x9f\x90\xb1

With --all (ASCII encoded too):

    ./uniesc.py --encode --all --python  'café'  ->  \u0063\u0061\u0066\u00e9
    ./uniesc.py --encode --all --uplus   'café'  ->  U+0063U+0061U+0066U+00E9
    ./uniesc.py --encode --all --html    'café'  ->  &#x63;&#x61;&#x66;&#xE9;
    ./uniesc.py --encode --all --cbytes  'café'  ->  \x63\x61\x66\xc3\xa9

--all can appear in any position -- all three orderings are equivalent:

    ./uniesc.py --encode --uplus --all 'café'   ->  U+0063U+0061U+0066U+00E9
    ./uniesc.py --encode --all --uplus 'café'   ->  U+0063U+0061U+0066U+00E9
    ./uniesc.py --all --encode --uplus 'café'   ->  U+0063U+0061U+0066U+00E9


--decode
........

    ./uniesc.py --decode --python  'caf\u00e9 \U0001f431'          ->  café 🐱
    ./uniesc.py --decode --uplus   'cafU+00E9 U+1F431'             ->  café 🐱
    ./uniesc.py --decode --html    'caf&#xE9; &#x1F431;'           ->  café 🐱
    ./uniesc.py --decode --cbytes  'caf\xc3\xa9 \xf0\x9f\x90\xb1' ->  café 🐱

Note: --all has no effect on --decode. Decode always processes whatever
escape sequences it finds, regardless of whether they represent ASCII or
non-ASCII characters:

    echo 'U+0041U+0020U+0042' | ./uniesc.py --decode --uplus        ->  A B
    echo 'U+0041U+0020U+0042' | ./uniesc.py --decode --uplus --all  ->  A B


Short flags
...........

    -e    short for --encode
    -d    short for --decode
    -a    short for --all

    ./uniesc.py -e --python 'café'       ->  caf\u00e9
    ./uniesc.py -d --python 'caf\u00e9'  ->  café
    ./uniesc.py -e -a --python 'café'    ->  \u0063\u0061\u0066\u00e9


stdin
.....

All flags work with stdin:

    echo 'café' | ./uniesc.py --encode --python
    echo 'café' | ./uniesc.py -e -a --uplus
    printf 'caf\u00e9' | ./uniesc.py --decode --python


------------------------------------------------------------------------
Unicode category codes (reference)
------------------------------------------------------------------------

Category codes appear in unichar.py and unistr output.

    Lu    Letter, uppercase
    Ll    Letter, lowercase
    Lt    Letter, titlecase
    Lm    Letter, modifier
    Lo    Letter, other
    Nd    Number, decimal digit
    No    Number, other
    Zs    Separator, space
    Zl    Separator, line
    Zp    Separator, paragraph
    Cc    Control character
    Cf    Format character
    Cs    Surrogate
    Co    Private use
    Cn    Unassigned / noncharacter
    Pc    Punctuation, connector
    Pd    Punctuation, dash
    Po    Punctuation, other
    Sm    Symbol, math
    Sc    Symbol, currency
    So    Symbol, other (most emoji fall here)

Full list: https://www.unicode.org/reports/tr44/#General_Category_Values
