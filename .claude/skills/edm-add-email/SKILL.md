---
name: edm-add-email
description: Add a new EDM email type. This involves analyzing requirements, creating data contracts, implementing UI components, and registering RPC logic.
---

# EDM Add Email Type Skill

This skill executes the standard workflow for adding a new email type, following a strict **Ask -> Plan -> Execute** process.

## Constraints

- **Phase Control**: Strict adherence to Phase 0 (Intent) -> Phase 1 (Plan) -> Phase 2 (Code) -> Phase 3 (Verify).
- **Stop Points**: MUST STOP and ask for user confirmation at defined checkpoints.
- **No Side Effects**: DO NOT modify code until Phase 2.
- **Single Step**: Only output content for the current step.
- **UI Compliance**: MUST follow guidelines in `.claude/docs/guidelines/ui_implementation_guide.md` (e.g., table layouts, inline CSS).

## Execution Steps

### Phase 0: Intent Confirmation

1. **Check Input**: Verify if the user provided 5 key items:
   - Type Name (PascalCase)
   - Entry Choice (ResponsiveGizmo)
   - Design Reference
   - Data Fields (IEmailData)
   - PRD Link
2. **If Incomplete**: STOP and ask for missing items.
3. **If Complete**: Proceed to Phase 1.1.

### Phase 1: Planning

1. **Phase 1.1: Business & Data Analysis**:
   - Analyze PRD vs Data Fields.
   - Output: Requirement Summary & Data Contract Validation.
   - **STOP** for confirmation.
2. **Phase 1.2: Selection Strategy**:
   - Analyze Design vs Existing Materials.
   - Decide: [Reuse] vs [New].
   - Output: Visual Structure, Selection Matrix, Design Specs (for New).
   - **STOP** for confirmation.
3. **Phase 1.3: Detailed Plan**:
   - Create Tech Spec using `specs/templates/TECH_SPEC_TEMPLATE.md`.
   - Initialize `TodoWrite` list.
   - **STOP** for confirmation.

### Phase 2: Execution

_Only enter after explicit confirmation._

1. **Step 1: Core Contract**:
   - Modify `emailData.ts` (Data Interface).
   - Modify `core.ts` (Tracking/Enum).
   - **STOP** for confirmation.
2. **Step 2: Component Implementation**:
   - Create `view.tsx` (UI with inline styles).
   - Create `index.ts` (Logic wrapper).
   - **STOP** for confirmation.
3. **Step 3: Debug & Mock**:
   - Run `.claude/scripts/debug_material.py` to generate mocks and start preview.
   - Output preview URL.
   - **STOP** for confirmation.
4. **Step 4: RPC Registration**:
   - Create `edm_templates_rpc/client/pages/<TypeName>/` structure.
   - Implement `config.ts`, `validator`, `dataProcessor`, `layout`.
   - **STOP** for confirmation.
5. **Step 5: Template Generation**:
   - Run `.claude/scripts/interactive_template.py` to generate final template.
   - Output final preview URL.
   - **STOP** for confirmation.

### Phase 3: Verification

1. **Guide User**: Tell user to run `npm run dev:material`.
2. **Cleanup**: Remove checklist from Tech Spec doc.
