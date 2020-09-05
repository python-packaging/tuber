# Tuber

This project finds an easy way to find the root of a python project's repo.  It
relies on several common markers, like `.git` or `pyproject.toml` to determine
this.

```pycon
>>> from tuber import get_root
>>> get_root("/")
Traceback (most recent call last):
...
tuber.RootException: No root found before actual root
>>> get_root(".")
PosixPath("/path/to/repo")
```

# License

Tuber is copyright [Tim Hatch](https://timhatch.com/), and licensed under
the MIT license.  I am providing code in this repository to you under an open
source license.  This is my personal repository; the license you receive to
my code is from me and not from my employer. See the `LICENSE` file for details.
