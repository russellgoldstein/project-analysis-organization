# Project Status Template

Use this template for project status updates in `knowledge/project-status/`.

## Ongoing Status File

File location: `knowledge/project-status/<project>-status.md`

```markdown
---
type: status
project: project-name
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources:
  - processed/source1.md
  - processed/source2.md
---

# Project Name - Status

## Current State

**Status:** On Track / At Risk / Blocked / Completed
**Phase:** Planning / Development / Testing / Launch / Maintenance
**Last Updated:** YYYY-MM-DD

### Summary

Brief 2-3 sentence summary of the current state of the project.

### Health Indicators

| Indicator | Status | Notes |
|-----------|--------|-------|
| Timeline | Green | On schedule |
| Scope | Yellow | Minor scope creep |
| Resources | Green | Fully staffed |
| Quality | Green | Tests passing |

## Recent Progress

### Week of YYYY-MM-DD

**Completed:**
- Item 1 completed
- Item 2 completed

**In Progress:**
- Item 3 underway (75%)
- Item 4 started

**Source:** [sprint-review.md](../processed/2024-01-15-zoom-sprint-review.md)

---

### Week of YYYY-MM-DD

[Previous week's updates...]

---

## Decisions Log

Significant decisions made for this project:

### Decision: [Brief Title]

**Date:** YYYY-MM-DD
**Decision:** What was decided
**Rationale:** Why this decision was made
**Impact:** What this means for the project
**Source:** [meeting.md](../processed/source.md)

---

### Decision: [Brief Title]

[Previous decisions...]

---

## Blockers & Risks

### Active Blockers

| Blocker | Owner | Impact | Status |
|---------|-------|--------|--------|
| [Description] | Name | High | Working on it |

### Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| [Description] | Medium | High | Mitigation plan |

## Key Milestones

| Milestone | Target Date | Status | Notes |
|-----------|-------------|--------|-------|
| Phase 1 Complete | YYYY-MM-DD | Done | Completed on time |
| Phase 2 Complete | YYYY-MM-DD | In Progress | On track |
| Launch | YYYY-MM-DD | Planned | |

## Team

| Role | Person | Notes |
|------|--------|-------|
| Tech Lead | [[john-smith]] | |
| PM | [[jane-doe]] | |
| Engineer | [[alex-chen]] | |

## Related

- [[project-tasks]] - Active task list
- [[architecture-wiki]] - Technical documentation

## Updates History

Chronological log of status updates:

- YYYY-MM-DD: Status created
- YYYY-MM-DD: Updated with sprint review notes
- YYYY-MM-DD: Added new decision
```

## Point-in-Time Status

File location: `knowledge/project-status/<project>-YYYY-MM-DD.md`

For specific status snapshots (e.g., weekly reports):

```markdown
---
type: status
project: project-name
period: Week of YYYY-MM-DD
created: YYYY-MM-DD
sources:
  - processed/source.md
---

# Project Name - Status Update

**Period:** Week of YYYY-MM-DD
**Author:** From [source document]

## Summary

Brief summary of this period's progress.

## Completed This Period

- Completed item 1
- Completed item 2
- Completed item 3

## In Progress

- In progress item 1 (estimated completion: date)
- In progress item 2 (75% done)

## Planned for Next Period

- Planned item 1
- Planned item 2

## Blockers

- Blocker description and mitigation

## Decisions Made

- Decision 1: Brief description

## Metrics

| Metric | Value | Change |
|--------|-------|--------|
| Tasks Completed | 5 | +2 |
| Story Points | 21 | - |
| Open Bugs | 3 | -1 |

## Notes

Additional context or observations.
```

## Decision Record

For significant decisions that warrant their own file:

File location: `knowledge/project-status/<project>-decisions.md`

```markdown
---
type: decision-log
project: project-name
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

# Project Name - Decision Log

## ADR-001: [Decision Title]

**Date:** YYYY-MM-DD
**Status:** Accepted / Superseded / Deprecated
**Deciders:** Name1, Name2

### Context

What is the issue that we're seeing that is motivating this decision?

### Decision

What is the change that we're proposing and/or doing?

### Consequences

What becomes easier or more difficult to do because of this change?

### Source

[Document where this was decided](../processed/source.md)

---

## ADR-002: [Decision Title]

[Next decision...]
```
