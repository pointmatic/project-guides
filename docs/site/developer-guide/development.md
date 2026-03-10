# Development Setup

Guide for setting up a development environment for project-guides.

## Prerequisites

- Python 3.11 or higher
- Git
- pip or pipx

## Clone the Repository

```bash
git clone https://github.com/pointmatic/project-guides.git
cd project-guides
```

## Set Up Virtual Environment

### Using venv

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### Using pyenv

```bash
pyenv virtualenv 3.11 project-guides
pyenv activate project-guides
```

## Install Development Dependencies

```bash
pip install -e ".[dev,docs]"
```

This installs:
- The package in editable mode
- Development dependencies (pytest, ruff, mypy)
- Documentation dependencies (mkdocs-material)

## Verify Installation

```bash
# Check package is installed
project-guides --version

# Run tests
pytest

# Check linting
ruff check .

# Check types
mypy project_guides
```

## Development Workflow

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Changes

Edit files in `project_guides/` or `tests/`

### 3. Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=project_guides

# Run specific test file
pytest tests/test_cli.py

# Run specific test
pytest tests/test_cli.py::test_init_command
```

### 4. Check Code Quality

```bash
# Lint code
ruff check .

# Format code
ruff format .

# Type check
mypy project_guides
```

### 5. Update Documentation

If you changed user-facing functionality:

```bash
# Edit documentation
vim docs/site/user-guide/commands.md

# Build and preview
mkdocs serve
# Open http://127.0.0.1:8000
```

### 6. Commit Changes

```bash
git add .
git commit -m "Add feature: description"
```

## Project Structure

### Main Package

```
project_guides/
├── __init__.py           # Package initialization
├── __main__.py           # CLI entry point
├── cli.py                # CLI commands implementation
├── config.py             # Configuration model
├── sync.py               # Guide synchronization logic
├── version.py            # Version information
└── templates/            # Bundled templates
    └── guides/           # Workflow guides
        ├── project-guide.md
        ├── best-practices-guide.md
        ├── debug-guide.md
        └── documentation-setup-guide.md
```

### Tests

```
tests/
├── __init__.py
├── test_cli.py           # CLI command tests
├── test_config.py        # Configuration tests
├── test_sync.py          # Sync logic tests
└── test_integration.py   # Integration tests
```

### Documentation

```
docs/
├── guides/               # Developer guides
├── site/                 # MkDocs documentation
│   ├── getting-started/
│   ├── user-guide/
│   ├── developer-guide/
│   └── about/
└── specs/                # Specifications
    ├── features.md
    ├── tech-spec.md
    └── stories.md
```

## Running Tests

### Basic Test Run

```bash
pytest
```

### With Coverage Report

```bash
pytest --cov=project_guides --cov-report=html
open htmlcov/index.html
```

### Verbose Output

```bash
pytest -v
```

### Stop on First Failure

```bash
pytest -x
```

### Run Specific Tests

```bash
# By file
pytest tests/test_cli.py

# By test name
pytest tests/test_cli.py::test_init_command

# By pattern
pytest -k "test_init"
```

## Code Quality Tools

### Ruff (Linter and Formatter)

```bash
# Check for issues
ruff check .

# Fix auto-fixable issues
ruff check --fix .

# Format code
ruff format .
```

### Mypy (Type Checker)

```bash
# Type check
mypy project_guides

# Strict mode
mypy --strict project_guides
```

## Building Documentation

### Local Development

```bash
# Serve with live reload
mkdocs serve

# Open http://127.0.0.1:8000
```

### Build Static Site

```bash
# Build to site/ directory
mkdocs build

# Build with strict mode (fail on warnings)
mkdocs build --strict
```

## Debugging

### Using pdb

Add breakpoint in code:

```python
import pdb; pdb.set_trace()
```

Run tests:

```bash
pytest tests/test_cli.py::test_init_command
```

### Using pytest debugging

```bash
# Drop into pdb on failure
pytest --pdb

# Drop into pdb on first failure
pytest -x --pdb
```

### Verbose CLI Output

```bash
# Run CLI with Python for better error messages
python -m project_guides init
```

## Common Tasks

### Add a New Command

1. Add command function in `project_guides/cli.py`
2. Add tests in `tests/test_cli.py`
3. Update documentation in `docs/site/user-guide/commands.md`
4. Run tests and linters

### Update a Guide Template

1. Edit file in `project_guides/templates/guides/`
2. Test with actual LLM
3. Update version in `project_guides/version.py` if needed
4. Document changes in `CHANGELOG.md`

### Add a New Guide

1. Create guide in `project_guides/templates/guides/`
2. Update `project_guides/sync.py` to include it
3. Add tests
4. Update documentation

## Troubleshooting

### Import Errors

Ensure package is installed in editable mode:

```bash
pip install -e .
```

### Test Failures

Check if dependencies are up to date:

```bash
pip install --upgrade -e ".[dev,docs]"
```

### Type Check Errors

Ignore specific errors if needed:

```python
# type: ignore[error-code]
```

## Next Steps

- [Contributing Guide](contributing.md) - Contribution guidelines
- [Testing Guide](testing.md) - Detailed testing information
