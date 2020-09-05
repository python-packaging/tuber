import os
import unittest
from pathlib import Path

import volatile

from tuber import get_root


class GetRootTest(unittest.TestCase):
    def test_invalid_dir_raises(self) -> None:
        with volatile.dir() as d:
            dp = Path(d)
            with self.assertRaisesRegex(ValueError, "missing is not a directory"):
                get_root(dp / "missing")

            (dp / "file").write_text("")
            with self.assertRaisesRegex(ValueError, "file is not a directory"):
                get_root(dp / "file")

            # This can be different depending on whether a tmpfs is used
            with self.assertRaisesRegex(
                ValueError, "No root found (before actual root|on same device)"
            ):
                get_root(dp)

            with self.assertRaisesRegex(
                ValueError, "No root found (before actual root|on same device)"
            ):
                get_root(Path("/"))

    def test_various_indicators(self) -> None:
        for ind in (".git", "pyproject.toml"):
            with volatile.dir() as d:
                dp = Path(d)
                # doesn't matter if it's a dir or file currently
                (dp / ind).write_text("")
                self.assertEqual(dp, get_root(dp))
                (dp / "x").mkdir()
                self.assertEqual(dp, get_root(dp / "x"))

    def test_optional_value(self) -> None:
        with volatile.dir() as d:
            dp = Path(d)
            # doesn't matter if it's a dir or file currently
            (dp / "pyproject.toml").write_text("")
            (dp / "x").mkdir()
            try:
                prev = os.getcwd()
                os.chdir(dp / "x")
                self.assertEqual(dp, get_root())
            finally:
                os.chdir(prev)
