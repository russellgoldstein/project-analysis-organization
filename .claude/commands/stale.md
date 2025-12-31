---
description: Find knowledge base entries that may be outdated
allowed-tools: Glob, Read, Bash
argument-hint: [days] [--type=<type>]
---

# Find Stale Entries

Find knowledge base entries that haven't been updated recently and may be outdated.

## Arguments

`$ARGUMENTS` - Optional:
- `<days>` - Entries not updated in N days (default: 30)
- `--type=<type>` - Filter by type: tasks, people, definitions, wiki, status

## Examples

```bash
/stale                    # Not updated in 30 days
/stale 14                 # Not updated in 14 days
/stale --type=tasks       # Only stale tasks
/stale 60 --type=people   # People not mentioned in 60 days
```

## Task

### 1. Scan Knowledge Base

For each file in `knowledge/`:
- Read frontmatter
- Extract `updated` or `created` date
- Compare to current date

### 2. Identify Stale Entries

An entry is stale if:
- Not updated in N days (from frontmatter)
- Not referenced in recent processed docs
- Status is still "In Progress" but no recent activity

### 3. Categorize by Risk

- **High Risk:** Important entries that are stale (tasks, active projects)
- **Medium Risk:** Reference material that may be outdated
- **Low Risk:** Stable content that changes rarely

### 4. Display Results

```markdown
# Stale Entries Report

**Date:** January 15, 2024
**Threshold:** 30 days
**Total Stale:** 12

---

## Summary

| Category | Stale | Total | % Stale |
|----------|-------|-------|---------|
| Tasks | 3 | 25 | 12% |
| People | 2 | 10 | 20% |
| Definitions | 1 | 15 | 7% |
| Wiki | 4 | 12 | 33% |
| Status | 2 | 8 | 25% |

---

## High Risk (Action Recommended)

### 🔴 knowledge/tasks/q4-tasks.md
- **Last Updated:** December 1, 2023 (45 days ago)
- **Issue:** Contains tasks marked "In Progress" from last quarter
- **Recommendation:** Review and update task statuses

### 🔴 knowledge/project-status/launch-status.md
- **Last Updated:** December 15, 2023 (31 days ago)
- **Issue:** Project status may be outdated
- **Recommendation:** Update with current status

### 🔴 knowledge/people/alex-chen.md
- **Last Updated:** November 20, 2023 (56 days ago)
- **Issue:** No recent mentions - person may have left or changed roles
- **Recommendation:** Verify current status

---

## Medium Risk (Review Suggested)

### 🟡 knowledge/wiki/deployment-guide.md
- **Last Updated:** December 5, 2023 (41 days ago)
- **Issue:** Deployment process may have changed
- **Recommendation:** Verify accuracy

### 🟡 knowledge/definitions/api-v1.md
- **Last Updated:** November 1, 2023 (75 days ago)
- **Issue:** May reference deprecated API version
- **Recommendation:** Check if still relevant

---

## Low Risk (For Awareness)

### 🟢 knowledge/wiki/architecture-overview.md
- **Last Updated:** October 15, 2023 (92 days ago)
- **Note:** Architecture docs change slowly, but verify periodically

### 🟢 knowledge/definitions/etl.md
- **Last Updated:** September 1, 2023 (136 days ago)
- **Note:** Standard definition, unlikely to change

---

## Recommendations

1. **Review high-risk items first** - These may contain incorrect information
2. **Update or archive Q4 tasks** - Close out old quarter properly
3. **Verify people status** - Check if Alex is still on the team
4. **Schedule regular reviews** - Run /stale monthly

---

## Quick Actions

- Mark as current: Edit file, update `updated` date
- Archive: Move to `knowledge/archive/`
- Delete: Remove if no longer relevant
- Review all: /validate for full KB health check
```

## No Stale Entries

```
No stale entries found! 🎉

All knowledge base entries have been updated within the last 30 days.

The knowledge base is well-maintained.
```

## Stale by Type

With `--type` flag, show only that category with more detail:

```bash
/stale --type=tasks
```

Shows detailed task analysis including completion rates, assignee activity, etc.
