# stories.md -- project-guide (python)

This document breaks the `project-guide` project into an ordered sequence of small, independently completable stories grouped into phases. Each story has a checklist of concrete tasks. Stories are organized by phase and reference modules defined in `tech-spec.md`.

Stories with code changes include a version number (e.g., v0.1.0). Stories with only documentation or polish changes omit the version number. The version follows semantic versioning and is bumped per story. Stories are marked with `[Planned]` initially and changed to `[Done]` when completed.

For a high-level concept (why), see `concept.md`. For requirements and behavior (what), see `features.md`. For implementation details (how), see `tech-spec.md`. For project-specific must-know facts, see `project-essentials.md` (`plan_phase` appends new facts per phase).

---



## Future

### Change "code_velocity" to "code_direct" [Deferred]

"velocity" isn't the right word and doesn't pair well with "code_test_first". The "direct" mode should be the default mode for coding.

### Test First flag [Deferred]

Add a `--test-first` flag to the `init` command that causes coding to prefer `code_test_first` whenever `code_direct` would have been chosen as a next step. This involves abstracting out the `code_*` mode and paves the way for a future `code_production` mode.

### Code Production Mode [Deferred]

Implement the `code_production` mode...TBD

### Audit Modes [Deferred]

Future modes (deferred): `audit_security`, `audit_architecture`, `audit_performance`, `audit_best_practices`, `audit_modularity`, `audit_patterns`

### Out of Scope for Phase J

- Mode auto-detection from `files_exist` prerequisites (future advanced feature)
- Interactive mode menu (deferred — direct `mode <name>` argument is sufficient for v2.0.0)
- LLM API calls for artifact generation (future — currently the LLM fills in variables conversationally)
- Per-project metadata overrides in `.project-guide.yml` (future — metadata.yml is the single source for now)
- Migration tooling for `docs/guides/` → `docs/project-guide/` (future `refactor` mode)
- Story detection in `status` command (nice-to-have, can be added in a follow-up phase)
- Future modes: `code_production`, `audit_*`, `refactor_*`

## Out of Scope for Phase K

- Release helper / version-bump / tag automation — explicitly deferred (developer works across pure-git, GitHub-tag-triggered, and branch-flow setups and prefers to stay tool-agnostic for now).
- `code_production` mode and `code_*` abstraction (Test First flag) — deferred to a separate phase focused on the code mode hierarchy.
- Audit modes (`audit_security`, `audit_architecture`, etc.) — deferred.
- Automatic detection of "release just shipped" beyond the all-stories-`[Done]` heuristic.
- Migration tooling for old `stories.md` files that predate the `## Future` convention — assume existing files are well-formed or get fixed manually.
- A `status` command flag to trigger archive — not needed; the mode itself is the entry point.

## Out of Scope for Phase L

- **`--no-input` for other commands.** `purge` has a `click.confirm()`; `update` has modified-file prompts. Wiring them to `should_skip_input()` is trivial but not required by the pyve integration. A follow-up phase can sweep all commands once there is demand.
- **`--quiet` / output suppression.** The spec is explicit: `--no-input` only affects stdin. A separate `--quiet` flag for reducing stdout chatter from `_copy_template_tree` is a reasonable future request (pyve's subprocess captures all of that), but not this phase.
- **Config-file fallback for prompt values.** `init` has no prompts that need this today. When the first one appears, the pattern is: CLI flag → env var → `.project-guide.yml` key → default. FR-L4 already describes the required error path; the fallback mechanism lands with the first real prompt.
- **Legacy broken-state detection.** The "`.project-guide.yml` absent but target directory populated" state is unusual (partial install, manual deletion) and falls through to the existing copy-with-skip-warnings path. Not addressed by FR-L1.
- **Interactive mode inversion.** No `--interactive` flag to force interactive mode over a non-TTY default. If someone needs it, `stdin` can always be re-attached. Out of scope.

## Out of Scope for Phase M

- A dedicated `refactor_essentials` mode for editing `project-essentials.md` directly. Not needed — the three planning modes cover the lifecycle, and direct editing is always available via a normal text editor.
- A `create_or_modify` action type. Mode templates handle existence-checking conversationally instead. Revisit only if other artifacts develop the same need.
- Validation/linting of `project-essentials.md` content. The artifact is freeform by design.
- Auto-detection of stale essentials (e.g., comparing against last commit). Out of scope; the planning-mode prompts are the maintenance mechanism.
- Migrating other LLM memory entries into `project-essentials.md`. Per-project decision the developer makes when they first run an updated planning mode.
- Support for literal `{{ var }}` strings as rendered output (e.g., Jinja syntax docs). Documented as a known limitation of the M.b validator; bridge if/when a real template needs it.
