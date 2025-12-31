---
description: Look up a person - shows profile, assigned tasks, mentions, and relationships
allowed-tools: Grep, Glob, Read
argument-hint: <person-name>
---

# Find Person

Look up a person and show all their information across the knowledge base.

## Arguments

`$ARGUMENTS` - Person's name (full or partial)

## Examples

```bash
/find John Smith
/find john
/find @jsmith
```

## Task

### 1. Find Person Profile

Search for the person in `knowledge/people/`:
- Try exact match: `<firstname>-<lastname>.md`
- Try partial match: files containing the name
- Try alias match: check `name_variations` in frontmatter

### 2. Find Assigned Tasks

Search `knowledge/tasks/` for tasks where:
- Assignee matches the person's name
- Person is mentioned in task description

### 3. Find Mentions

Search across all knowledge base for mentions:
- `knowledge/project-status/` - Status updates mentioning them
- `knowledge/wiki/` - Wiki articles mentioning them
- `processed/` - Recent documents mentioning them

### 4. Find Relationships

From the person's profile and other people's profiles:
- Who they work with
- Who they report to
- Who reports to them

### 5. Format Output

```
# John Smith
===========

## Profile

| Field | Value |
|-------|-------|
| Role | Senior Engineer |
| Team | Platform Team |
| Expertise | Backend, Auth, APIs |

Source: [knowledge/people/john-smith.md]

---

## Assigned Tasks (3 active)

### High Priority
1. **Implement OAuth2** - Due: Jan 25
   Status: In Progress
   [knowledge/tasks/auth-tasks.md]

### Normal Priority
2. **Review API docs** - Due: Jan 20
   Status: Pending
   [knowledge/tasks/docs-tasks.md]

3. **Update deployment script** - No deadline
   Status: Pending
   [knowledge/tasks/infra-tasks.md]

### Completed Recently
- ✓ Set up CI pipeline (Jan 10)

---

## Recent Mentions (last 7 days)

| Date | Document | Context |
|------|----------|---------|
| Jan 15 | sprint-review.md | Led OAuth discussion |
| Jan 14 | standup.md | Reported auth progress |
| Jan 12 | slack-discussion.md | Answered API questions |

---

## Relationships

**Works with:**
- Jane Doe (PM, same project)
- Bob Wilson (QA, reviews his PRs)

**Reports to:**
- Sarah Kim (Engineering Manager)

---

## Quick Actions

- /search "John Smith" - Find all mentions
- /my-tasks (if this is you) - See your task list
```

## Not Found Handling

If person not found:

```
Person not found: "<name>"

**Searched:**
- knowledge/people/ - No matching profile
- Name variations checked

**Did you mean:**
- John Davis (john-davis.md)
- Johnny Smith (johnny-smith.md)

**Suggestions:**
- Check spelling
- Try first name only: /find John
- The person may not be in the knowledge base yet
```

## Partial Match Handling

If multiple matches:

```
Multiple matches for "John":

1. John Smith - Senior Engineer, Platform Team
   [knowledge/people/john-smith.md]

2. John Davis - Product Manager
   [knowledge/people/john-davis.md]

3. Johnny Wilson - QA Engineer
   [knowledge/people/johnny-wilson.md]

Specify full name: /find John Smith
```
