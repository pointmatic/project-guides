# Project-Guide — Calm the chaos of LLM-assisted coding

This document provides step-by-step instructions for an LLM to assist a human developer in a project. 

## How to Use Project-Guide

### For Developers
After installing project-guide (`pip install project-guide`) and running `project-guide init`, instruct your LLM as follows in the chat interface: 

```
Read `docs/project-guide/go-project-guide.md`
```

After reading, the LLM will respond:
1. (optional) "I need more information..." followed by a list of questions or details needed. 
  - LLM will continue asking until all needed information is clear.
2. "The next step is ___."
3. "Say 'go' when you're ready." 

For efficiency, when you change modes, start a new LLM conversation. 

### For LLMs

**Modes**
This Project-Guide offers a human-in-the-loop workflow for you to follow that can be dynamically reconfigured based on the project `mode`. Each `mode` defines a focused sequence of steps to guide you (the LLM) to help generate artifacts for some facet in the project lifecycle. This document is customized for default.

**Approval Gate**
When you have completed the steps, pause for the developer to review, correct, redirect, or ask questions about your work.  

**Rules**
- Work through each step methodically, presenting your work for approval before continuing a cycle. 
- When the developer says "go" (or equivalent like "continue", "next", "proceed"), continue with the next action. 
- If the next action is unclear, tell the developer you don't have a clear direction on what to do next, then suggest something. 
- Never auto-advance past an approval gate—always wait for explicit confirmation. 
- After compacting memory, re-read this guide to refresh your context.

---


# Default Mode -- Getting Started

This is the default mode for new projects. It provides an overview of the full project lifecycle. For focused work, switch to a specific mode with `project-guide mode <name>`.

---

## Project Lifecycle

| Step | Mode | What it does |
|------|------|-------------|
| 1 | `plan_concept` | Define the problem and solution space |
| 2 | `plan_features` | Define requirements, inputs, outputs, behavior |
| 3 | `plan_tech_spec` | Define architecture, modules, dependencies |
| 4 | `plan_stories` | Break into phases and stories with checklists |
| 5 | `project_setup` | Scaffold LICENSE, headers, manifest, README, CHANGELOG, .gitignore |
| 6 | `code_velocity` | Implement stories with fast iteration |

## Get Started

To begin a new project, run:

```bash
project-guide mode plan_concept
```

## All Available Modes

### Planning (sequence)
| Mode | Command | Output |
|------|---------|--------|
| **Concept** | `project-guide mode plan_concept` | `docs/specs/concept.md` |
| **Features** | `project-guide mode plan_features` | `docs/specs/features.md` |
| **Tech Spec** | `project-guide mode plan_tech_spec` | `docs/specs/tech-spec.md` |
| **Stories** | `project-guide mode plan_stories` | `docs/specs/stories.md` |
| **Phase** | `project-guide mode plan_phase` | Add a new phase to an existing project |

### Setup (sequence)
| Mode | Command | Purpose |
|------|---------|---------|
| **Project Setup** | `project-guide mode project_setup` | One-time project scaffolding |

### Coding (cycle)
| Mode | Command | Workflow |
|------|---------|----------|
| **Velocity** | `project-guide mode code_velocity` | Direct commits, fast iteration |
| **Test-First** | `project-guide mode code_test_first` | TDD red-green-refactor cycle |
| **Debug** | `project-guide mode debug` | Test-driven debugging |

### Documentation (sequence)
| Mode | Command | Output |
|------|---------|--------|
| **Branding** | `project-guide mode document_brand` | `docs/specs/brand-descriptions.md` |
| **Landing Page** | `project-guide mode document_landing` | GitHub Pages + MkDocs docs |

