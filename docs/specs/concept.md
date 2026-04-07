# concept.md — Project-Guide

Define the problem space (problem statement, pain points, target users, value criteria) and the solution space (solution statement, goals, scope, constraints), and pain point to solution mapping.

NOTE: This software project is in its third rewrite. Initially I started with an overly complex approach, then simplified to learn what worked well. Now I'm introducing some complexity to make it more maintainable and extensible.

## Problem Space
 
### Problem Statement
Developing software is complex and requires a lot of documentation and guidance. Doing this with an LLM requires a lot of prompting and context management, and it is too early in the AI revolution for proven practices to emerge. 

Without some framework, each project is a unique snowflake that is difficult to maintain and extend. The many learnings over time from project-to-project are difficult to apply systematically. 
There are also conflicting philophies:
|-|-|-|-|
| Philosophy | Description | Advantages | Disadvantages |
|-|-|-|-|
| **Vibe-coding** | Give the AI a high-level description and let it figure out the details. | Empowers non-technical people to contribute, proven to be a tool for fast iteration and experimentation, can help clarify requirements (what to build) | Can lead to unexpected results or unmaintainable code, often results in an 80%-90% solution that requires significant cleanup |
| **Agentic coding** | Give a herd of AI agents a problem and let them work away to build a solution. | Can build complex systems autonomously, can be better than an average programmer | Is very difficult for a developer to cognitively grasp and manage so much generated code, many complain that the code is just AI slop (strange problems that are harder to track down than writing it in other ways), code becomes a burden if the AI made decisions that are not aligned with product value |
| **HITLoop (Human-In-The-Loop)** | Collaborate closely with the AI to accelerate ideation, experimentation, and the text and code generation, but supervise all the activities closely to redirect when the AI is off course or when a better idea emerges. Ask questions when you don't understand what is going on. | Product decisions are often made on-the-fly and are difficult to preconceive before coding, developer gains familiarity with the codebase as it is generated, opportunities to redirect the AI or adjust requirements can be made early | Is slower than agentic AI or vibe-coding, requires more active involvement from the developer, can be tempting to do other things when the AI is generating code or documentation |

### Pain Points
1. **Repetitive**: AI-assisted coding has many repetitive actions and prompts. 
2. **Error-prone**: Copy-pasting prompts from a scratch-pad is error-prone and time-consuming. 
3. **AI decisions**: Turning over high-level decision-making to the LLM is risky and unreliable. 
4. **AI forgetting**: Managing the context window of the LLM is difficult and leads to cyclical forgetting.
5. **Best practices**: Much if not most software best practices are known generally but not codified in a practical way for AI-assisted development.
6. **Documentation**: Documentation of key decisions and trade-offs is easily lost in an LLM chat history.
7. **AI opacity**: Tracking LLM plans and progress is opaque and the styles and formats change across versions and models.
8. **Consistency**: Applying best practices and lessons learned consistently is practically impossible without a framework.

## Solution Space
`project-guide` is a Python project that provides a framework for AI-assisted software development. It applies the HITLoop philosophy and enables the developer to operate at a higher level of abstraction, focusing on strategic decisions while the framework handles the repetitive tasks of document generation and coding. **The LLM never commits code.** 

### Solution Overview
The system consists of a collection of markdown documents that are specialized around specified software development modes (planning, coding, debugging, etc.). Each mode has its own steps and criteria for "done". For convenience, there is a single entry point that the LLM can read to begin collaborating with the developer. `project-guide` can auto-detect a development mode based on the project context, or the developer can explicitly set the mode.

Simple workflow: 
1. Developer asks LLM to "Read the <entry-point-markdown-file>" (most efficient in a new chat window)
2. (optional) LLM asks clarifying questions to the developer
3. LLM follows the steps in the <entry-point-markdown-file>
4. LLM asks the developer to review and indicates what comes next, waiting for a "go" signal or suggests the next mode
5. Developer reviews and tests artifacts
6. (optional) Developer provides feedback or requests changes
7. (if cycle mode) Developer types "go" to move to next iteration

Changing Mode:
1. Developer runs CLI command to change mode
2. `project-guide` updates the LLM <entry-point-markdown-file> to reflect the new mode
3. Developer asks LLM to "Read the <entry-point-markdown-file>" for the new mode (most efficient in a new chat window)

LLM Bad Behavior:
1. Developer can log bad behavior to `project-guide`
2. Developer can customize a mode template based on logs
3. Developer can report persistent problems in a GitHub issue

### Pain-Point to Solution Mapping
1. **Repetitive**
  a. Provides a standardized set of markdown documents for each development mode
  b. Can auto-detect the current development mode based on the project context
  c. Naturally enables LLM to take over the detail-oriented work
2. **Error-prone**
  a. Provides a dynamically-generated,single entry point for the LLM to read
  b. Can auto-detect the current development mode based on the project context
  c. Gives developer a quick way to switch to a different development workflow (mode)
3. **AI decisions**
  a. Keeps developer close to the documentation and code as it emerges
  b. Relieves the developer of text and code tedium
  c. Developer can naturally focus on the big picture during generation and approval gates
  d. Allows the developer to spend the majority of time on higher-order thinking (ideation, design, review, strategy, abstraction)
4. **AI forgetting**
  a. Focused modes reduces token burden of entry point document
  b. Provides a quick way to refresh the LLM's memory as context window fills up then compacts (similar to new chat window)
  c. Enables tracking and reporting bad LLM behaviors
5. **Best practices**
  a. Includes focused best practices for each development mode
  b. Enables uniform distribution of best practices across all projects
  c. Allows easy per-project updates and additions via user-customized templates or global enhancements in future releases
6. **Documentation**
  a. Generates comprehensive documentation with minimal developer effort
  b. Having a standardized documentation approach makes it more likely to be completed onprojects with limited time investment
7. **AI opacity**
  a. Most of the planning is transparent and documented permanently in four stages (concept, features, tech-spec, stories)
  b. Shifting the coding implementation from an LLM-owned internal plan in the chat to a story document inverts control and increases LLM accountability
8. **Consistency**
  a. The templated approach ensures consistency across all projects
  b. Versioning helps developers check and manage when or if the updates are installed
  c. (future) Refactoring documentation and coding help migrate legacy projects to new standards