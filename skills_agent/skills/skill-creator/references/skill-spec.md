# Agent Skills Specification (agentskills.io)

## SKILL.md Structure

Every skill is a directory containing a `SKILL.md` file. The file has two parts:

### Part 1: YAML Frontmatter (Required)

```yaml
---
name: skill-name          # Required: kebab-case, max 64 chars, matches folder name
description: ...          # Required: max 1024 chars — what it does + when to use it
metadata:                 # Optional
  adk_additional_tools:   # List extra tool names the skill needs from the agent
    - tool_name
---
```

**Rules for `name`:**
- Lowercase letters and hyphens only
- No consecutive hyphens
- Must match the directory folder name exactly

**Rules for `description`:**
- Explain WHAT the skill does
- Explain WHEN the agent should activate it
- Under 1024 characters

### Part 2: Markdown Body (Instructions)

After the frontmatter, write step-by-step instructions in Markdown.

- Use numbered steps for sequential actions
- Reference files with relative paths: `references/filename.md`
- Keep total content under 500 lines (~5000 tokens)
- Put detailed domain knowledge in `references/` files, not in the body

## Directory Structure

```
skill-name/
├── SKILL.md              # Required: metadata + instructions
├── references/           # Optional: .md files with detailed knowledge
├── assets/               # Optional: templates, data files
└── scripts/              # Optional: .py scripts executable by the agent
```

## Progressive Disclosure Levels

- **L1** (~100 tokens): Only `name` + `description` from frontmatter — loaded at startup for all skills
- **L2** (<5000 tokens): Full SKILL.md body — loaded when agent activates the skill
- **L3** (on demand): Files in `references/`, `assets/`, `scripts/` — loaded only when instructions require them

## ADK-Specific Metadata

To make extra tools available when a skill is active, add to frontmatter:

```yaml
metadata:
  adk_additional_tools:
    - tool_function_name
```

The tool must already be registered in the agent's `SkillToolset.additional_tools`.
