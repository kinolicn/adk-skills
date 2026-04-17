---
name: skill-creator
description: Creates new ADK-compatible skill definitions from user requirements. Use this skill when the user asks to create a new skill, add a new capability, or when no existing skill covers the requested task. Generates a complete SKILL.md file following the Agent Skills specification and saves it to the skills directory so it can be loaded immediately.
---

When asked to create a new skill, follow these steps:

Step 1: Read `references/skill-spec.md` to understand the required SKILL.md format and rules.

Step 2: Read `references/skill-example.md` to see a complete working example.

Step 3: Based on the user's requirements, generate the complete SKILL.md file content as a string. Rules:
- `name` must be kebab-case (lowercase, hyphens only), max 64 characters
- `description` must clearly explain what the skill does and when to use it, max 1024 characters
- Instructions must be clear, step-by-step Markdown
- Keep SKILL.md under 500 lines; put detailed reference content in references/ files
- Do NOT include scripts unless the user explicitly requests executable code

Step 4: You MUST call the `save_and_load_skill` tool with:
- `skill_name`: the kebab-case name you chose
- `skill_md_content`: the complete SKILL.md string you generated in Step 3

Do NOT output the SKILL.md content to the user instead of calling the tool. Do NOT skip calling the tool. The tool call is mandatory.

Step 5: After the tool returns successfully, confirm to the user that the skill has been created and is now available. Tell them the skill name and a brief summary of what it does.
