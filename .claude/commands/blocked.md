---
description: Show all blocked tasks and what's blocking them
allowed-tools: Glob, Read, Grep
argument-hint: [--assignee=<name>]
---

# Blocked Tasks

Show all tasks that are currently blocked.

## Arguments

`$ARGUMENTS` - Optional:
- `--assignee=<name>` - Filter by assignee

## Examples

```bash
/blocked                    # All blocked tasks
/blocked --assignee=John    # John's blocked tasks
```

## Task

### 1. Scan All Tasks

Search `knowledge/tasks/*.md`:
- Find tasks with Status: "Blocked"
- Also find tasks mentioning "blocked by", "waiting on", "depends on"

### 2. Extract Blocker Information

For each blocked task:
- What is blocking it
- Who/what is the blocker
- How long has it been blocked
- Priority of the blocked task

### 3. Group by Blocker Type

- **External:** Waiting on other teams, vendors
- **Internal:** Waiting on team members
- **Technical:** Dependencies, infrastructure
- **Decision:** Waiting for decision/approval

### 4. Display Results

```markdown
# Blocked Tasks

**Date:** January 15, 2024
**Total Blocked:** 4

---

## Impact Summary

| Priority | Count | Impact |
|----------|-------|--------|
| High | 2 | Blocking release |
| Medium | 1 | Sprint risk |
| Low | 1 | Minor delay |

---

## External Blockers (2)

### 🚫 Deploy to staging
- **Assignee:** John Smith
- **Priority:** High
- **Blocked by:** DevOps team - provisioning new cluster
- **Blocked since:** January 12, 2024 (3 days)
- **Impact:** Blocking QA testing
- **File:** knowledge/tasks/deploy-tasks.md

**Status:** Escalated to DevOps manager, ETA tomorrow

### 🚫 Integrate payment provider
- **Assignee:** Jane Doe
- **Priority:** High
- **Blocked by:** Vendor - waiting for API credentials
- **Blocked since:** January 10, 2024 (5 days)
- **Impact:** Payment feature delayed
- **File:** knowledge/tasks/payment-tasks.md

**Status:** Followed up with vendor, no response yet

---

## Internal Blockers (1)

### 🚫 Review security implementation
- **Assignee:** Bob Wilson
- **Priority:** Medium
- **Blocked by:** Waiting on John to complete OAuth
- **Blocked since:** January 14, 2024 (1 day)
- **Impact:** Security review delayed
- **File:** knowledge/tasks/security-tasks.md

**Status:** John's OAuth work is in progress, expect unblock by Jan 17

---

## Technical Blockers (1)

### 🚫 Run performance tests
- **Assignee:** Sarah Kim
- **Priority:** Low
- **Blocked by:** Test environment down
- **Blocked since:** January 13, 2024 (2 days)
- **Impact:** Cannot validate performance
- **File:** knowledge/tasks/testing-tasks.md

**Status:** IT investigating, ticket #12345

---

## Blocker Resolution Tracking

| Blocker | Owner | ETA | Actions Taken |
|---------|-------|-----|---------------|
| DevOps cluster | DevOps Team | Jan 16 | Escalated |
| Vendor credentials | Vendor | Unknown | Following up |
| OAuth completion | John | Jan 17 | In progress |
| Test environment | IT | Unknown | Ticket filed |

---

## Recommendations

1. **Escalate payment vendor** - 5 days with no response
2. **Check DevOps ETA** - Critical for release
3. **Parallelize where possible** - Some work can continue

---

## Quick Actions

- Unblock a task: Edit task file, change Status and add resolution note
- See all tasks: /my-tasks
- See overdue: /overdue
```

## No Blocked Tasks

```
No blocked tasks found! 🎉

All tasks are progressing normally.

To check task status:
  /my-tasks    # Your tasks
  /overdue     # Overdue tasks
  /status      # Pipeline overview
```

## Recently Unblocked

Also show recently unblocked tasks:

```markdown
## Recently Unblocked (last 7 days)

| Task | Unblocked | Was blocked by |
|------|-----------|----------------|
| API integration | Jan 13 | Waiting on specs |
| Database access | Jan 11 | Permissions issue |

These may need attention after being blocked.
```
