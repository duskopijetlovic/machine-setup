#!/usr/bin/env python3

# Created by AI: Claude - Model: Sonnet 5
# Date: Sep 6, 2026

# unichar: Unicode character lookup / conversion / search tool
#   info <char>    -> name, code point, category
#   char <hex>     -> character from hex code point (e.g. 1F431 or U+1F431)
#   search <term>  -> characters whose Unicode name matches term

# Examples:
#   ./unichar.py -h
#   ./unichar.py info '🐱'
#   ./unichar.py char U+1F431
#   ./unichar.py search cat

import argparse
import sys
import unicodedata

# Short, category-specific explanations for characters that have no visible
# glyph (unicodedata.category() code -> one-line description). Used only
# when a character is genuinely non-printable per str.isprintable().
NON_PRINTABLE_NOTES = {
    "Cc": "control character - no glyph; used for device/text control (e.g. tab, newline)",
    "Cf": "format character - invisible; affects layout or direction of surrounding text",
    "Cs": "surrogate code point - not valid on its own; used in UTF-16 encoding pairs",
    "Co": "private use character - no standard glyph; meaning is application-defined",
    "Cn": "unassigned code point - not currently assigned a character (may be in a future Unicode version)",
    "Zl": "line separator - invisible; marks a line boundary",
    "Zp": "paragraph separator - invisible; marks a paragraph boundary",
    "Zs": "space separator - a blank/whitespace character with no visible mark",
}


def is_noncharacter(code):
    """Return True if code is one of the 66 Unicode noncharacters: U+FDD0-U+FDEF,
    or the last two code points of any plane (U+xFFFE / U+xFFFF). These are
    permanently reserved by the Unicode standard and will never be assigned
    a character - distinct from code points that are merely unassigned so far."""
    if 0xFDD0 <= code <= 0xFDEF:
        return True
    return (code & 0xFFFF) in (0xFFFE, 0xFFFF)


def print_char_info(c, name, code, cat):
    """Print the standard Char/Name/Code/Category block, plus a one-line
    note when the character has no visible glyph of its own."""
    if c.isprintable():
        print(f"Char: {c}")
    else:
        if cat == "Cn" and is_noncharacter(ord(c)):
            note = "Unicode noncharacter - permanently reserved; guaranteed never to be assigned a character"
        else:
            note = NON_PRINTABLE_NOTES.get(cat, "non-printable character - no visible glyph")
        print(f"Char: {c!r}  (not directly displayable - shown as its Python repr; {note})")
    print(f"Name: {name}")
    print(f"Code: {code}")
    print(f"Category: {cat}")


def cmd_info(args):
    # Only drop the trailing line ending: .strip() would also eat the very
    # characters we may be asked about (space, NBSP, tab, ...).
    c = args.char if args.char else sys.stdin.read().rstrip('\r\n')
    if not c:
        print("Error: No character provided. Usage: unichar info 'char' OR echo 'char' | unichar info")
        sys.exit(1)
    c = c[0]
    try:
        name = unicodedata.name(c, "UNKNOWN")
        code = f"U+{ord(c):04X}"
        cat = unicodedata.category(c)
        print_char_info(c, name, code, cat)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def cmd_char(args):
    hex_str = args.hex_number.upper().removeprefix("U+").removeprefix("0X")
    try:
        as_int = int(hex_str, 16)
        as_chr = chr(as_int)
    except (ValueError, OverflowError) as e:
        print(f"Error: invalid code point '{args.hex_number}' ({e})")
        sys.exit(1)
    try:
        name = unicodedata.name(as_chr)
    except ValueError:
        name = "UNKNOWN"
    print_char_info(as_chr, name, f"U+{as_int:04X}", unicodedata.category(as_chr))


def cmd_search(args):
    term = args.term if args.term else sys.stdin.read().strip()
    if not term:
        print("Error: No search term provided. Usage: unichar search 'word' OR echo 'word' | unichar search")
        sys.exit(1)
    term = term.upper()
    found = 0
    for code in range(0x110000):
        c = chr(code)
        try:
            name = unicodedata.name(c)
        except ValueError:
            continue
        if term in name:
            if found:
                print("-" * 20)
            print_char_info(c, name, f"U+{code:04X}", unicodedata.category(c))
            found += 1
    if found == 0:
        print(f"No matches found for '{term}'.")


def main():
    parser = argparse.ArgumentParser(
        prog="unichar",
        description="unichar -- command-line tool for looking up, converting, and searching Unicode characters",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_info = sub.add_parser("info", help="Get details about a character (char -> name/code/category)")
    p_info.add_argument("char", nargs="?", help="character (reads stdin if omitted)")
    p_info.set_defaults(func=cmd_info)

    p_char = sub.add_parser("char", help="Get a character from its hex code point (hex -> char)")
    p_char.add_argument("hex_number", help="hex code point, e.g. 1F431 or U+1F431")
    p_char.set_defaults(func=cmd_char)

    p_search = sub.add_parser("search", help="Search Unicode names for a term (term -> matching chars)")
    p_search.add_argument("term", nargs="?", help="search term (reads stdin if omitted)")
    p_search.set_defaults(func=cmd_search)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
