#!/usr/bin/env python3

# Created by AI: Claude - Model: Sonnet 4.6 
# Date: Sep 21, 2026

# uniesc: encode Unicode text to escape sequences, or decode them back
#
# By default, ASCII characters (U+0000-U+007F) pass through unchanged and only
# non-ASCII characters are encoded. Use --all to encode every character,
# including ASCII. --all only affects --encode; --decode always handles any
# valid escape sequence regardless.
#
# --uplus round trips: U+XXXX tokens are not self-delimiting (decode reads up
# to 6 hex digits). When an ASCII hex digit (0-9, a-f, A-F) follows an encoded
# character, encode zero-pads that code point to 6 digits (U+0000E9a), so
# decode reads exactly 6 and 'a' stays a literal 'a'.
#
# Examples:
#   ./uniesc.py --encode --python 'café 🐱'
#   ./uniesc.py --encode --python --all 'café 🐱'
#   ./uniesc.py --decode --python 'caf\u00e9 \U0001f431'
#   ./uniesc.py --encode --uplus 'café 🐱'
#   ./uniesc.py --encode --uplus --all 'café 🐱'
#   ./uniesc.py --decode --uplus 'cafU+00E9 U+1F431'
#   ./uniesc.py --encode --html 'café 🐱'
#   ./uniesc.py --encode --html --all 'café 🐱'
#   ./uniesc.py --decode --html 'caf&#xE9; &#x1F431;'
#   ./uniesc.py --encode --cbytes 'café 🐱'
#   ./uniesc.py --encode --cbytes --all 'café 🐱'
#   ./uniesc.py --decode --cbytes 'caf\xc3\xa9 \xf0\x9f\x90\xb1'
#   ./uniesc.py --decode --cbytes 'c\x61f\xc3\xa9 \xf0\x9f\x90\xb1'
#   ./uniesc.py --decode --cbytes '\x63\x61\x66\xc3\xa9 \xf0\x9f\x90\xb1'
#   echo 'café' | ./uniesc.py --encode --python

import argparse
import html as html_module
import re
import sys


def _chr_or_keep(cp, token):
    """chr(cp), or the original token (with a warning on stderr) when cp is not
    a valid scalar value: above U+10FFFF, or a surrogate (U+D800-U+DFFF).
    Neither can be printed as UTF-8, so keeping the token beats a traceback."""
    if cp > 0x10FFFF or 0xD800 <= cp <= 0xDFFF:
        print(f'uniesc: skipped invalid code point {token}', file=sys.stderr)
        return token
    return chr(cp)


# ---------------------------------------------------------------------------
# Encode functions: text -> escape sequences
# ---------------------------------------------------------------------------

def encode_python(text, encode_ascii=False):
    r"""Non-ASCII BMP -> \uXXXX; non-BMP -> \UXXXXXXXX.
    ASCII passes through unless encode_ascii=True."""
    result = []
    for c in text:
        cp = ord(c)
        if cp < 0x80 and not encode_ascii:
            result.append(c)
        elif cp <= 0xFFFF:
            result.append(f'\\u{cp:04x}')
        else:
            result.append(f'\\U{cp:08x}')
    return ''.join(result)


_ASCII_HEX = frozenset('0123456789abcdefABCDEF')


def encode_uplus(text, encode_ascii=False):
    """Non-ASCII -> U+XXXX tokens; ASCII passes through unless encode_ascii=True.

    U+ tokens are not self-delimiting, and decode reads up to 6 hex digits. So
    when a passed-through ASCII hex digit follows a token, the code point is
    zero-padded to the full 6 digits (U+00E9 then 'a' -> U+0000E9a), which
    decode reads back exactly. Without a following hex digit the usual 4-6
    digit form is used, so ordinary output is unchanged."""
    result = []
    for i, c in enumerate(text):
        cp = ord(c)
        if cp < 0x80 and not encode_ascii:
            result.append(c)
        else:
            nxt = text[i + 1] if i + 1 < len(text) else ''
            width = 6 if (not encode_ascii and nxt in _ASCII_HEX) else 4
            result.append(f'U+{cp:0{width}X}')
    return ''.join(result)


def encode_html(text, encode_ascii=False):
    """Non-ASCII -> &#xXXXX; hex HTML numeric entities.
    ASCII passes through unless encode_ascii=True."""
    result = []
    for c in text:
        cp = ord(c)
        if cp < 0x80 and not encode_ascii:
            result.append(c)
        else:
            result.append(f'&#x{cp:X};')
    return ''.join(result)


def encode_cbytes(text, encode_ascii=False):
    r"""Non-ASCII -> UTF-8 byte sequence as \xNN\xNN.
    ASCII passes through unless encode_ascii=True."""
    result = []
    for c in text:
        cp = ord(c)
        if cp < 0x80 and not encode_ascii:
            result.append(c)
        else:
            for byte in c.encode('utf-8'):
                result.append(f'\\x{byte:02x}')
    return ''.join(result)


