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

# The sealed gate: /output/entry.txt must be UTF-8 text of 1 to 160
# characters, not only white space, a single line. Refuse to write
# anything that would fail it rather than emit an invalid entry.
assert 1 <= len(LINE) <= 160, "entry line outside the 1-160 character gate"
assert LINE.count("\n") == 0, "entry line must be a single line"
assert LINE.strip() == LINE and LINE.strip(), "entry must not be only white space"


def main() -> None:
    out_path = os.environ.get("MAKEFUN_OUTPUT", "/output/entry.txt")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(LINE)


if __name__ == "__main__":
    main()
