# Configuration

project-guide uses a simple YAML configuration file to store project-specific settings.

## Configuration File

The `.project-guide.yml` file is created automatically when you run `project-guide init`. It's stored in your project root.

### Default Configuration

```yaml
version: "2.0"
installed_version: "2.0.13"
target_dir: "docs/project-guide"
metadata_file: ".metadata.yml"
current_mode: "code_velocity"
overrides: {}
```

## Configuration Fields

### `version`

The configuration file format version. Currently `"2.0"`.

### `installed_version`

The version of the project-guide package that was used to install or last update the files. Used alongside content hashing to determine which files need updating.

### `target_dir`

The directory where project-guide files are installed. Defaults to `docs/project-guide`.

You can customize this:

```yaml
target_dir: "documentation/workflows"
```

### `metadata_file`

The name of the metadata file used to track file state. Defaults to `.metadata.yml`.

### `current_mode`

Tracks the active development mode. Changed via the `project-guide mode` command. project-guide includes 15 modes to match different development workflows.

### `overrides`

A mapping of template paths to override metadata. Managed automatically by the `override` and `unoverride` commands.

Example:

```yaml
overrides:
  templates/modes/debug-mode.md:
    reason: "Custom debugging workflow for our project"
    locked_version: "2.0.10"
    last_updated: "2026-03-15"
```

Override fields:

- `reason` -- Why the override was created
- `locked_version` -- The package version when the override was set
- `last_updated` -- When the override was last modified

## Zero Configuration

project-guide works out of the box with sensible defaults. You don't need to create or modify the configuration file manually unless you want to customize behavior.

## Custom Target Directory

To use a custom target directory, specify it during initialization:

```bash
project-guide init --target-dir custom/path
```

Or modify the configuration file:

```yaml
target_dir: "custom/path"
```

All commands will respect this setting.

## Content Hash Sync

project-guide uses content hashing (not version numbers) to track file state. This enables smart updates that:

- Detect exactly which files have changed upstream
- Only update non-overridden files
- Show which files are current, outdated, or overridden
- Preserve your customizations

## Manual Configuration

While not recommended, you can manually edit `.project-guide.yml` if needed. The file uses standard YAML syntax.

!!! warning
    Manual edits should be done carefully. Invalid YAML will cause commands to fail.

## Next Steps

- [Commands Reference](../user-guide/commands.md) - Learn all available commands
- [Override Management](../user-guide/overrides.md) - Understand the override system
- [Workflow Guide](../user-guide/workflow.md) - See configuration in action
