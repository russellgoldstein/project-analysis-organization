---
description: Show tasks assigned to you (from USER_NAME in .env)
allowed-tools: Glob, Read, Grep
argument-hint: [--all] [--status=<status>]
---

# My Tasks

Show all tasks assigned to you.

## Arguments

`$ARGUMENTS` - Optional:
- `--all` - Include completed tasks
- `--status=<status>` - Filter by status: pending, in-progress, blocked, done
- `--priority=<priority>` - Filter by priority: high, medium, low

## Examples

```bash
/my-tasks                      # Active tasks only
/my-tasks --all                # Include completed
/my-tasks --status=blocked     # Only blocked tasks
/my-tasks --priority=high      # Only high priority
```

## Task

### 1. Get User Name

Read from `.env`:
- `USER_NAME` - Primary name
- `USER_ALIASES` - Alternative names to match

### 2. Search Tasks

Scan all files in `knowledge/tasks/`:
- Parse each task entry
- Match assignee against user name or aliases
- Filter by status (exclude "Done" unless `--all`)

### 3. Categorize Tasks

Group tasks by:
- Priority (High → Medium → Low → Unspecified)
- Status (Blocked → In Progress → Pending)
- Deadline (Overdue → This week → Later → No deadline)

### 4. Display Results

```markdown
# My Tasks

**User:** John Smith
**Date:** January 15, 2024

---

## Summary

| Status | Count |
|--------|-------|
| In Progress | 3 |
| Pending | 5 |
| Blocked | 1 |
| **Total Active** | **9** |

---

## Overdue (1)

### ⚠️ Update API documentation
- **Due:** January 10, 2024 (5 days overdue)
- **Priority:** Medium
- **Source:** [sprint-planning.md]
- **File:** knowledge/tasks/docs-tasks.md

---

## High Priority (2)

### 🔴 Implement OAuth2 authentication
- **Due:** January 25, 2024
- **Status:** In Progress
- **Source:** [sprint-planning.md]
- **File:** knowledge/tasks/auth-tasks.md

### 🔴 Fix security vulnerability
- **Due:** January 18, 2024
- **Status:** Pending
- **Source:** [security-audit.md]
- **File:** knowledge/tasks/security-tasks.md

---

## In Progress (2)

### API endpoint refactoring
- **Due:** January 30, 2024
- **Priority:** Medium
- **File:** knowledge/tasks/api-tasks.md

### Database migration planning
- **Due:** February 1, 2024
- **Priority:** Medium
- **File:** knowledge/tasks/data-tasks.md

---

## Pending (4)

### Write unit tests for auth module
- **Due:** January 28, 2024
- **Priority:** Medium

### Review PR #456
- **Due:** None
- **Priority:** Low

...

---

## Blocked (1)

### 🚫 Deploy to staging
- **Blocked by:** Waiting on DevOps for new cluster
- **Since:** January 14, 2024
- **Priority:** High
- **File:** knowledge/tasks/deploy-tasks.md

---

## Quick Actions

- Mark task done: Edit the task file, change Status to "Done"
- Add new task: /task <description> @me
- See all tasks: /search assignee:John
```

## No Tasks Found

```
No tasks found assigned to John Smith.

Checked:
- USER_NAME: John Smith
- USER_ALIASES: john, jsmith

Possible reasons:
- No tasks assigned yet
- Name mismatch in task files
- Tasks not yet processed

Try:
- /search John - Find mentions
- /find John - Check your profile
```

## User Not Configured

```
USER_NAME not configured in .env

Please add to your project's .env file:
USER_NAME=Your Full Name
USER_ALIASES=nickname,shortname

Then run /my-tasks again.
```
