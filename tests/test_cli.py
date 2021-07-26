# stdlib
import os
import shutil
from typing import List

# 3rd party
import pytest
from coincidence.regressions import AdvancedFileRegressionFixture
from consolekit.testing import CliRunner

# this package
from pychoosealicense.__main__ import main


@pytest.mark.parametrize(
		"extra_args",
		[pytest.param([], id=''), pytest.param(["--verbose"], id="verbose")],
		)
@pytest.mark.parametrize("terminal_width", [30, 80, 120, 200])
def test_cli(
		identifier: str,
		terminal_width: int,
		cli_runner: CliRunner,
		advanced_file_regression: AdvancedFileRegressionFixture,
		monkeypatch,
		extra_args: List[str]
		):

	monkeypatch.setattr(
			shutil,
			"get_terminal_size",
			lambda *args, **kwargs: os.terminal_size((terminal_width, 24)),
			)

	result = cli_runner.invoke(main, args=[identifier, "--no-colour", *extra_args])

	result.check_stdout(advanced_file_regression, extension=".md")
	assert result.exit_code == 0
