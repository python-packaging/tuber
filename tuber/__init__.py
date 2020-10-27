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


if __name__ == "__main__":  # pragma: no cover
    print(get_root())
