# Agent Skills

A collection of reusable [Agent Skills](https://agentskills.io) for AI-powered development tools.

## What are Agent Skills?

Agent Skills are folders of instructions, scripts, and resources that give AI agents new capabilities and expertise. They help agents perform tasks more accurately and efficiently by providing domain-specific knowledge on demand.

These skills are compatible with tools like [Claude Code](https://claude.ai/code), [Cursor](https://cursor.com), [OpenCode](https://opencode.ai), [Gemini CLI](https://geminicli.com), and [many others](https://agentskills.io).

## Available Skills

| Skill | Description |
|-------|-------------|
| [admin-ui-svelte](./admin-ui-svelte) | Build modern admin dashboards with Tailwind CSS v4, Skeleton UI, and Svelte 5. Covers layouts, tables, forms, navigation, auth pages, and responsive design patterns. |
| [bootstrap-5](./bootstrap-5) | Build modern, responsive, accessible web interfaces using pure Bootstrap 5. Covers grid system, flexbox utilities, spacing, colors, typography, forms, buttons, cards, modals, navbars, and more. |
| [contextual-stewardship](./contextual-stewardship) | Extract, curate, and persist architectural decisions, business rules, and workflows into long-term memory using graceful degradation (MCP Context → local TOON file). |
| [long-running-work-planning](./long-running-work-planning) | Break down ambiguous problems, explore alternatives, and maintain work continuity across extended tasks with structured incremental reasoning. |
| [json-schema](./json-schema) | Author, review, debug, migrate, and explain JSON Schema with verifiable Draft 2020-12 correctness, complete keyword coverage, and executable validation checks. |
| [quality-grading](./quality-grading) | Grade code, specifications, or design documents across four quality dimensions with a 1-5 scoring scale and auto-improvement for artifacts below threshold. |

## Installation

Copy the skill folder to your project or skills directory:

```bash
# Clone or download this repository
git clone https://github.com/lindoelio/my-agent-skills.git

# Copy a skill to your project
cp -r my-agent-skills/admin-ui-svelte ./skills/
```

Alternatively, configure your agent tool to point to this repository as a skills source.

## Usage

Once installed, compatible AI agents will automatically discover these skills and use them when relevant to your task. Simply ask your agent to help with something covered by a skill, and it will load the appropriate context.

Example prompts:

```
"Create a responsive admin dashboard with sidebar navigation"
"Build a login form with validation using Bootstrap 5"
"Help me debug this intermittent API failure"
```

## Creating Your Own Skills

To create a new skill, create a folder with a `SKILL.md` file containing YAML frontmatter and instructions:

```markdown
---
name: my-skill
description: What it does and when to use it.
---

# Instructions

Your detailed instructions for the agent here.
```

See the [Agent Skills Specification](https://agentskills.io/specification) for the complete format and [AGENTS.md](./AGENTS.md) for contributor guidelines.

## Resources

- [Agent Skills Documentation](https://agentskills.io/home)
- [Specification](https://agentskills.io/specification)
- [Best Practices](https://agentskills.io/skill-creation/best-practices)
- [Example Skills](https://github.com/anthropics/skills)
- [Reference Library](https://github.com/agentskills/agentskills/tree/main/skills-ref)

## License

Each skill has its own license specified in the `SKILL.md` frontmatter. See individual skill folders for details.