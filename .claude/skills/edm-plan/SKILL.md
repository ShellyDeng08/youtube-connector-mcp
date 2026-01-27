---
name: edm-plan
description: Plan a new EDM feature or requirement. Use this when user wants to create PRD, TRD, or Tech Spec.
---

# EDM Plan Skill

This skill guides the user through the process of analyzing requirements, designing solutions, and generating standard documentation (PRD/Tech Spec).

## Constraints

- **Interaction Mode**: Follow **Ask -> Discuss -> Confirm -> Generate** pattern.
- **Prohibited**:
  - DO NOT generate any file immediately upon receiving the request.
  - DO NOT generate any file until the user explicitly confirms (e.g., "Start generating", "Looks good").
  - If user input is partial/fuzzy, DO NOT guess; MUST ask follow-up questions.
- **Templates**: MUST use standard templates located in `packages/apps/edm-ai-docs/specs/templates/`.

## Execution Steps

1. **Identify Intent**:

   - Ask the user to clarify the type of planning if not specified:
     - **[1] Product Requirement (PRD)**: For new features/iterations.
     - **[2] Technical Requirement (TRD)**: For refactoring/tech projects.
     - **[3] Technical Solution (Tech Spec)**: For specific implementation design.
     - **[4] Exploration**: For brainstorming.

2. **Gather & Clarify**:

   - **PRD/TRD**: Ask for Goal, Scope, Metrics.
   - **Tech Spec**: Ask for PRD link, UI changes, Architecture changes.
   - **Exploration**: Ask for core problem/idea.
   - _Action_: Summarize understanding and ask "Is there anything missing?" before proceeding.

3. **Generate Document** (Only after confirmation):

   - Select the correct template:
     - PRD/TRD -> `packages/apps/edm-ai-docs/specs/templates/PRD_TEMPLATE.md`
     - Tech Spec -> `packages/apps/edm-ai-docs/specs/templates/TECH_SPEC_TEMPLATE.md`
   - Use `Write` tool to create the file in `packages/apps/edm-ai-docs/specs/`.
   - File naming convention: `<Name>_<Type>.md` (e.g., `MilestoneEmail_PRD.md`).

4. **Delivery**:
   - Inform the user that the document has been created.
   - Provide the "Feishu Doc Sync Tip" (as defined in `AGENT_PROMPT.md`).
