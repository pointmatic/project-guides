# Override Management

Learn how to effectively manage file overrides to balance customization with receiving updates.

## Understanding Overrides

An override tells project-guide: "I've customized this file -- don't update it automatically."

### Why Overrides Matter

- **Preserve customizations**: Your project-specific changes won't be overwritten
- **Selective updates**: Update some files while keeping others locked
- **Hash tracking**: Know which content version you customized from

## Override Lifecycle

### 1. Customize a File

Edit the file to add project-specific content:

```bash
vim docs/project-guide/templates/modes/debug-mode.md
# Add your customizations
```

### 2. Mark as Overridden

Tell project-guide not to update this file. Both arguments are positional:

```bash
project-guide override templates/modes/debug-mode.md "Added team workflow steps"
```

### 3. Continue Updating Others

Other files still receive updates:

```bash
project-guide update
# Only non-overridden files are updated
```

### 4. Review New Versions (Optional)

Periodically check what's new:

```bash
# Force update creates .bak.<timestamp> backup
project-guide update --force

# Compare versions
diff docs/project-guide/templates/modes/debug-mode.md \
     docs/project-guide/templates/modes/debug-mode.md.bak.*
```

### 5. Decide: Keep or Adopt

Either keep your override or adopt the new version:

```bash
# Keep override (restore from backup)
mv docs/project-guide/templates/modes/debug-mode.md.bak.<timestamp> \
   docs/project-guide/templates/modes/debug-mode.md

# Or adopt new version (remove override)
project-guide unoverride templates/modes/debug-mode.md
```

## Override Strategies

### Strategy 1: Override Heavily Customized Files

**Use case**: Files with significant project-specific content

```bash
# Customize for your project
vim docs/project-guide/templates/modes/debug-mode.md
# Add company-specific sections, remove irrelevant parts

# Lock it
project-guide override templates/modes/debug-mode.md \
  "Customized for company workflow and security requirements"
```

**Pros**: Preserves all customizations
**Cons**: Misses workflow improvements

### Strategy 2: Minimal Overrides, Frequent Reviews

**Use case**: Want to receive most updates

```bash
# Only override when absolutely necessary
# Periodically review new versions
project-guide update --force
diff docs/project-guide/templates/modes/*.md \
     docs/project-guide/templates/modes/*.md.bak.*

# Merge improvements manually
```

**Pros**: Receives workflow improvements
**Cons**: Requires manual merging

### Strategy 3: Hybrid Approach

**Use case**: Balance customization and updates

```bash
# Override files with project-specific content
project-guide override templates/modes/debug-mode.md "Custom debug workflow"

# Keep general files up-to-date
project-guide update
```

**Pros**: Best of both worlds
**Cons**: Requires thoughtful decisions

## Best Practices

### 1. Document Override Reasons

Always provide a clear reason:

```bash
project-guide override templates/modes/debug-mode.md \
  "Added sections for: internal APIs, security review process, deployment checklist"
```

This helps future you (and teammates) understand why.

### 2. Review Overrides Periodically

Set a reminder to review overrides:

```bash
# Monthly or quarterly
project-guide overrides
# Review each override: still needed?
```

### 3. Keep Override List Short

Only override when necessary:

- Project-specific workflow steps
- Company security requirements
- Custom tool integrations
- NOT minor wording preferences
- NOT formatting changes
- NOT typo fixes (contribute upstream instead)

### 4. Use Version Control

Track override decisions in git:

```bash
# After overriding
git add .project-guide.yml docs/project-guide/
git commit -m "Override debug-mode.md: added internal deployment steps"
```

Note: `.bak` files are gitignored and will not be committed.

### 5. Team Communication

For team projects:

- Document overrides in README or CONTRIBUTING.md
- Discuss override decisions in team meetings
- Share override reasons in commit messages

## Common Scenarios

### Scenario 1: Adding Project-Specific Steps

**Problem**: Need to add steps specific to your project

**Solution**:
```bash
# Edit file
vim docs/project-guide/templates/modes/debug-mode.md
# Add section: "## Our Project Setup"

# Override
project-guide override templates/modes/debug-mode.md \
  "Added project-specific setup steps"
```

### Scenario 2: Removing Irrelevant Sections

**Problem**: File includes sections that don't apply

**Solution**:
```bash
# Edit file
vim docs/project-guide/templates/modes/debug-mode.md
# Remove sections that don't apply

# Override
project-guide override templates/modes/debug-mode.md \
  "Removed sections not applicable to our stack"
```

### Scenario 3: Integrating Internal Tools

**Problem**: Need to reference internal tools/systems

**Solution**:
```bash
# Edit file
vim docs/project-guide/developer/setup.md
# Add references to internal CI/CD, code review tools

# Override
project-guide override developer/setup.md \
  "Integrated with internal tools: Jenkins, Gerrit, Artifactory"
```

### Scenario 4: Accidentally Overrode

**Problem**: Marked file as overridden by mistake

**Solution**:
```bash
# Remove override
project-guide unoverride templates/modes/debug-mode.md

# Update to latest
project-guide update
```

### Scenario 5: Want to See New Version

**Problem**: File is overridden but want to see what's new

**Solution**:
```bash
# Force update (creates .bak.<timestamp> backup)
project-guide update --force

# Compare
diff docs/project-guide/templates/modes/debug-mode.md \
     docs/project-guide/templates/modes/debug-mode.md.bak.*

# Decide what to do
# Option A: Keep override (restore backup)
mv docs/project-guide/templates/modes/debug-mode.md.bak.<timestamp> \
   docs/project-guide/templates/modes/debug-mode.md

# Option B: Merge manually
# (edit file to incorporate new improvements)

# Option C: Adopt new version (remove override)
project-guide unoverride templates/modes/debug-mode.md
```

## Override Metadata

Overrides are stored in `.project-guide.yml`:

```yaml
overrides:
  templates/modes/debug-mode.md:
    reason: "Added team-specific debugging steps"
    locked_version: "a3f8c2e1"
    last_updated: "2026-03-15T10:30:00Z"
  developer/setup.md:
    reason: "Customized for our internal toolchain"
    locked_version: "b7d4e9f0"
    last_updated: "2026-04-01T14:20:00Z"
```

### Fields

- `reason`: Why the file was overridden (required, positional arg)
- `locked_version`: Content hash when the file was overridden
- `last_updated`: Timestamp of when the override was created

## Advanced: Selective Merging

For advanced users who want to merge improvements:

```bash
# 1. Force update to get latest
project-guide update --force

# 2. Compare your version with the new one
# Your customized version is backed up as .bak.<timestamp>
# The new version is now the current file

# 3. Manually merge
vim docs/project-guide/templates/modes/debug-mode.md
# Incorporate improvements while keeping customizations

# 4. Keep override
# (already overridden, no action needed)
```

## Next Steps

- [Commands Reference](commands.md) - Detailed command documentation
- [Workflow Guide](workflow.md) - See overrides in action
- [Configuration](configuration.md) - Understand configuration