# ---------------------------------------------------------------------------
# Decode functions: escape sequences -> text
# ---------------------------------------------------------------------------

def decode_python(text):
    r"""Replace \UXXXXXXXX and \uXXXX with the corresponding characters."""
    def replacer(m):
        return _chr_or_keep(int(m.group(1) or m.group(2), 16), m.group(0))
    # Match 8-digit \U first, then 4-digit \u
    return re.sub(r'\\U([0-9a-fA-F]{8})|\\u([0-9a-fA-F]{4})', replacer, text)


def decode_uplus(text):
    """Replace U+XXXX tokens (4-6 hex digits) with the corresponding characters."""
    return re.sub(
        r'U\+([0-9a-fA-F]{4,6})',
        lambda m: _chr_or_keep(int(m.group(1), 16), m.group(0)),
        text,
    )


def decode_html(text):
    """Replace &#xXXXX; (and &#NNNN;) HTML numeric entities with characters."""
    return html_module.unescape(text)


def decode_cbytes(text):
    r"""Replace consecutive \xNN sequences with UTF-8 decoded characters."""
    def replacer(m):
        hex_bytes = re.findall(r'[0-9a-fA-F]{2}', m.group(0))
        return bytes(int(b, 16) for b in hex_bytes).decode('utf-8', errors='replace')
    return re.sub(r'(?:\\x[0-9a-fA-F]{2})+', replacer, text)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

# Shown at the bottom of --help. Kept ASCII-only so help prints under any
# locale. The full reference is the README that ships next to this script.
EPILOG = r"""formats (shown for e-acute U+00E9 and cat face U+1F431):
  --python   \u00e9    \U0001f431
  --uplus    U+00E9    U+1F431
  --html     &#xE9;    &#x1F431;
  --cbytes   \xc3\xa9  \xf0\x9f\x90\xb1

examples:
  uniesc.py --decode --python 'caf\u00e9 \U0001f431'
  uniesc.py --decode --uplus  'cafU+00E9 U+1F431'
  uniesc.py -e --all --html 'text'
  echo 'text' | uniesc.py -e --python

notes:
  --uplus   U+ tokens are not self-delimiting (decode reads up to 6 hex
            digits). When an ASCII hex digit (0-9, a-f, A-F) follows an
            encoded character, encode zero-pads it to 6 digits (U+0000E9a)
            so the round trip is exact.
  --decode  ignores --all. Code points above U+10FFFF and surrogates
            (U+D800-U+DFFF) are left as written, with a warning on stderr.
            --html also decodes named entities (&amp;, &eacute;).

full reference: unichar-unistr-uniesc-README.txt (next to this script)
"""



def main():
    parser = argparse.ArgumentParser(
        prog='uniesc',
        description=(
            'uniesc -- encode Unicode text to escape sequences, or decode them back.\n'
            'By default, ASCII characters (U+0000-U+007F) pass through unchanged.\n'
            'Use --all with --encode to encode every character including ASCII.'
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=EPILOG,
    )

    direction = parser.add_mutually_exclusive_group(required=True)
    direction.add_argument(
        '--encode', '-e', action='store_true',
        help='encode text -> escape sequences',
    )
    direction.add_argument(
        '--decode', '-d', action='store_true',
        help='decode escape sequences -> text',
    )

    fmt = parser.add_mutually_exclusive_group(required=True)
    fmt.add_argument(
        '--python', action='store_true',
        help=r'Python/C style: \uXXXX (BMP) / \UXXXXXXXX (non-BMP)',
    )
    fmt.add_argument(
        '--uplus', action='store_true',
        help='Unicode notation: U+XXXX (non-ASCII encoded, ASCII passes through)',
    )
    fmt.add_argument(
        '--html', action='store_true',
        help='HTML/XML hex numeric entities: &#xXXXX;',
    )
    fmt.add_argument(
        '--cbytes', action='store_true',
        help=r'C/shell UTF-8 byte sequences: \xNN\xNN',
    )

    parser.add_argument(
        '--all', '-a', action='store_true',
        help='encode ASCII characters too (only affects --encode)',
    )
    parser.add_argument(
        'text', nargs='?',
        help='text to process (reads stdin if omitted)',
    )

    # Bare invocation: the required flags are missing anyway, so show the full
    # help (on stderr, exit 2 like any usage error) instead of a terse error.
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(2)

    args = parser.parse_args()

    if args.text is not None:
        text = args.text
    else:
        text = sys.stdin.read().rstrip('\n')

    if not text:
        print('Error: No text provided.', file=sys.stderr)
        sys.exit(1)

    if args.encode:
        fn = (encode_python if args.python else
              encode_uplus  if args.uplus  else
              encode_html   if args.html   else
              encode_cbytes)
        print(fn(text, encode_ascii=args.all))
    else:
        fn = (decode_python if args.python else
              decode_uplus  if args.uplus  else
              decode_html   if args.html   else
              decode_cbytes)
        print(fn(text))


if __name__ == '__main__':
    main()
