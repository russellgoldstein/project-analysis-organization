# Meeting Notes Template

Use this template when creating meeting notes in `knowledge/meetings/`.

## Meeting Notes File

File location: `knowledge/meetings/YYYY-MM-DD-<meeting-topic>.md` (lowercase, hyphenated)

```markdown
---
type: meeting-notes
meeting_date: YYYY-MM-DD
meeting_type: sprint-planning | architecture-review | standup | 1on1 | kickoff | retrospective | other
meeting_topic: Topic Name
source_document: processed/YYYY-MM-DD-<source>-<description>.md
participants:
  - Name 1
  - Name 2
  - Name 3
extracted_date: YYYY-MM-DD
tags:
  - tag1
  - tag2
---

# Meeting: <Topic>

**Date:** YYYY-MM-DD
**Type:** <Sprint Planning | Architecture Review | Standup | 1:1 | Kickoff | Retrospective>
**Participants:** Name 1, Name 2, Name 3
**Source:** [Original Document](../processed/<filename>.md)

## Executive Summary & Talking Points

### Executive Summary

A 2-3 sentence executive summary suitable for sharing with stakeholders who did not attend the meeting. Focus on outcomes and decisions, not process.

### Key Talking Points

- **Point 1**: Brief description of key topic or outcome
- **Point 2**: Brief description of key topic or outcome
- **Point 3**: Brief description of key topic or outcome

## Action Items & Next Steps

### Action Items

| Action | Assignee | Deadline | Priority | Status |
|--------|----------|----------|----------|--------|
| Description of specific task | Name | YYYY-MM-DD | High | Pending |
| Description of specific task | Name | YYYY-MM-DD | Medium | Pending |
| Description of specific task | Unassigned | TBD | Low | Pending |

### Next Steps

General follow-up items not assigned to specific individuals:

- Follow-up item 1
- Follow-up item 2
- Follow-up item 3

## Key Decisions & Architectural Principles

### Decisions Made

| Decision | Decided By | Date | Rationale |
|----------|------------|------|-----------|
| Description of what was decided | Name/Team | YYYY-MM-DD | Why this was decided |

(If no decisions were made: "No explicit decisions recorded in this meeting.")

### Architectural Principles

Technical or process principles established or reinforced:

- **Principle Name**: Description of the pattern, standard, or approach adopted

(If none: "No new architectural principles established.")

## Risks, Blockers, & Open Questions

### Risks

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Risk description | High/Med/Low | High/Med/Low | Mitigation plan if discussed |

(If none: "No risks identified.")

### Blockers

| Blocker | Owner | Blocked Tasks | Resolution Path |
|---------|-------|---------------|-----------------|
| Blocker description | Name | What's blocked | How to resolve |

(If none: "No blockers reported.")

### Open Questions

| Question | Needs Answer From | Urgency | Status |
|----------|-------------------|---------|--------|
| Question text | Name/Team | High/Med/Low | Open |

(If none: "No open questions remaining.")

---

**Source:** [Original Document](../processed/<filename>.md)
**Extracted:** YYYY-MM-DD
```

## Minimal Meeting Notes

For simple meetings or standups with limited content:

```markdown
---
type: meeting-notes
meeting_date: YYYY-MM-DD
meeting_type: standup
meeting_topic: Daily Standup
source_document: processed/YYYY-MM-DD-zoom-standup.md
participants:
  - Name 1
  - Name 2
extracted_date: YYYY-MM-DD
---

# Meeting: Daily Standup

**Date:** YYYY-MM-DD
**Participants:** Name 1, Name 2

## Executive Summary & Talking Points

### Executive Summary

Brief standup covering progress and blockers.

### Key Talking Points

- Point 1
- Point 2

## Action Items & Next Steps

### Action Items

| Action | Assignee | Deadline | Priority | Status |
|--------|----------|----------|----------|--------|
| Task 1 | Name | TBD | Medium | Pending |

### Next Steps

- Next step 1

## Key Decisions & Architectural Principles

No decisions made.

## Risks, Blockers, & Open Questions

### Blockers

| Blocker | Owner | Resolution Path |
|---------|-------|-----------------|
| Blocker 1 | Name | Resolution |

(If none: "No blockers reported.")
```

## Guidelines

### Creating Meeting Notes

- Create one file per meeting
- Use the meeting date as the filename prefix
- Include all participants who spoke or were mentioned
- Extract verbatim quotes for important decisions
- Link back to the source document

### Meeting Type Selection

| Type | Use For |
|------|---------|
| `sprint-planning` | Sprint or iteration planning meetings |
| `architecture-review` | Technical design discussions |
| `standup` | Daily status meetings |
| `1on1` | One-on-one meetings |
| `kickoff` | Project or initiative kickoffs |
| `retrospective` | Sprint retrospectives |
| `other` | Any other meeting type |

### Action Item Standards

- **Assignee**: Use actual name or "Unassigned"
- **Deadline**: Use YYYY-MM-DD format or "TBD"
- **Priority**: High = blocking, Medium = this sprint, Low = backlog
- **Status**: Pending, In Progress, Done, Blocked

### Linking

- Always link to source document
- Use `[[name]]` syntax for person references
- Link to related wiki articles when relevant
