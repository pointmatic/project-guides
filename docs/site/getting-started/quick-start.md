# Quick Start

Get up and running with project-guides in minutes.

## 1. Install

Install project-guides using pip or pipx:

```bash
pip install project-guides
```

Or for system-wide access:

```bash
pipx install project-guides
```

## 2. Initialize Your Project

Navigate to your project directory and initialize project-guides:

```bash
cd /path/to/your/project
project-guides init
```

This creates:
- `docs/guides/` directory with all workflow guides
- `.project-guides.yml` configuration file

## 3. Start Collaborating with Your LLM

Tell your LLM to read the project guide and begin:

```
Read `docs/guides/project-guide.md` and start.
```

The guide will walk your LLM through:
1. Creating planning documents (features.md, tech-spec.md, stories.md)
2. Breaking work into stories and tasks
3. Implementing each story step-by-step

## 4. Guide the Workflow

As the LLM completes each step, simply say:

```
proceed
```

You stay in charge—directing features, flow, and taste—while the LLM handles the typing.

## HITLoop Development

This is "HITLoop" (human-in-the-loop) development:
- **You direct**: Features, architecture, priorities
- **LLM executes**: Planning, coding, testing, documentation
- **Pace**: Production-ready backends in 6-12 hours

## Managing Customizations

### Override a Guide

When you customize a guide for your project:

```bash
project-guides override project-guide.md
```

This marks the guide as overridden, preventing future updates from overwriting your changes.

### Update Non-Overridden Guides

Pull the latest workflow improvements:

```bash
project-guides update
```

This updates all non-overridden guides to the latest versions.

### Check Status

See which guides are current, outdated, or overridden:

```bash
project-guides status
```

## Next Steps

- [Commands Reference](../user-guide/commands.md) - Learn all available commands
- [Workflow Guide](../user-guide/workflow.md) - Understand the complete workflow
- [Configuration](configuration.md) - Customize project-guides behavior
- [Override Management](../user-guide/overrides.md) - Master the override system
