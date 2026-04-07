# Default Mode — determining which mode to use

## Prerequisites

Before starting, the developer must provide (or the LLM must ask):

1. **A project idea** — a short description of what the project should do (a few sentences to a few paragraphs). This is often documented in a `docs/specs/concept.md` file.
2. **Language / runtime** — e.g. Python 3.14, Node 22, Go 1.23, etc.
3. **License preference** — e.g. Apache-2.0, MIT, MPL-2.0, GPL-3.0. If a `LICENSE` file already exists in the project root, that license prevails.

The developer may optionally provide:

- Preferred frameworks, libraries, or tools
- Constraints (no UI, no database, must run offline, etc.)
- Target audience (CLI tool, library, web app, etc.)

Additionally, the LLM should ask the developer the following question **after the tech spec is approved but before writing the stories document**:

> **Will this project need CI/CD automation?** For example: GitHub Actions for linting/testing on every push, dynamic code coverage badges (Codecov/Coveralls), and/or automated publishing to a package registry (PyPI, npm, etc.) on tagged releases?

If the answer is yes, the stories document should include a dedicated phase (typically the last phase) covering:

- **CI workflow** — GitHub Actions (or equivalent) running lint, type-check, and tests on push/PR, with a Python/Node/etc. version matrix.
- **Coverage reporting** — uploading coverage to a service like Codecov and adding a dynamic badge to the README.
- **Release automation** — publishing to the package registry on version tags, preferably using trusted publishing (OIDC) to avoid storing API tokens.

If the answer is no, skip this phase entirely.

