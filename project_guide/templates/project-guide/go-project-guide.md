# Project-Guide — Calm the chaos of LLM-assisted coding

{{template "project-guide/src/_header-common.md"}}

{{template "{{mode_src_template}}"}}


---

## Step 0: Project Setup

Before writing any spec documents, handle project scaffolding:

### License

1. If a `LICENSE` file exists in the project root, read it and identify the license.
2. If no `LICENSE` file exists, create one based on the developer's preference.
3. Record the license identifier (SPDX format, e.g. `Apache-2.0`) — this will be used in `pyproject.toml` (or equivalent) and in file headers.

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
| **Typed** | If the project ships type stubs or a `py.typed` marker | Static `shields.io` badge |
| **Coverage** | If a coverage service is configured (Codecov, Coveralls) | Codecov/Coveralls badge URL |

Use dynamic badges from the package registry (e.g. `shields.io/pypi/...`) when the package is published. Before publication, use static `shields.io` badges or omit registry-dependent badges. Always include the **License** badge. Add badges proactively — do not wait for the developer to ask.

### CHANGELOG.md

Changelog approach depends on the development mode:

**For Velocity Mode Projects:**

Maintain a manual `CHANGELOG.md` file in the repository root following Keep a Changelog format.

**File Location and Naming:**
- File name: `CHANGELOG.md` (all caps, hyphen separator)
- Location: Repository root (same level as `README.md`, `LICENSE`)

**Header Format:**
```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
```

**Version Entry Format:**
```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- New features, capabilities, or files

### Changed
- Changes to existing functionality

### Fixed
- Bug fixes
```

**Guidelines:**
- Update `CHANGELOG.md` in the same commit as the version bump
- Each story with a version number should have a corresponding changelog entry
- Use standard categories: Added, Changed, Deprecated, Removed, Fixed, Security
- Omit empty categories
- Most recent versions at the top

**Note:** The `CHANGELOG.md` file can remain unimplemented until the project is released. For prototypes and early-stage projects, focus on getting the code working first. The changelog can be created retroactively before the first public release by reviewing git history and the `stories.md` file.

**For Production Mode Projects:**

Use **automated GitHub Releases** as the canonical changelog (configured in the CI/CD phase).

**Approach:**
- GitHub Actions automatically creates releases from version tags
- Release notes are auto-generated from merged PR titles
- No manual `CHANGELOG.md` maintenance required
- Users view changelog at `https://github.com/username/repo/releases`

**Optional:** Generate `CHANGELOG.md` from GitHub Releases API using tools like `github-changelog-generator` if a file-based changelog is desired for distribution.

**Rationale:** Automated GitHub Releases eliminate duplication, ensure consistency, and reduce maintenance overhead in production projects.

---

## Step 1: Features Document (`docs/specs/features.md`)

### Purpose

Define **what** the project does — requirements, inputs, outputs, behavior — without specifying **how** it is implemented. This is the source of truth for scope.

### Instructions for the LLM

Generate `docs/specs/features.md` with the following sections:

1. **Header** — `# features.md — <Project Name> (<Language>)`
2. **Overview** — one paragraph explaining the document's purpose and cross-references to `tech-spec.md` and `stories.md`
3. **Project Goal** — what the project does, broken into:
   - **Core Requirements** — the essential functionality
   - **Operational Requirements** — error handling, logging, configuration, etc.
   - **Quality Requirements** — deduplication, caching, rate limiting, etc.
   - **Usability Requirements** — who uses it and how (CLI, library, web, etc.)
   - **Non-goals** — what the project explicitly does not do
4. **Inputs** — required and optional inputs with examples
5. **Outputs** — file structures, data formats, schemas
6. **Functional Requirements** — numbered list of features with detailed behavior descriptions and edge cases
7. **Configuration** — config precedence, environment variables, config file format
8. **Testing Requirements** — minimum test coverage expectations
9. **Security and Compliance Notes** — if applicable
10. **Performance Notes** — concurrency, rate limiting, atomicity
11. **Acceptance Criteria** — definition of done for the whole project

### Approval Gate

Present the complete `features.md` to the developer. Do not proceed until the developer approves or requests changes. Iterate as needed.

---

## Step 2: Technical Specification (`docs/specs/tech-spec.md`)

### Purpose

Define **how** the project is built — architecture, module layout, dependencies, data models, API signatures, and cross-cutting concerns.

