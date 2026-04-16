# Copyright (c) 2026 Pointmatic
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tests for project_guide.runtime — should_skip_input and _require_setting."""

import inspect
import io
import types

import click
import pytest

from project_guide.runtime import _require_setting, _resolve_setting, should_skip_input


@pytest.fixture
def clean_env(monkeypatch):
    """Remove all env vars that should_skip_input consults.

    Every test in this file starts from a known baseline: neither
    PROJECT_GUIDE_NO_INPUT nor CI set. Individual tests opt in to setting
    them.
    """
    monkeypatch.delenv("PROJECT_GUIDE_NO_INPUT", raising=False)
    monkeypatch.delenv("CI", raising=False)
    return monkeypatch


@pytest.fixture
def tty_stdin(monkeypatch):
    """Force sys.stdin.isatty() to return True (interactive baseline)."""
    fake = io.StringIO("")
    fake.isatty = lambda: True  # type: ignore[method-assign]
    monkeypatch.setattr("sys.stdin", fake)
    return fake


# --- Explicit flag ---------------------------------------------------------


def test_flag_true_returns_true_regardless_of_env(clean_env, tty_stdin):
    """should_skip_input(True) wins even with nothing else set."""
    assert should_skip_input(True) is True


def test_flag_true_beats_tty(clean_env, monkeypatch):
    """Explicit flag overrides even a real interactive TTY."""
    fake = io.StringIO("")
    fake.isatty = lambda: True  # type: ignore[method-assign]
    monkeypatch.setattr("sys.stdin", fake)
    assert should_skip_input(True) is True


def test_flag_false_with_tty_and_no_env_returns_false(clean_env, tty_stdin):
    """Interactive baseline: nothing set, TTY stdin, no flag → False."""
    assert should_skip_input(False) is False


# --- PROJECT_GUIDE_NO_INPUT env var ---------------------------------------


@pytest.mark.parametrize("value", ["1", "true", "TRUE", "True", "yes", "YES", "on", "ON"])
def test_project_guide_no_input_truthy_values(clean_env, tty_stdin, value):
    """All documented truthy values trigger skip-input (case-insensitive)."""
    clean_env.setenv("PROJECT_GUIDE_NO_INPUT", value)
    assert should_skip_input(False) is True


@pytest.mark.parametrize("value", ["", "0", "false", "no", "off", "maybe"])
def test_project_guide_no_input_falsy_values_fall_through(clean_env, tty_stdin, value):
    """Non-truthy values fall through to the next signal (here: TTY → False)."""
    clean_env.setenv("PROJECT_GUIDE_NO_INPUT", value)
    assert should_skip_input(False) is False


def test_project_guide_no_input_unset_falls_through(clean_env, tty_stdin):
    """Unset env var falls through to the next signal."""
    # clean_env already deleted it; TTY fixture ensures the TTY fallback is False
    assert should_skip_input(False) is False


# --- CI env var ------------------------------------------------------------


def test_ci_env_var_triggers_skip(clean_env, tty_stdin):
    """CI=1 triggers skip-input when flag and PROJECT_GUIDE_NO_INPUT are not set."""
    clean_env.setenv("CI", "1")
    assert should_skip_input(False) is True


@pytest.mark.parametrize("value", ["true", "YES", "on"])
def test_ci_env_var_case_insensitive(clean_env, tty_stdin, value):
    clean_env.setenv("CI", value)
    assert should_skip_input(False) is True


def test_ci_env_var_falsy_falls_through(clean_env, tty_stdin):
    clean_env.setenv("CI", "0")
    assert should_skip_input(False) is False


# --- Non-TTY stdin ---------------------------------------------------------


def test_non_tty_stdin_triggers_skip(clean_env, monkeypatch):
    """Non-TTY stdin (pipe, redirect) returns True when nothing else is set."""
    fake = io.StringIO("")
    fake.isatty = lambda: False  # type: ignore[method-assign]
    monkeypatch.setattr("sys.stdin", fake)
    assert should_skip_input(False) is True


# --- Safety: None / closed stdin ------------------------------------------


def test_stdin_none_returns_true(clean_env, monkeypatch):
    """sys.stdin is None (some subprocess contexts) → treat as non-TTY."""
    monkeypatch.setattr("sys.stdin", None)
    assert should_skip_input(False) is True


def test_stdin_closed_returns_true(clean_env, monkeypatch):
    """A closed stdin raises ValueError on isatty() → treat as non-TTY."""
    fake = io.StringIO("")
    fake.close()
    monkeypatch.setattr("sys.stdin", fake)
    # StringIO.isatty() after close() raises ValueError — runtime must catch it
    assert should_skip_input(False) is True


# --- Priority order --------------------------------------------------------


def test_flag_beats_env(clean_env, monkeypatch):
    """Explicit flag=True wins even if all env vars say otherwise."""
    # Non-TTY would normally return True, but so would the flag, so distinguish
    # priority by setting flag=True while forcing a TTY — the result must still
    # be True. To prove flag > env, we set a falsy env (which alone would give
    # False under TTY) and pass flag=True.
    clean_env.setenv("PROJECT_GUIDE_NO_INPUT", "0")
    clean_env.setenv("CI", "0")
    fake = io.StringIO("")
    fake.isatty = lambda: True  # type: ignore[method-assign]
    monkeypatch.setattr("sys.stdin", fake)
    assert should_skip_input(True) is True


def test_env_beats_ci(clean_env, tty_stdin):
    """PROJECT_GUIDE_NO_INPUT=1 wins even when CI is also set to a falsy value.

    The semantic question here is: does PROJECT_GUIDE_NO_INPUT take priority
    over CI? Demonstrate by setting PROJECT_GUIDE_NO_INPUT=1 and CI=0 — if CI
    were checked first and short-circuited to False, we'd get False. The
    correct behavior is that PROJECT_GUIDE_NO_INPUT is checked first.
    """
    clean_env.setenv("PROJECT_GUIDE_NO_INPUT", "1")
    clean_env.setenv("CI", "0")
    assert should_skip_input(False) is True


def test_ci_beats_tty(clean_env, monkeypatch):
    """CI=1 wins even when stdin is a real TTY."""
    clean_env.setenv("CI", "1")
    fake = io.StringIO("")
    fake.isatty = lambda: True  # type: ignore[method-assign]
    monkeypatch.setattr("sys.stdin", fake)
    assert should_skip_input(False) is True


# --- _require_setting contract --------------------------------------------


def test_require_setting_raises_click_exception():
    """_require_setting raises click.ClickException (exit 1)."""
    with pytest.raises(click.ClickException) as excinfo:
        _require_setting("project name", "project-name", "PROJECT_GUIDE_PROJECT_NAME")
    # click.ClickException default exit code is 1
    assert excinfo.value.exit_code == 1


def test_require_setting_message_format():
    """Exact message format is part of the contract — do not change lightly."""
    with pytest.raises(click.ClickException) as excinfo:
        _require_setting("project name", "project-name", "PROJECT_GUIDE_PROJECT_NAME")
    assert excinfo.value.message == (
        "project name is required when --no-input is active. "
        "Provide via --project-name or PROJECT_GUIDE_PROJECT_NAME."
    )


# ---------------------------------------------------------------------------
# Story N.c — _resolve_setting
# ---------------------------------------------------------------------------

@pytest.fixture
def clean_resolve_env(monkeypatch):
    """Remove the test env var used by _resolve_setting tests."""
    monkeypatch.delenv("PG_TEST_SETTING", raising=False)
    return monkeypatch


def _cfg(key: str, value: object) -> object:
    """Return a SimpleNamespace acting as a Config with one attribute set."""
    return types.SimpleNamespace(**{key: value})


# --- Priority order ---------------------------------------------------------


@pytest.mark.parametrize("cli_val,env_val,cfg_val,expected", [
    (True,  "0",   False, True),   # CLI wins over env and config
    (None,  "1",   False, True),   # env wins over config (bool True)
    (None,  None,  True,  True),   # config wins over default (bool True)
    (None,  None,  None,  False),  # falls through to default (False)
])
def test_resolve_setting_bool_priority(clean_resolve_env, monkeypatch, cli_val, env_val, cfg_val, expected):
    """Priority chain: CLI > env > config > default for bool settings."""
    if env_val is not None:
        monkeypatch.setenv("PG_TEST_SETTING", env_val)
    config = _cfg("test_key", cfg_val) if cfg_val is not None else None
    result = _resolve_setting("test", cli_val, "PG_TEST_SETTING", "test_key", config, False)
    assert result is expected


# --- Full fallback chain ----------------------------------------------------


def test_resolve_setting_full_fallback_returns_default_bool(clean_resolve_env):
    """CLI=None, env unset, config key absent → bool default returned."""
    result = _resolve_setting("test", None, "PG_TEST_SETTING", "missing_key", None, False)
    assert result is False


def test_resolve_setting_full_fallback_returns_default_str(clean_resolve_env):
    """CLI=None, env unset, config key absent → str default returned."""
    result = _resolve_setting("test", None, "PG_TEST_SETTING", "missing_key", None, "default-val")
    assert result == "default-val"


# --- Bool env-var resolution ------------------------------------------------


@pytest.mark.parametrize("raw", ["1", "true", "yes", "on", "TRUE", "YES", "ON"])
def test_resolve_setting_truthy_env_returns_true(clean_resolve_env, monkeypatch, raw):
    """Recognised truthy strings → True for bool settings."""
    monkeypatch.setenv("PG_TEST_SETTING", raw)
    result = _resolve_setting("test", None, "PG_TEST_SETTING", "k", None, False)
    assert result is True


@pytest.mark.parametrize("raw", ["0", "false", "no", "off", ""])
def test_resolve_setting_falsy_env_returns_false(clean_resolve_env, monkeypatch, raw):
    """Unrecognised strings → False for bool settings."""
    monkeypatch.setenv("PG_TEST_SETTING", raw)
    result = _resolve_setting("test", None, "PG_TEST_SETTING", "k", None, False)
    assert result is False


# --- String resolution ------------------------------------------------------


def test_resolve_setting_env_returned_as_is_for_str(clean_resolve_env, monkeypatch):
    """For str settings, the env var value is returned raw."""
    monkeypatch.setenv("PG_TEST_SETTING", "my-project")
    result = _resolve_setting("test", None, "PG_TEST_SETTING", "k", None, "")
    assert result == "my-project"


def test_resolve_setting_config_key_returned_as_is_for_str(clean_resolve_env):
    """For str settings, the config value is returned raw."""
    config = _cfg("proj_name", "my-project")
    result = _resolve_setting("test", None, "PG_TEST_SETTING", "proj_name", config, "")
    assert result == "my-project"


# --- Contract test ----------------------------------------------------------


def test_resolve_setting_contract():
    """Function signature is stable — guards against accidental drift."""
    sig = inspect.signature(_resolve_setting)
    params = list(sig.parameters.keys())
    assert params == ["name", "cli_value", "env_var", "config_key", "config", "default"]
    # Return annotation exists and is a union type
    assert sig.return_annotation is not inspect.Parameter.empty
