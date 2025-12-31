---
description: Quick-add a task - creates file in raw/ for pipeline processing
allowed-tools: Write, Bash
argument-hint: <task description> [@assignee] [#priority] [due:YYYY-MM-DD]
---

# Quick Capture Task

Quickly add a task that will be processed through the pipeline.

## Arguments

`$ARGUMENTS` - Task description with optional metadata:
- `@name` - Assign to someone
- `#high` / `#medium` / `#low` - Priority
- `due:YYYY-MM-DD` - Deadline

## Examples

```bash
/task Update the API documentation
/task Review PR #123 @john #high
/task Deploy to staging @jane due:2024-01-20
/task Fix login bug #high due:2024-01-16
```

## Task

### 1. Parse Arguments

Extract from `$ARGUMENTS`:
- **Description**: Everything except metadata tokens
- **Assignee**: Text after `@` (until space)
- **Priority**: `#high`, `#medium`, or `#low`
- **Deadline**: Date after `due:`

### 2. Generate Filename

Format: `raw/YYYY-MM-DD-task-<slug>.md`

Create slug from task description (first 5-6 words).

### 3. Create File

Write to `raw/`:

```markdown
---
source: manual-task
created: YYYY-MM-DD HH:MM
type: task
assignee: <extracted or empty>
priority: <extracted or empty>
deadline: <extracted or empty>
---

# Task: <brief title from description>

<full task description>

**Assignee:** <name or Unassigned>
**Priority:** <priority or Not specified>
**Deadline:** <date or Not specified>
```

### 4. Confirm Creation

```
Task captured!

File: raw/2024-01-15-task-review-pr-123.md

Details:
- Description: Review PR #123
- Assignee: John
- Priority: High
- Deadline: Not specified

To process into knowledge base:
  /intake    - Process this task
  /run       - Run full pipeline
```

## Examples with Output

### Basic Task
```bash
/task Update the API documentation
```
Creates:
```markdown
---
source: manual-task
created: 2024-01-15 14:30
type: task
---

# Task: Update the API documentation

Update the API documentation

**Assignee:** Unassigned
**Priority:** Not specified
**Deadline:** Not specified
```

### Full Metadata
```bash
/task Deploy new auth system to production @john #high due:2024-01-20
```
Creates:
```markdown
---
source: manual-task
created: 2024-01-15 14:30
type: task
assignee: john
priority: high
deadline: 2024-01-20
---

# Task: Deploy new auth system to production

Deploy new auth system to production

**Assignee:** John
**Priority:** High
**Deadline:** 2024-01-20
```

## Error Handling

- If no description: "Please provide task description: /task <description>"
- If invalid date format: Warn but still create task
- If raw/ doesn't exist: Create it
