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

import click

from project_guides.version import __version__
from project_guides.config import Config
from project_guides.sync import get_all_guide_names, copy_guide


@click.group()
@click.version_option(version=__version__)
def main():
    """Manage LLM project guides across repositories."""
    pass


@main.command()
@click.option('--target-dir', default='docs/guides', help='Target directory for guides')
@click.option('--force', is_flag=True, help='Overwrite existing files')
def init(target_dir: str, force: bool):
    """Initialize guides in a new project."""
    config_path = Path(".project-guides.yml")
    
    # Check if config already exists
    if config_path.exists() and not force:
        click.secho(
            f"Error: {config_path} already exists. Use --force to overwrite.",
            fg='red',
            err=True
        )
        raise click.Abort()
    
    # Create target directory
    target_path = Path(target_dir)
    target_path.mkdir(parents=True, exist_ok=True)
    
    # Get all guide names
    guide_names = get_all_guide_names()
    
    # Copy all templates
    click.echo(f"Initializing project-guides v{__version__}...")
    click.secho(f"✓ Created {target_dir}/", fg='green')
    
    for guide_name in guide_names:
        try:
            copy_guide(guide_name, target_path, force=force)
            click.secho(f"✓ Installed {guide_name}", fg='green')
        except FileExistsError:
            if not force:
                click.secho(f"⚠ Skipped {guide_name} (already exists)", fg='yellow')
    
    # Create config file
    config = Config(
        version="1.0",
        installed_version=__version__,
        target_dir=target_dir
    )
    config.save(str(config_path))
    click.secho(f"✓ Created {config_path}", fg='green')
    
    click.echo(f"\nSuccessfully initialized {len(guide_names)} guides.")


if __name__ == "__main__":
    main()
