# Default Mode -- Getting Started

This is the default mode for new projects. It walks through the full project lifecycle: setup, planning, and implementation. For focused work, switch to a specific mode with `project-guide mode <name>`.

---

## Step 0: Project Setup

Before writing any spec documents, handle project scaffolding:

### License

1. If a `LICENSE` file exists in the project root, read it and identify the license.
2. If no `LICENSE` file exists, create one based on the developer's preference.
3. Record the license identifier (SPDX format, e.g. `Apache-2.0`) -- this will be used in `pyproject.toml` (or equivalent) and in file headers.

### Copyright and License Header

Every source file in the project must carry a standard copyright and license header. The header format depends on the license and the file's comment syntax.

**Example for Apache-2.0 in a Python file:**

```python
# Copyright (c) <year> <copyright holder>
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
```

**Example for MIT in a Python file:**

```python
# Copyright (c) <year> <copyright holder>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction. See the LICENSE file for details.
```

Adapt the comment syntax for the file type (`#` for Python/Shell, `//` for JS/TS/Go, `<!-- -->` for HTML/XML, etc.).

### Project Metadata

When creating the project's package manifest (e.g. `pyproject.toml`, `package.json`, `Cargo.toml`):

- The `license` field must match the `LICENSE` file (use the SPDX identifier).
- Include the copyright holder in the authors/maintainers field.

### README Badges

When a `README.md` is created or updated, include all applicable badges at the top of the file (below the project title). Choose from the following based on what applies to the project:

| Badge | When to include | Example source |
|-------|----------------|----------------|
| **CI status** | If CI is configured (GitHub Actions, etc.) | GitHub Actions badge URL |
| **Package version** | If published to a registry (PyPI, npm, crates.io) | `shields.io/pypi/v/...` |
| **Language version** | If the package specifies supported versions | `shields.io/pypi/pyversions/...` |
| **License** | Always (if a LICENSE file exists) | `shields.io/pypi/l/...` or `shields.io/github/license/...` |
| **Coverage** | If a coverage service is configured (Codecov, Coveralls) | Codecov/Coveralls badge URL |

Always include the **License** badge. Add badges proactively.

### CHANGELOG.md

Maintain a manual `CHANGELOG.md` file in the repository root following [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) format.

**Header Format:**
```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
```

**Guidelines:**
- Update `CHANGELOG.md` in the same commit as the version bump
- Use standard categories: Added, Changed, Deprecated, Removed, Fixed, Security
- Most recent versions at the top

---

## Step 1: Concept Document

Define the problem and solution space. Switch to concept mode for detailed guidance:

```bash
project-guide mode plan_concept
```

**Output:** `docs/specs/concept.md`

---

## Step 2: Features Document

Define what the project does -- requirements, inputs, outputs, behavior.

```bash
project-guide mode plan_features
```

**Output:** `docs/specs/features.md`

---

## Step 3: Technical Specification

Define how the project is built -- architecture, modules, dependencies.

```bash
project-guide mode plan_tech_spec
```

**Output:** `docs/specs/tech-spec.md`

---

## Step 4: Stories Document

Break the project into phases and stories with checklists.

```bash
project-guide mode plan_stories
```

**Output:** `docs/specs/stories.md`

---

## Step 5: Implementation

Implement stories one at a time. Switch to a coding mode:

```bash
project-guide mode code_velocity    # Fast iteration, direct commits
project-guide mode code_test_first  # TDD workflow
```

---

## Summary

| Step | Action | Mode |
|------|--------|------|
| 0 | Project setup (LICENSE, headers, badges) | default |
| 1 | Write concept document | `plan_concept` |
| 2 | Write features document | `plan_features` |
| 3 | Write technical specification | `plan_tech_spec` |
| 4 | Write stories document | `plan_stories` |
| 5 | Implement stories | `code_velocity` or `code_test_first` |

---

## Other Modes

| Mode | Use for |
|------|---------|
| `debug` | Test-driven debugging |
| `plan_phase` | Add a new phase to an existing project |
| `document_brand` | Generate project branding and descriptions |
| `document_landing` | Generate GitHub Pages landing page and MkDocs docs |
