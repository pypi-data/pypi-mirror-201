"""Utility Functions."""
import string
from pathlib import Path


def get_title(path: Path) -> str:
    """Extract title from note."""
    found_line = False

    with path.open(encoding="utf-8") as fd_in:

        for line in fd_in.readlines():
            if "=======" in line:  # pylint: disable=no-else-continue
                found_line = True
                continue

            elif found_line:
                title = line.strip()
                break

    return title


def parse_stem(stem: str) -> str:
    """Extract group name from note stem."""
    tokens = stem.split('__')

    if len(tokens) == 1:
        return ''

    if len(tokens) == 3:
        return tokens[0]

    try:
        _ = int(tokens[0])
        return ''

    except ValueError:
        return tokens[0]


def to_title_case(title: str, ) -> str:
    """Convert title to title case."""
    return string.capwords(title, sep='_').replace('_', ' ')
