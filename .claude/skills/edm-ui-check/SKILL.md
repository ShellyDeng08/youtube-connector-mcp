---
name: edm-ui-check
description: Review EDM UI code against compatibility guidelines (Outlook, Gmail, etc.).
---

# EDM UI Check Skill

This skill performs a static analysis review of EDM email components to ensure compliance with strict email client compatibility rules.

## Constraints

- **Reference**: MUST strictly follow rules in `.claude/docs/guidelines/ui_implementation_guide.md`.
- **Scope**: Focus on CSS compatibility, HTML structure (Tables vs Divs), and Image handling.
- **Output**: Provide a structured Markdown report with "Pass/Fail/Warning" for each check.

## Execution Steps

1. **Identify Target**:
   - If user provided a file path, use it.
   - If not, ask user which component to review (e.g., "Which `view.tsx` should I check?").

2. **Analyze Code**:
   - Read the target file content.
   - Check against key EDM rules:
     - [ ] **Layout**: Is it using `<table>` for structure? (Divs are risky in Outlook).
     - [ ] **CSS**: Are styles inline? (No external stylesheets).
     - [ ] **Flexbox**: If used, is there a table-based fallback?
     - [ ] **Images**: Are `alt` tags present? Are dimensions specified?
     - [ ] **Dark Mode**: Are dark mode meta tags or overrides handled?

3. **Generate Report**:
   - Output a report in the following format:
     ```markdown
     ### UI Compliance Report: <Filename>
     
     **✅ Passed Checks**
     - [Rule Name]: Description...

     **❌ Violations (Must Fix)**
     - [Line X]: <Issue Description> (Ref: ui_implementation_guide.md#Section)
       - *Suggestion*: <Code Fix>

     **⚠️ Warnings (Potential Risks)**
     - [Line Y]: <Issue Description>
     ```

4. **Auto-Fix (Optional)**:
   - Ask user: "Do you want me to attempt to fix the Violations automatically?"
   - If yes, apply fixes using `SearchReplace` or `Write`.
