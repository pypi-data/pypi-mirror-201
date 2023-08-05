import datetime
import shutil
from collections.abc import Iterable
from pathlib import Path
from pprint import pprint
from unittest import TestCase

from bx_py_utils.path import assert_is_file

import manageprojects
from manageprojects.utilities.pyproject_toml import toml_load


PROJECT_PATH = Path(manageprojects.__file__).parent.parent
GIT_BIN_PARENT = Path(shutil.which('git')).parent


class BaseTestCase(TestCase):
    maxDiff = None

    def assert_toml(self, path: Path, expected: dict):
        got = toml_load(path)
        try:
            self.assertDictEqual(got, expected)
        except AssertionError:
            print('-' * 79)
            pprint(got)
            print('-' * 79)
            raise

    def assert_datetime_range(
        self, dt: datetime.datetime, reference: datetime.datetime, max_diff_sec: int = 5
    ):
        self.assertEqual(dt.tzinfo, reference.tzinfo)
        diff = datetime.timedelta(seconds=max_diff_sec)
        min_dt = reference - diff
        max_dt = reference + diff
        self.assertLessEqual(dt, max_dt)
        self.assertGreaterEqual(dt, min_dt)

    def assert_datetime_now_range(self, dt: datetime.datetime, max_diff_sec: int = 5):
        now = datetime.datetime.now(tz=dt.tzinfo)
        self.assert_datetime_range(dt=dt, reference=now, max_diff_sec=max_diff_sec)

    def assert_content(self, got: str, expected: str, strip=True):
        if strip:
            got = got.strip()
            expected = expected.strip()

        try:
            self.assertEqual(got, expected)
        except AssertionError:
            print('-' * 79)
            print(got)
            print('-' * 79)
            raise

    def assert_in_content(self, *, got: str, parts: Iterable[str]):
        assert parts
        missing_parts = [part for part in parts if part not in got]
        if missing_parts:
            print('-' * 79)
            print(got)
            print('-' * 79)
            info = ', '.join(repr(part) for part in missing_parts)
            raise AssertionError(f'Text parts: {info} not found in: {got!r}')

    def assert_file_content(self, path: Path, content: str):
        assert_is_file(path)
        file_content = path.read_text().strip()
        self.assert_content(got=file_content, expected=content)
