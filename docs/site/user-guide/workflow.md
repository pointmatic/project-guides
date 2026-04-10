# Workflow Guide

Learn how to use project-guide effectively in your LLM-assisted development workflow.

## The HITLoop Workflow

project-guide supports "HITLoop" (human-in-the-loop) development where:
- **You direct**: Features, architecture, priorities, taste
- **LLM executes**: Planning, coding, testing, documentation
- **Result**: Production-ready projects in 6-12 hours

## Initial Setup

### 1. Install project-guide

```bash
pip install project-guide
```

### 2. Initialize Your Project

```bash
cd /path/to/your/project
project-guide init
```

This creates:
- `docs/project-guide/` with all workflow files rendered from templates
- `docs/project-guide/go.md` as the LLM entry point
- `.project-guide.yml` configuration

### 3. Choose a Mode

project-guide ships with 15 modes for different workflows. Pick the one that fits:

```bash
# List all available modes
project-guide mode

# Switch to a mode
project-guide mode plan_concept
```

Switching modes re-renders `go.md` so the LLM sees the right workflow immediately.

### 4. Start the LLM Workflow

Tell your LLM:

```
Read `docs/project-guide/go.md` and start.
```

The guide walks the LLM through the steps defined by the active mode.

### 5. Guide Each Step

As the LLM completes steps, say:

```
go
```

You stay in control, approving each step before moving forward.

## Common Workflows

### Starting a New Project

```bash
# 1. Create project directory
mkdir my-project && cd my-project

# 2. Initialize git
git init

# 3. Install project-guide
pip install project-guide

# 4. Initialize files
project-guide init

# 5. Choose your mode
project-guide mode plan_concept

# 6. Start LLM collaboration
# Tell LLM: "Read `docs/project-guide/go.md` and start."
```

### Switching Modes Mid-Project

As your project evolves, switch modes to match the current phase:

```bash
# Finished planning, ready to build
project-guide mode code_velocity

# Need to track down a bug
project-guide mode debug

# Time to write documentation
project-guide mode documentation
```

Each switch re-renders `go.md` so the LLM picks up the new workflow.

### Adding Files to an Existing Project

```bash
# Navigate to project
cd existing-project

# Initialize project-guide
project-guide init

# Check status
project-guide status
```

### Updating Files Across Projects

```bash
# Update project-guide package
pip install --upgrade project-guide

# Update files in each project
cd project1
project-guide update

cd ../project2
project-guide update
```

### Customizing a File

```bash
# 1. Edit the file
vim docs/project-guide/templates/modes/debug-mode.md

# 2. Mark as overridden (positional args: file path, then reason)
project-guide override templates/modes/debug-mode.md "Added team-specific workflow"

# 3. Verify override
project-guide status
```

### Syncing Latest Improvements

Hash-based sync means only files whose content has actually changed are flagged:

```bash
# Check which files have changed
project-guide status

# Preview what would be updated
project-guide update --dry-run

# Update non-overridden files
project-guide update

# Review changes
git diff docs/project-guide/
```

## Multi-Project Management

### Keeping Files in Sync

When working on multiple projects:

1. **Update package globally** (if using pipx):
   ```bash
   pipx upgrade project-guide
   ```

2. **Update each project**:
   ```bash
   for project in project1 project2 project3; do
     cd $project
     project-guide update
     cd ..
   done
   ```

3. **Review changes**:
   ```bash
   git diff docs/project-guide/
   ```

### Managing Project-Specific Customizations

For files customized per project:

```bash
# Project A: Custom mode template
cd projectA
project-guide override templates/modes/debug-mode.md "Custom debugging workflow"

# Project B: Custom developer setup
cd ../projectB
project-guide override developer/setup.md "Internal toolchain references"

# Both: Update non-overridden files
project-guide update
```

## Override Management

### When to Override

Override a file when:
- You've customized it for your project's specific needs
- The file contains project-specific instructions
- You want to prevent updates from overwriting changes

### When NOT to Override

Don't override if:
- You want to receive workflow improvements
- The customization is minor (consider contributing upstream instead)
- You're just experimenting (test changes first)

### Reviewing Overridden Files

Periodically review overridden files:

```bash
# List all overrides
project-guide overrides

# Force update to see what's new (creates .bak.<timestamp> backups)
project-guide update --force
diff docs/project-guide/templates/modes/debug-mode.md \
     docs/project-guide/templates/modes/debug-mode.md.bak.*

# Decide: keep override or adopt new version
```

## Best Practices

### 1. Version Control

Always commit files to version control:

```bash
git add docs/project-guide/ .project-guide.yml
git commit -m "Initialize project-guide"
```

Note: `.bak` files are gitignored and will not be committed.

### 2. Document Overrides

Use a clear reason when overriding:

```bash
project-guide override templates/modes/debug-mode.md \
  "Added company-specific security requirements"
```

### 3. Regular Updates

Update files regularly to get improvements:

```bash
# Weekly or monthly
project-guide update
git diff docs/project-guide/
git commit -m "Update project-guide to latest"
```

### 4. Review Before Committing

Always review file updates before committing:

```bash
project-guide update
git diff docs/project-guide/
# Review changes, then commit
```

### 5. Team Coordination

For team projects:
- Document which files are overridden and why
- Share override decisions with the team
- Consider contributing improvements back to project-guide

## Troubleshooting

### Files Not Updating

Check if files are overridden:

```bash
project-guide status
project-guide overrides
```

### Accidental Override

Remove override to allow updates:

```bash
project-guide unoverride templates/modes/debug-mode.md
project-guide update
```

### Lost Customizations

If you updated with `--force`, restore from the timestamped backup:

```bash
# Find the backup
ls docs/project-guide/templates/modes/debug-mode.md.bak.*

# Restore it
mv docs/project-guide/templates/modes/debug-mode.md.bak.<timestamp> \
   docs/project-guide/templates/modes/debug-mode.md

# Re-override
project-guide override templates/modes/debug-mode.md "Restored customization"
```

## Next Steps

- [Commands Reference](commands.md) - Detailed command documentation
- [Override Management](overrides.md) - Master the override system
- [Configuration](configuration.md) - Customize behavior