### Instructions for the LLM

Generate `docs/specs/tech-spec.md` with the following sections.

**Note:** The sections below are tailored for CLI tools and libraries. Adapt them to fit the project type:
- **Web apps**: Add sections for routing, database schema, API endpoints, deployment
- **Mobile apps**: Add sections for screen navigation, platform APIs, build targets
- **Data pipelines**: Add sections for data models, transformations, scheduling
- **Bash utilities**: May only need sections 1-6; skip data models and API design

**Standard Sections:**

1. **Header** — `# tech-spec.md — <Project Name> (<Language>)`
2. **Overview** — one paragraph with cross-references to `features.md` and `stories.md`
3. **Runtime & Tooling** — language version, package manager, linter, test runner, etc.
4. **Dependencies** — tables for runtime, optional, system, and development dependencies with purpose for each
5. **Package Structure** — full directory tree with one-line descriptions per file
6. **Filename Conventions** — naming rules for different file types (see below)
7. **Key Component Design** — for each major module:
   - Function/method signatures (with types)
   - Brief description of behavior
   - Edge cases handled
8. **Data Models** — full model definitions with field types and defaults
9. **Configuration** — settings model with all fields, types, defaults, and precedence rules
10. **CLI Design** — subcommands table, shared flags, exit codes (if applicable)
11. **Library API** — public API with usage examples (if applicable)
12. **Cross-Cutting Concerns** — retry strategy, rate limiting, logging, caching, atomic writes, etc.
13. **Testing Strategy** — unit tests, integration tests, and what each covers

### Filename Conventions

When generating the tech-spec.md, include a **Filename Conventions** section that establishes naming rules for the project. Use the following guidelines:

**General Rule:**
- Use **hyphens (`-`)** for word separation in most files
- Use **underscores (`_`)** only for language-specific conventions or internal modules

**Specific Rules by File Type:**

| File Type | Convention | Examples |
|-----------|------------|----------|
| **Documentation** (Markdown) | Hyphens | `getting-started.md`, `api-reference.md`, `project-guide.md` |
| **User-facing scripts** | Hyphens | `deploy-app.sh`, `run-tests.sh` |
| **Workflow files** | Hyphens | `deploy-docs.yml`, `run-tests.yml` |
| **Python modules** | Underscores (PEP 8) | `my_module.py`, `data_processor.py` |
| **Python packages** | Underscores (PEP 8) | `my_package/`, `utils/` |
| **Internal library scripts** | Underscores | `lib/backend_detect.sh`, `lib/utils.sh` |
| **JavaScript/TypeScript** | Hyphens or camelCase | `api-client.ts`, `dataProcessor.ts` (follow project convention) |
| **Configuration files** | Hyphens or dots | `mkdocs.yml`, `.gitignore`, `pyproject.toml` |

**Rationale:**
- **Hyphens** are URL-friendly, standard in Unix/Linux, and preferred by documentation tools (MkDocs, Jekyll, Hugo)
- **Underscores** follow language conventions (Python PEP 8) and are used for internal modules not exposed as URLs
- **Consistency** within each category is more important than uniformity across all files

**Project-Specific Guidance:**
- If the project generates web content (docs, static sites), prefer hyphens for all user-facing files
- If the project is a library, follow the language's standard conventions
- Document any exceptions or special cases in the tech spec

### Approval Gate

Present the complete `tech-spec.md` to the developer. Do not proceed until approved.

---

## Step 3: Stories Document (`docs/specs/stories.md`)

### Purpose

Break the project into an ordered sequence of small, independently completable stories grouped into phases. Each story has a checklist of concrete tasks.

### Instructions for the LLM

Generate `docs/specs/stories.md` following this exact format:

#### Document Header

```markdown
# stories.md — <Project Name> (<Language>)

<One paragraph describing the document. Mention that stories are organized by phase
and reference modules defined in `tech-spec.md`.>

<One paragraph explaining the numbering scheme (e.g. A.a, A.b) and version bumping
convention. Mention that stories with no code changes have no version number.
Mention the [Planned]/[Done] suffix convention.>

---
```

#### Phase Sections

Each phase is a `## Phase <Letter>: <Name>` heading followed by stories.

Recommended phase progression:

