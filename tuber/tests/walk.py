import os
import tempfile
import unittest
from pathlib import Path

from tuber import walk

INCLUDED_TEST_FILEPATHS = [
    "test.py",
    "abc/test2.py",
    "abc/def/test3.py",
    "ghi/test4.py",
]

EXCLUDED_TEST_FILEPATHS = [
    ".direnv" ".eggs" "abc/.ext.py" "abc/.git",
    "abc/.hg",
    "abc/.mypy_cache",
    "abc/def/.nox*",
    "abc/def/.tox",
    "abc/def/.venv",
    "abc/def/.svn",
    "ghi/_build",
    "ghi/buck-out*",
    "ghi/build*",
    "ghi/dist*",
]


class WalkTest(unittest.TestCase):
    @staticmethod
    def _make_empty_file(path: str) -> None:
        basedir = os.path.dirname(path)
        if not os.path.exists(basedir):
            os.makedirs(basedir)
        open(path, "a").close()

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        for relative_test_filepath in EXCLUDED_TEST_FILEPATHS + INCLUDED_TEST_FILEPATHS:
            absolute_test_filepath = os.path.join(
                self.temp_dir.name, relative_test_filepath
            )
            self._make_empty_file(absolute_test_filepath)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_inclusions_and_exclusions(self) -> None:
        temp_dir_path = Path(self.temp_dir.name)
        result_paths = list(walk(temp_dir_path))
        self.assertEqual(
            sorted(result_paths),
            sorted(
                [
                    os.path.join(temp_dir_path, test_file)
                    for test_file in INCLUDED_TEST_FILEPATHS
                ]
            ),
        )
