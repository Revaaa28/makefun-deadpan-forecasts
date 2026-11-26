#!/usr/bin/env python3
"""Deadpan Forecasts for Cities That Do Not Exist — make.fun entry.

Writes a single deadpan weather forecast for an invented city to
/output/entry.txt. The text is a fixed string, chosen by manual ranking
against the kit judge brief (dry, deadpan TV meteorologist; criteria in
order: on-subject forecast, funnier, more vivid, broadcast tone, tight use
of characters): nine millimetres of rain in one hour, all of it landing on
the same parked bicycle, with the owner already notified twice.

The program is deterministic: it writes byte-identical output on every run.
"""

import os

LINE = "In Dullbridge, expect 9 millimetres of rain between 3 and 4 p.m., all of it landing on the same parked bicycle; the owner has been notified twice."

# The city the entry is about. The forecast line must name this city and no
# other, so a later edit that renames the city in the text (or swaps in a
# different line) fails loudly instead of silently shipping a mismatched
# entry under this entry's title.
CITY = "Dullbridge"


def validate_entry(text: str) -> None:
    """Gate the exact text that will be written, not just the constant.

    Checks the sealed gate (UTF-8 text, 1 to 160 characters, not only white
    space, a single line) plus two failure modes the bare asserts missed:
    carriage returns / control characters hiding inside the line, and a
    city name that no longer matches the entry's title city.
    """
    if not (1 <= len(text) <= 160):
        raise ValueError("entry line outside the 1-160 character gate")
    if not text.strip():
        raise ValueError("entry must not be only white space")
    if text.strip() != text:
        raise ValueError("entry must not start or end with white space")
    # A single line means no line break of any kind, not just "\n".
    if any(ch in text for ch in ("\n", "\r", "\u2028", "\u2029")):
        raise ValueError("entry line must be a single line")
    # No other control characters may hide in the line either.
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in text):
        raise ValueError("entry line contains a control character")
    # The forecast must be about this entry's city, named up front in
    # broadcast style ("In <city>, ...").
    if not text.startswith(f"In {CITY}, "):
        raise ValueError(f"entry must open with the forecast city 'In {CITY}, '")


# The sealed gate: /output/entry.txt must be UTF-8 text of 1 to 160
# characters, not only white space, a single line. Refuse to write
# anything that would fail it rather than emit an invalid entry.
validate_entry(LINE)


def main() -> None:
    out_path = os.environ.get("MAKEFUN_OUTPUT", "/output/entry.txt")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(LINE)
    # Re-gate the bytes actually written: a write that silently changed the
    # text (encoding, newline translation) must fail here, not ship.
    with open(out_path, "r", encoding="utf-8", newline="") as f:
        written = f.read()
    if written != LINE:
        raise ValueError("written entry differs from the validated line")
    validate_entry(written)


if __name__ == "__main__":
    main()
