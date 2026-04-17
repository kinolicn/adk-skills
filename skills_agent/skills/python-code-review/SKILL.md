---
name: python-code-review
description: This skill performs comprehensive Python code reviews. It checks for code quality, compliance with Python best practices, readability, error handling, security vulnerabilities, and performance issues. Activate this skill when tasked with auditing Python scripts or projects.
metadata:
  version: "1.0"
  author: "assistant"
---

To review a Python codebase, follow these steps:

Step 1: Collect the Python code that needs review. Ensure it's in readable format (e.g., `.py` files or pasted code).

Step 2: Check for the following aspects:
- **Code Quality & Readability**:
  - Ensure compliance with PEP 8 standards.
  - Look for meaningful naming conventions.
  - Comments and docstrings should adequately describe functionality.

- **Error Handling**:
  - Check if try-except blocks properly handle exceptions.
  - Look at the management of resources like file handlers and database connections.

- **Security**:
  - Hunt for hardcoded sensitive information.
  - Inspect user input handling and SQL query formatting.

- **Performance**:
  - Look for unnecessary nested loops and redundant operations.
  - Check for opportunities to use generators or efficient data structures.

Step 3: Use references to ensure a thorough audit:
- Refer to `readability-guidelines.md` for PEP 8 rules.
- Use `security-checklist.md` for spotting vulnerabilities.

Step 4: Compile the findings into a structured report:
- Summarize strengths and weaknesses.
- List specific issues with relevant code snippets.
- Suggest corrections or improvements.

Step 5: Validate your reviewed corrections using Python linters (e.g., `pylint`, `flake8`). Test runtime for optimized sections if performance improvements were suggested.