| Phase | Name | Purpose |
|-------|------|---------|
| A | Foundation | Hello world, project structure, core models, config, logging |
| B | Core Services | The main functional modules (one story per service) |
| C | Pipeline & Orchestration | Wiring services together, caching, concurrency, error handling |
| D | CLI & Library API | User-facing interfaces |
| E | Testing & Quality | Test suites, coverage, edge case tests |
| F | Documentation & Release | README, changelog, final testing, polish |
| G | CI/CD & Automation | GitHub Actions, coverage badges, release automation (if requested) |
| H | GitHub Pages Documentation | Public-facing documentation site (for production projects) |

Phases may be added, removed, or renamed to fit the project. Phase G (CI/CD) is only included if the developer answered "yes" to the CI/CD question in the prerequisites. Phase H (GitHub Pages) is optional and typically added for production projects that need public documentation - see `docs/guides/documentation-setup-guide.md` for the complete workflow.

#### Story Format

Each story follows this format:

```markdown
### Story <Phase>.<letter>: v<version> <Title> [Planned]

<Optional one-line description.>

- [ ] <Task 1>
  - [ ] <Subtask 1a>
  - [ ] <Subtask 1b>
- [ ] <Task 2>
- [ ] <Task 3>
```

**Example without version (documentation/polish story):**

```markdown
### Story F.b: Update Documentation [Planned]

Polish README and add usage examples.

- [ ] Update README with advanced examples
- [ ] Add troubleshooting section
- [ ] Review all docs for consistency
```

Rules:

- **Story ID**: `<Phase letter>.<lowercase letter>` — e.g. `A.a`, `A.b`, `B.a`
- **Version**: semver, bumped per story. Stories with no code changes omit the version.
- **Status suffix**: `[Planned]` initially, changed to `[Done]` when completed.
- **Checklist**: use `- [ ]` for planned tasks, `- [x]` for completed tasks. Subtasks are indented with two spaces.
- **First story** should always be a minimal "Hello World" (Story A.a) — the smallest
  possible runnable artifact proving the environment and package structure are wired up.
- **Second story** (A.b) should be an **end-to-end stack spike** — a throwaway script
  (in `scripts/`, not the package) that wires the full critical path together before
  any production modules are written. See `docs/guides/best-practices-guide.md` §
  "Hello World First — Spike Early, Spike Often" for the full principle and rationale.
- **Additional spikes** should be added as the first story of any phase that introduces
  a major new integration boundary (new API, new hardware backend, new async framework).
  Each spike gets its own story ID and version bump.
- **Homepage**: If a project homepage (e.g. `docs/index.html`) was created during the
  planning phase, include a task in the Hello World story to verify it is present and
  references the correct repository URL.
- **Each story** should be completable in a single session and independently verifiable.
- **Verification tasks** (e.g. "Verify: command prints version") should be included where appropriate.

### Approval Gate

Present the complete `stories.md` to the developer. Do not proceed until approved.

---

## Step 4: Implementation

Once all three documents are approved, begin implementing stories in order:

1. **Start with Story A.a** (Hello World).
2. For each story:
   a. Read the story's checklist.
   b. Implement all tasks.
   c. Add the copyright/license header to every new source file.
   d. Run tests if applicable.
   e. Mark checklist items as `[x]` and change the story suffix to `[Done]`.
   f. Bump the version in the package manifest and source (if the story has a version).
   g. Present the completed story to the developer for approval.
3. **Pause after each story.** Do not proceed to the next story until the developer says "proceed" (or equivalent like "continue", "next", "go ahead"). This is a hard gate — never auto-advance.
4. **If unclear which story is next**, ask the developer: "Which story should I work on next?" or "Should I proceed with Story X.y?"

### File Header Reminder

Every new source file created during implementation must include the copyright and license header as the very first content in the file (before any code, docstrings, or imports).

---

## Summary

| Step | Action | Gate |
|------|--------|------|
| 0 | Set up LICENSE, determine header format | Developer confirms license |
| 1 | Write `docs/specs/features.md` | Developer approves |
| 2 | Write `docs/specs/tech-spec.md` | Developer approves |
| 3 | Write `docs/specs/stories.md` | Developer approves |
| 4 | Implement stories one by one | Developer approves each story |

---

## Debugging and Maintenance

Once the project is implemented and in use, bugs may be discovered. For a structured approach to debugging:

- See `docs/guides/debug_guide.md` for test-driven debugging methodology
- Always write a failing test before implementing a fix
- Document fixes as new stories in `stories.md`