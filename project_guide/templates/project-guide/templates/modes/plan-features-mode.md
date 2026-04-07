# features.md -- {{ project_name }}

Define **what** the project does -- requirements, inputs, outputs, behavior -- without specifying **how** it is implemented. This is the source of truth for scope.

For implementation details, see `tech-spec.md`. For the implementation plan, see `stories.md`.

{% include "modes/_header-sequence.md" %}

## Steps

1. Gather information from the developer (ask questions if needed):
   - project_name: The project name
   - programming_language: e.g., Python 3.11+, Node 22, Go 1.23
   - project_goal: One paragraph on what the project does
   - core_requirements: The essential functionality
   - operational_requirements: Error handling, logging, configuration, CLI interface, etc.
   - quality_requirements: Reliability, clarity, minimal dependencies, cross-platform, etc.
   - usability_requirements: Who uses it and how (CLI, library, web, etc.)
   - non_goals: What the project explicitly does NOT do
   - inputs: Required and optional inputs with examples (CLI args, config files, env vars)
   - outputs: File structures, console output, data formats
   - functional_requirements: Numbered list of features with behavior descriptions and edge cases
   - configuration: Config precedence, config file format/schema
   - testing_requirements: Minimum test coverage expectations
   - security_notes: Security and compliance considerations (if applicable)
   - performance_notes: Concurrency, rate limiting, atomicity (if applicable)
   - acceptance_criteria: Definition of done for the whole project

2. Generate `docs/specs/features.md` using the artifact template at `templates/artifacts/features.md`

3. Present the complete document to the developer for approval. Iterate as needed.

## Formats

### functional_requirements

```markdown
### FR-1: Feature Name

Description of the feature's purpose.

**Behavior:**
1. Step 1
2. Step 2
3. Step 3

**Edge Cases:**
- Edge case 1 -> How it's handled
- Edge case 2 -> How it's handled
```
