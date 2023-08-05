import subprocess

from bx_py_utils.path import assert_is_file
from packaging.version import Version

from manageprojects import __version__
from manageprojects.cli.cli_app import PACKAGE_ROOT
from manageprojects.test_utils.click_cli_utils import subprocess_cli
from manageprojects.test_utils.project_setup import check_editor_config, get_py_max_line_length
from manageprojects.tests.base import BaseTestCase
from manageprojects.utilities import code_style


class ProjectSetupTestCase(BaseTestCase):
    def test_version(self):
        self.assertIsNotNone(__version__)

        version = Version(__version__)  # Will raise InvalidVersion() if wrong formatted
        self.assertEqual(str(version), __version__)

        cli_bin = PACKAGE_ROOT / 'cli.py'
        assert_is_file(cli_bin)

        output = subprocess.check_output([cli_bin, 'version'], text=True)
        self.assertIn(f'manageprojects v{__version__}', output)

    def test_code_style(self):
        cli_bin = PACKAGE_ROOT / 'cli.py'
        assert_is_file(cli_bin)

        try:
            output = subprocess_cli(
                cli_bin=cli_bin,
                args=('check-code-style',),
                exit_on_error=False,
            )
        except subprocess.CalledProcessError as err:
            self.assertIn('.venv/bin/darker', err.stdout)  # darker was called?
        else:
            if 'Code style: OK' in output:
                self.assertIn('.venv/bin/darker', output)  # darker was called?
                return  # Nothing to fix -> OK

        # Try to "auto" fix code style:

        try:
            output = subprocess_cli(
                cli_bin=cli_bin,
                args=('fix-code-style',),
                exit_on_error=False,
            )
        except subprocess.CalledProcessError as err:
            output = err.stdout

        self.assertIn('.venv/bin/darker', output)  # darker was called?

        # Check again and display the output:

        try:
            code_style.check(package_root=PACKAGE_ROOT)
        except SystemExit as err:
            self.assertEqual(err.code, 0, 'Code style error, see output above!')

    def test_check_editor_config(self):
        check_editor_config(package_root=PACKAGE_ROOT)

        max_line_length = get_py_max_line_length(package_root=PACKAGE_ROOT)
        self.assertEqual(max_line_length, 119)
