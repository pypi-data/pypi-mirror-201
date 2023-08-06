"""Main module."""
from pathlib import Path
from typing import IO, List

import anytree
import jinja2
import nanoid

from . import data

NANOID_ALPHABET = '-0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
NANOID_SIZE = 10


def get_notes(
    root_dir: Path,
    *,
    filter_: str = '_include',
    note_pattern: str = '**/*.rst',
    meta_pattern: str = '**/_meta.yaml'
) -> (List[data.Note], List[data.MetaData]):
    """Return notes and meta data from notebook."""
    notes = [
        data.Note.from_path(root_dir, x)
        for x in sorted(root_dir.glob(note_pattern)) if filter_ not in x.parts
    ]

    meta_data = [
        data.MetaData.from_yaml(root_dir, x)
        for x in root_dir.glob(meta_pattern)
    ]

    return (notes, meta_data)


def get_target() -> str:
    """Create a random target ID."""
    return nanoid.generate(NANOID_ALPHABET, NANOID_SIZE)


def to_tree(notes: List[data.Note],
            meta_data: List[data.MetaData]) -> data.Node:
    """Get a tree of notes from a list of notes and override meta data."""
    root = data.Node('root')
    resolver = anytree.resolver.Resolver()

    for note in notes:
        root.add_note(note)

    for override in meta_data:
        node = resolver.get(root, override.path)
        node.update(override.to_dict())

    return root


def render_index(root: anytree.Node, title: str, header: str,
                 template: jinja2.Template, out: IO[str]) -> None:
    """Render notebook tree into index.rst."""
    ctx = {
        'title':
        title,
        'header':
        header,
        'nodes': [
            node for node in anytree.PreOrderIter(root)
            if node.depth and not node.is_leaf
        ]
    }

    out.write(template.render(ctx))


def render_note(template: jinja2.Template, out: IO[str]) -> None:
    """Render a single note for export."""
    note_id = get_target()
    out.write(template.render(note_id=note_id))
