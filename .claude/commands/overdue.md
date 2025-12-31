---
description: List all tasks that are past their deadline
allowed-tools: Glob, Read, Grep
argument-hint: [--days=<N>] [--assignee=<name>]
---

# Overdue Tasks

List all tasks that are past their deadline.

## Arguments

`$ARGUMENTS` - Optional:
- `--days=<N>` - Include tasks due within N days (default: 0, only past due)
- `--assignee=<name>` - Filter by assignee

## Examples

```bash
/overdue                    # All overdue tasks
/overdue --days=7           # Overdue + due within 7 days
/overdue --assignee=John    # John's overdue tasks
```

## Task

### 1. Get Current Date

Use today's date as reference.

### 2. Scan All Tasks

Search `knowledge/tasks/*.md`:
- Parse each task entry
- Extract deadline field
- Compare to current date

### 3. Categorize by Severity

- **Critical:** More than 7 days overdue
- **Overdue:** 1-7 days overdue
- **Due Today:** Due today
- **At Risk:** Due within N days (if --days specified)

### 4. Display Results

```markdown
# Overdue Tasks

**Date:** January 15, 2024
**Total Overdue:** 5

---

## Critical (7+ days overdue)

### ⛔ Update security patches
- **Assignee:** Bob Wilson
- **Due:** January 5, 2024 (10 days overdue)
- **Priority:** High
- **Source:** security-audit.md
- **File:** knowledge/tasks/security-tasks.md

**Action needed:** This is significantly overdue. Escalate or reassign.

---

## Overdue (1-7 days)

### ⚠️ Update API documentation
- **Assignee:** John Smith
- **Due:** January 10, 2024 (5 days overdue)
- **Priority:** Medium
- **File:** knowledge/tasks/docs-tasks.md

### ⚠️ Review Q4 metrics
- **Assignee:** Jane Doe
- **Due:** January 12, 2024 (3 days overdue)
- **Priority:** Low
- **File:** knowledge/tasks/reporting-tasks.md

---

## Due Today

### 📅 Submit expense reports
- **Assignee:** Sarah Kim
- **Due:** January 15, 2024
- **Priority:** Low
- **File:** knowledge/tasks/admin-tasks.md

---

## Summary by Assignee

| Assignee | Critical | Overdue | Due Today |
|----------|----------|---------|-----------|
| Bob Wilson | 1 | 0 | 0 |
| John Smith | 0 | 1 | 0 |
| Jane Doe | 0 | 1 | 0 |
| Sarah Kim | 0 | 0 | 1 |

---

## Recommendations

1. **Escalate critical items** - Tasks 7+ days overdue need attention
2. **Review blocked tasks** - Some overdue items may be blocked
3. **Update deadlines** - If tasks are deprioritized, update the deadline

---

## Quick Actions

- See your overdue: /overdue --assignee=<your-name>
- See all tasks: /my-tasks
- Search tasks: /search deadline
```

## No Overdue Tasks

```
No overdue tasks found! 🎉

All tasks are on track.

To see upcoming deadlines:
  /overdue --days=7    # Tasks due within a week
```

## With --days Flag

```bash
/overdue --days=7
```

Adds section:

```markdown
## Due Within 7 Days

### 📆 Complete OAuth implementation
- **Assignee:** John Smith
- **Due:** January 20, 2024 (5 days)
- **Priority:** High

### 📆 Write integration tests
- **Assignee:** Jane Doe
- **Due:** January 22, 2024 (7 days)
- **Priority:** Medium
```
