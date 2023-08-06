"""Template Filters."""
from itertools import groupby, zip_longest

from jinja2.filters import do_batch


def format_rst(cell):
    """Format cell for rst list table."""
    if cell:
        return f':doc:`{cell.title} <{cell.url}>`'

    return ""


def table_header(node):
    """Return table header row."""
    return node.groups()


def table_body(node):
    """Return table rows."""
    if not node.groups():
        return do_batch(node.notes, 4, fill_with="")

    notes = {
        key: list(value)
        for key, value in groupby(node.notes, lambda x: x.group)
    }
    cols = [notes[x] for x in node.groups(overide_names=False)]

    return zip_longest(*cols, fillvalue=None)
