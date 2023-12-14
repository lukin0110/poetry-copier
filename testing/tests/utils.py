"""Test utilities."""

import os
from pathlib import Path


def assert_paths(directory: str, paths: set[str]) -> None:
    """Check if the given set of paths exist in the specified directory.

    Parameters
    ----------
    directory : str
        The directory in which to check for the paths.
    paths : set[str]
        A set of relative file paths to check for in the directory.

    Raises
    ------
    AssertionError
        If any of the paths in the set are not found in the directory.
    """
    tree = set()
    for root, _, files in os.walk(directory):
        for file in files:
            relative_path = os.path.relpath(Path(root) / file, directory)
            tree.add(relative_path)

    if tree != paths:
        diff1, diff2 = paths - tree, tree - paths
        msg = [f"Asserted but not in tree: {diff1}."] if diff1 else []
        msg += [f"In tree but not asserted: {diff2}."] if diff2 else []
        raise AssertionError(" ".join(msg))
