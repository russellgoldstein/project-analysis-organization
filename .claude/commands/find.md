---
description: Look up a person - profile, tasks, recent discussions, decisions, blockers, relationships
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

### 3. Find Recent Activity

Search across all sources for the person's activity:

**Discussions & Conversations:**
- `processed/` - Recent documents where they spoke/participated
- Extract quotes and context from Zoom/Slack/meeting transcripts

**Decisions Involved:**
- `knowledge/project-status/` - Decisions they made or participated in
- `extractions/*-summary.md` - Key points attributed to them

**Issues & Blockers:**
- Tasks where they're blocked or blocking
- Problems they raised or are working on

### 4. Find Mentions

Search across all knowledge base for mentions:
- `knowledge/project-status/` - Status updates mentioning them
- `knowledge/wiki/` - Wiki articles mentioning them
- `processed/` - Recent documents mentioning them

### 6. Find Relationships

From the person's profile and other people's profiles:
- Who they work with
- Who they report to
- Who reports to them

### 7. Format Output

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

## Recent Discussions (last 14 days)

### From Sprint Planning (Jan 15)
> "I think we should use OAuth2 instead of building our own auth.
> It's more secure and we can integrate with Google and GitHub."

### From Slack #data-pipeline (Jan 14)
> "The ETL job is fixed. It was a schema change on the source API."

### From Standup (Jan 12)
> "Finished the CI pipeline setup. Moving on to auth work."

---

## Decisions Involved

| Date | Decision | Role |
|------|----------|------|
| Jan 15 | Use OAuth2 for authentication | Proposed |
| Jan 10 | Adopt GitHub Actions for CI | Implemented |
| Jan 5 | Defer mobile auth to next sprint | Participated |

---

## Current Blockers

- Waiting on API credentials from external team (Jan 14)
- Needs design review for OAuth flow (Jan 13)

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
