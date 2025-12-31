---
description: Generate standup notes - what you did, what you're doing, blockers
allowed-tools: Glob, Read, Grep
argument-hint: [--for=<name>]
---

# Standup Notes

Generate standup notes based on your recent activity.

## Arguments

`$ARGUMENTS` - Optional:
- `--for=<name>` - Generate standup for a specific person (default: USER_NAME from .env)

## Examples

```bash
/standup                  # Your standup (from .env USER_NAME)
/standup --for=John       # Standup for John
```

## Task

### 1. Identify User

- Read `USER_NAME` from `.env` (or use `--for` argument)
- Also check `USER_ALIASES` for name matching

### 2. Find Yesterday's Completed Tasks

Search `knowledge/tasks/` for tasks where:
- Assignee matches user
- Status changed to "Done" yesterday or today
- Or `completed` date is yesterday

### 3. Find Today's Tasks

Search `knowledge/tasks/` for tasks where:
- Assignee matches user
- Status is "In Progress" or "Pending"
- Priority: show High first

### 4. Find Blockers

Search `knowledge/tasks/` for tasks where:
- Assignee matches user
- Status is "Blocked"
- Or task description mentions "blocked", "waiting"

### 5. Get Recent Context

Search recent `processed/` documents (last 2 days) for:
- Mentions of the user
- Context about their work

### 6. Generate Standup

```markdown
# Standup Notes

**Date:** January 15, 2024
**Name:** John Smith

---

## Yesterday (Completed)

- ✓ **Finished OAuth2 integration** - Merged PR #234, all tests passing
- ✓ **Reviewed Jane's API documentation** - Left comments, approved
- ✓ **Fixed login redirect bug** - Hotfix deployed to production

---

## Today (Planned)

### High Priority
- [ ] **Deploy OAuth2 to staging** - Target: EOD
- [ ] **Write migration script for user table**

### Normal Priority
- [ ] **Update Swagger docs** with new auth endpoints
- [ ] **Meet with Sarah** about infrastructure needs

---

## Blockers

- **Staging deployment blocked** - Waiting on DevOps to provision new cluster
  - Raised in #platform channel
  - ETA from DevOps: Tomorrow

---

## Notes

- Sprint ends Friday
- Need to sync with Jane on API versioning
- PTO next Monday

---

*Copy-paste ready for standup meeting*
```

### 7. Copy-Friendly Format

Also output a compact version:

```
Yesterday:
• Finished OAuth2 integration (PR #234 merged)
• Reviewed API docs
• Fixed login redirect bug

Today:
• Deploy OAuth2 to staging
• Write user table migration script
• Update Swagger docs

Blockers:
• Staging deployment - waiting on DevOps (ETA tomorrow)
```

## No Activity Found

If no tasks found for user:

```
No recent activity found for John Smith.

Possible reasons:
- Tasks not yet assigned in knowledge base
- Name mismatch (check USER_NAME in .env)
- No documents processed recently

Try:
- /my-tasks to see all your tasks
- /find John to check your profile
```

## Multiple Users

If user name is ambiguous:

```
Multiple matches for "John":

1. John Smith (john-smith.md)
2. John Davis (john-davis.md)

Specify: /standup --for="John Smith"
```
