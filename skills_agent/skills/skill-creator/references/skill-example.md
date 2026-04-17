# Example Skill: code-reviewer

This is a complete, working example of a skill following the Agent Skills specification.

## Directory Structure

```
code-reviewer/
├── SKILL.md
└── references/
    └── checklist.md
```

## SKILL.md Content

```markdown
---
name: code-reviewer
description: Reviews Python code for quality, security, and best practices. Use this skill when the user asks to review, audit, or check their Python code. Covers readability, error handling, security vulnerabilities, and performance.
metadata:
  author: example
  version: "1.0"
---

When reviewing Python code, follow these steps:

Step 1: Read `references/checklist.md` for the full review checklist.

Step 2: Analyze the provided code against each checklist category:
- Readability and style (PEP 8)
- Error handling and edge cases
- Security vulnerabilities (injection, hardcoded secrets, etc.)
- Performance considerations

Step 3: Provide a structured report with:
- A summary score (Good / Needs Improvement / Critical Issues)
- Specific findings per category
- Concrete suggestions with corrected code snippets where applicable
```

## references/checklist.md Content

```markdown
# Python Code Review Checklist

## Readability
- [ ] Follows PEP 8 naming conventions
- [ ] Functions have docstrings
- [ ] No magic numbers — use named constants

## Error Handling
- [ ] Exceptions are caught specifically, not bare `except:`
- [ ] Resources (files, connections) are closed in `finally` or `with` blocks

## Security
- [ ] No hardcoded credentials or API keys
- [ ] SQL queries use parameterized statements
- [ ] User input is validated before use

## Performance
- [ ] No unnecessary loops inside loops
- [ ] Large data uses generators where possible
```

## Key Points from This Example

1. The `name` is kebab-case and matches the folder name
2. The `description` says both WHAT it does and WHEN to use it
3. Instructions reference `references/checklist.md` for L3 loading
4. Steps are numbered and actionable
5. Detailed content lives in `references/`, keeping SKILL.md concise
