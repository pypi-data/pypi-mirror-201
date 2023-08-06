#!/usr/bin/env python3

import os
from typing import List

import pytest
from click.testing import CliRunner
from pip_preserve.cli import cli


class TestPIPRequirements:
    """Test reconstructing requirements."""

    DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    _PREAMBLE_LINES = 3

    @pytest.mark.parametrize("env,requirements_file,cli_args", [
        (os.path.join(DATA_DIR, "env01"), "requirements.txt", []),
        (os.path.join(DATA_DIR, "env01"), "requirements_direct_url.txt", ["--direct-url"]),
    ])
    def test_env(self, env: str, requirements_file: str, cli_args: List[str]) -> None:
        """Test reconstructing requirements from an environment."""
        with open(os.path.join(env, requirements_file)) as f:
            expected = f.read()

        runner = CliRunner(mix_stderr=False)
        result = runner.invoke(cli, ["--site-packages", os.path.join(env, "site-packages")] + cli_args)
        assert result.exit_code == 0

        lines = result.output.splitlines()[self._PREAMBLE_LINES:]
        expected_lines = expected.splitlines()[self._PREAMBLE_LINES:]
        assert lines == expected_lines

    def test_env_empty(self) -> None:
        """Test failure in reconstructing requirements from an environment."""
        runner = CliRunner()
        env = os.path.join(self.DATA_DIR, "empty")
        result = runner.invoke(cli, ["--site-packages", env])
        assert result.exit_code != 0

    def test_ignore_errors(self) -> None:
        """Test passing ignore errors."""
        runner = CliRunner()
        env = os.path.join(self.DATA_DIR, "env02", "site-packages")

        result = runner.invoke(cli, ["--site-packages", env])
        assert result.exit_code != 0

        result = runner.invoke(cli, ["--site-packages", env, "--ignore-errors"])
        assert result.exit_code == 0

        with open(os.path.join(self.DATA_DIR, "env02", "requirements.txt")) as f:
            expected = f.read()

        lines = result.output.splitlines()[self._PREAMBLE_LINES:]
        expected_lines = expected.splitlines()[self._PREAMBLE_LINES:]
        assert lines == expected_lines

