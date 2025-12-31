# Proposed Update Template

Use this template for change proposals in `proposed-updates/`.

## Proposed Update File

File location: `proposed-updates/update-<NNN>-<brief-description>.md`

```markdown
---
type: proposed-update
proposal_id: update-001
created: YYYY-MM-DD
target_file: knowledge/tasks/project-alpha-tasks.md
target_section: Task "Implement authentication"
change_type: update
source_document: processed/2024-01-15-zoom-sprint-review.md
confidence: high
status: pending_review
reviewed_date: null
reviewed_by: null
---

# Proposed Update: [Brief Descriptive Title]

## Summary

One-sentence summary of what this proposal changes.

## Target

**File:** `knowledge/tasks/project-alpha-tasks.md`
**Section:** Task "Implement authentication"
**Line(s):** Approximately lines 45-48

## Change Type

`update` - Modify existing content

**Change types:**
- `update` - Modify existing content
- `add` - Add new content to existing file
- `merge` - Combine this content with another entry
- `archive` - Mark content as outdated/remove

## Current Content

The current content in the target file:

```markdown
### Task: Implement authentication

| Field | Value |
|-------|-------|
| Status | In Progress |
| Assignee | John Smith |
| Deadline | 2024-01-20 |
```

## Proposed Content

What it should be changed to:

```markdown
### Task: Implement authentication

| Field | Value |
|-------|-------|
| Status | Done |
| Assignee | John Smith |
| Deadline | 2024-01-20 |
| Completed | 2024-01-15 |
```

## Diff View

```diff
- | Status | In Progress |
+ | Status | Done |
+ | Completed | 2024-01-15 |
```

## Rationale

Explain why this change should be made:

In the sprint review meeting on 2024-01-15, John Smith confirmed that the authentication implementation was completed and merged to production.

## Source Evidence

**Document:** `processed/2024-01-15-zoom-sprint-review.md`

**Relevant Quote:**
> "The authentication work is done. We merged it yesterday and it's been running in production without issues."
> — John Smith, Sprint Review, January 15, 2024

**Context:**
This was stated during the "Completed Work" section of the sprint review, approximately 15 minutes into the meeting.

## Confidence Assessment

**Confidence Level:** High

**Reasoning:**
- Direct statement from the task assignee
- Specific completion claim ("merged yesterday")
- Corroborated by production deployment mention

**Potential Issues:** None identified

## Impact Analysis

**Affected Files:**
- Primary: `knowledge/tasks/project-alpha-tasks.md`
- Related: None

**Side Effects:**
- Task count in "In Progress" decreases
- Task count in "Done" increases

---

## Review Section

### Review Actions

- [ ] **Approve and apply** - Apply this change as proposed
- [ ] **Modify and apply** - Make adjustments before applying
- [ ] **Reject** - Do not apply this change
- [ ] **Defer** - Review again later

### Reviewer Notes

_Add notes here during review:_

```
[Date] [Reviewer]: Notes about the review...
```

### Resolution

**Final Decision:** [Pending / Approved / Modified / Rejected / Deferred]
**Resolved Date:** YYYY-MM-DD
**Resolved By:** Reviewer Name
**Notes:** Any final notes about the resolution
```

## Quick Proposal (for simple updates)

```markdown
---
type: proposed-update
proposal_id: update-002
created: YYYY-MM-DD
target_file: knowledge/definitions/api.md
change_type: update
source_document: processed/2024-01-15-meeting.md
confidence: medium
status: pending_review
---

# Proposed Update: Clarify API Definition

## Summary

Add context about internal API usage.

## Target

**File:** `knowledge/definitions/api.md`

## Change

**Add to "Context in Project" section:**

```markdown
The Platform team maintains the core internal APIs, while product teams consume them.
```

## Source

> "Platform owns the APIs, product teams use them"
> — Jane Doe, Team Sync

## Confidence

Medium - Inferred from discussion context

---

- [ ] Approve
- [ ] Modify
- [ ] Reject
- [ ] Defer
```

## Merge Proposal

For combining entries:

```markdown
---
type: proposed-update
proposal_id: update-003
created: YYYY-MM-DD
target_file: knowledge/definitions/api-gateway.md
change_type: merge
source_document: knowledge/definitions/gateway-service.md
confidence: high
status: pending_review
---

# Proposed Update: Merge Duplicate Definitions

## Summary

Merge "Gateway Service" into "API Gateway" as they refer to the same thing.

## Files to Merge

- **Keep:** `knowledge/definitions/api-gateway.md`
- **Merge into it:** `knowledge/definitions/gateway-service.md`

## Proposed Merged Content

[Combined content from both files]

## After Merge

- Delete `gateway-service.md`
- Add "Gateway Service" as alias in `api-gateway.md`

---

- [ ] Approve
- [ ] Modify
- [ ] Reject
- [ ] Defer
```

## Confidence Guidelines

**High:**
- Explicit statement from authoritative source
- Clear date and attribution
- No ambiguity in interpretation

**Medium:**
- Inferred from context
- Partially corroborated
- Some interpretation required

**Low:**
- Uncertain interpretation
- Conflicting signals
- Limited context
