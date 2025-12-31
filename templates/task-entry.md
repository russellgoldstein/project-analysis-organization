# Task Entry Template

Use this template when creating or updating task entries in `knowledge/tasks/`.

## Single Task Entry

```markdown
### Task: [Brief descriptive title]

| Field | Value |
|-------|-------|
| **ID** | task-NNNN (auto-generated) |
| **Assignee** | Name or "Unassigned" |
| **Deadline** | YYYY-MM-DD or "Not specified" |
| **Priority** | High / Medium / Low / Not specified |
| **Status** | Pending / In Progress / Blocked / Done |
| **Created** | YYYY-MM-DD |
| **Updated** | YYYY-MM-DD |
| **Source** | [document name](../processed/source.md) |

**Description:**
Clear description of what needs to be done. Be specific enough that anyone can understand the task.

**Acceptance Criteria:**
- [ ] Criterion 1
- [ ] Criterion 2

**Dependencies:**
- Depends on: [other task or "None"]
- Blocks: [what this blocks or "Nothing"]

**Notes:**
Additional context, updates, or discussion points.

**History:**
- YYYY-MM-DD: Created from [source document]
- YYYY-MM-DD: Status changed to In Progress
```

## Task Collection File

File location: `knowledge/tasks/<project>-tasks.md`

```markdown
---
type: task-collection
project: project-name
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources:
  - processed/source1.md
  - processed/source2.md
---

# Project Name - Tasks

## Summary

| Status | Count |
|--------|-------|
| Pending | X |
| In Progress | X |
| Blocked | X |
| Done | X |

## High Priority

### Task: [Title]
[task entry]

---

## Active Tasks

### Task: [Title]
[task entry]

---

### Task: [Title]
[task entry]

---

## Blocked

### Task: [Title]
[task entry with blocker details]

---

## Completed

### Task: [Title]
[task entry with completion date]

---

## Archived

Tasks that are no longer relevant:

### Task: [Title]
- **Archived:** YYYY-MM-DD
- **Reason:** Superseded by other work
```

## Field Guidelines

### Status Values

- **Pending**: Not yet started
- **In Progress**: Actively being worked on
- **Blocked**: Cannot proceed due to dependency
- **Done**: Completed
- **Archived**: No longer relevant

### Priority Values

- **High**: Urgent, affects deadlines, blocks others
- **Medium**: Normal priority, part of current sprint
- **Low**: Nice to have, can be deferred
- **Not specified**: Priority not determined

### Assignee

- Use full name when known
- Use "Unassigned" when no owner
- Use "Team" for collective tasks
- Note if assignment is tentative: "John Smith (tentative)"
