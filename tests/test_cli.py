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

from pathlib import Path

import pytest
from click.testing import CliRunner

from project_guides.cli import main
from project_guides.config import Config


@pytest.fixture
def runner():
    """Create a Click CLI test runner."""
    return CliRunner()


def test_init_in_empty_directory(runner, tmp_path):
    """Test init command in an empty directory."""
    with runner.isolated_filesystem(temp_dir=tmp_path):
        result = runner.invoke(main, ['init'])
        
        assert result.exit_code == 0
        assert "Initializing project-guides" in result.output
        assert "Successfully initialized" in result.output
        
        # Verify config file was created
        assert Path(".project-guides.yml").exists()
        
        # Verify guides were created
        assert Path("docs/guides/project-guide.md").exists()
        assert Path("docs/guides/debug-guide.md").exists()
        assert Path("docs/guides/developer/codecov-setup-guide.md").exists()


def test_init_with_existing_config_error(runner, tmp_path):
    """Test that init errors when config already exists."""
    with runner.isolated_filesystem(temp_dir=tmp_path):
        # First init
        result = runner.invoke(main, ['init'])
        assert result.exit_code == 0
        
        # Second init without force should fail
        result = runner.invoke(main, ['init'])
        assert result.exit_code == 1
        assert "already exists" in result.output


def test_init_with_force_flag(runner, tmp_path):
    """Test init with --force flag overwrites existing files."""
    with runner.isolated_filesystem(temp_dir=tmp_path):
        # First init
        result = runner.invoke(main, ['init'])
        assert result.exit_code == 0
        
        # Modify a guide
        guide_path = Path("docs/guides/project-guide.md")
        original_content = guide_path.read_text()
        guide_path.write_text("Modified content")
        
        # Second init with force
        result = runner.invoke(main, ['init', '--force'])
        assert result.exit_code == 0
        
        # Verify file was overwritten
        assert guide_path.read_text() == original_content


def test_init_with_custom_target_dir(runner, tmp_path):
    """Test init with custom --target-dir."""
    with runner.isolated_filesystem(temp_dir=tmp_path):
        result = runner.invoke(main, ['init', '--target-dir', 'custom/path'])
        
        assert result.exit_code == 0
        assert Path("custom/path/project-guide.md").exists()
        
        # Verify config has correct target_dir
        config = Config.load(".project-guides.yml")
        assert config.target_dir == "custom/path"
