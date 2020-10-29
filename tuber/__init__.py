import os
from fnmatch import fnmatch
from pathlib import Path
from typing import Iterable, Optional, Union

# This covers 99% of Python projects.  For simplicity, stop at the first one
# found.

DEFAULT_ROOT_INDICATORS = {
    ".git",
    ".hg",
    "pyproject.toml",
    "setup.cfg",
    "setup.py",
}

DEFAULT_INCLUDES = ["*.py"]

DEFAULT_EXCLUDES = [
    ".direnv",
    ".egg*",
    ".ext.py",
    ".git",
    ".hg",
    ".mypy_cache",
    ".nox",
    ".tox",
    ".venv",
    ".svn",
    "_build",
    "buck-out",
    "build",
    "dist",
]


class RootException(ValueError):
    pass


def get_root(
    path: Optional[Union[Path, str]] = None,
    root_indicators: Iterable[str] = DEFAULT_ROOT_INDICATORS,
) -> Path:
    if path is None:
        path = Path(".")
    if not isinstance(path, Path):
        path = Path(path)

    # Not guaranteed to return a substring of the passed-in path; this gives the
    # "correct" behavior in the presence of symlinks into a repo.
    path = path.resolve()
    if not path.is_dir():
        raise RootException(f"{path} is not a directory")

    while True:
        if any((path / x).exists() for x in root_indicators):
            return path
        parent = path.parent

        if parent == path:
            raise RootException("No root found before actual root")
        if parent.stat().st_dev != path.stat().st_dev:
            raise RootException("No root found on same device")
        path = parent


def walk(
    root: Path,
    includes: Iterable[str] = DEFAULT_INCLUDES,
    excludes: Iterable[str] = DEFAULT_EXCLUDES,
) -> Iterable[str]:
    """Generator that calls os.walk on a path and applies includes/excludes

    walk() uses fnmatch so Unix shell-style wildcards e.g. *, ?, [1-9] are supported.
    For more information on the wildcards see
    https://docs.python.org/3/library/fnmatch.html.
    Note, the patterns in includes/excludes are only applied to the filename itself,
    not the directories in the path. Additionally os.walk traverses directories in
    arbitrary order.
    """
    for dirpath, dirnames, filenames in os.walk(root):
        for filename in filenames:
            if not any([fnmatch(filename, pattern) for pattern in includes]):
                continue
            if any([fnmatch(filename, pattern) for pattern in excludes]):
                continue
            yield os.path.join(dirpath, filename)
        dirnames[:] = [
            d
            for d in dirnames
            if not any([fnmatch(d, pattern) for pattern in excludes])
        ]


if __name__ == "__main__":  # pragma: no cover
    print(get_root())
