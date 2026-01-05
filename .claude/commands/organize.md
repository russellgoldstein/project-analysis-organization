---
description: Organize extracted information into knowledge base directories
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
argument-hint: [tasks|definitions|people|wiki|status|jira|meetings|all]
---

# Knowledge Organization Pipeline (Stage 3)

Organize extractions from processed documents into the knowledge base.

## Arguments

`$ARGUMENTS` - Optional filter:
- `tasks` - Organize only task extractions
- `definitions` - Organize only term/definition extractions
- `people` - Organize only people extractions
- `meetings` - Organize only meeting notes
- `wiki` - Generate only wiki proposals (to proposed-updates/)
- `status` - Organize only project status content
- `jira` - Generate only JIRA draft tickets
- `all` - Organize everything (default)

## Prerequisites

- Files must have been processed (extractions exist)
- Knowledge base directories must exist

## Task

Read extractions from `extractions/` and organize into `knowledge/`:

### 1. Load Extractions

Scan `extractions/` for files that haven't been organized:
- `*-summary.md` - Contains themes, decisions (→ project-status)
- `*-tasks.md` - Contains action items (→ tasks, jira-drafts)
- `*-entities.md` - Contains people, terms (→ people, definitions)
- `*-meeting.md` - Contains structured meeting notes (→ meetings)
- `*-wiki.md` - Contains wiki content proposals (→ proposed-updates)

### 2. Process Task Extractions

For each task extraction file:

#### Route to `knowledge/tasks/`

1. Read existing task files to avoid duplicates
2. Group tasks by project or epic
3. Append new tasks to appropriate file or create new one

File format: `knowledge/tasks/<project>-tasks.md`

```markdown
---
type: task-collection
project: project-name
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources:
  - processed/source1.md
  - processed/source2.md
---

# Project Name - Tasks

## Active Tasks

### Task: Title
| Field | Value |
|-------|-------|
| Assignee | Name |
| Deadline | Date |
| Priority | High |
| Status | Pending |
| Source | [document](../processed/file.md) |

**Description:** ...

---

## Completed Tasks

### Task: Title
[completed task details]
```

#### Route to `knowledge/jira-drafts/`

For tasks marked as "JIRA candidates":

File format: `knowledge/jira-drafts/draft-<title>.md`

```markdown
---
type: jira-draft
created: YYYY-MM-DD
source_document: processed/file.md
suggested_project: PROJ
---

# [Draft] Ticket Title

**Type:** Story | Bug | Task
**Priority:** High | Medium | Low
**Suggested Assignee:** Name

## Summary
One-line summary

## Description
Detailed description

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Source Context
> Original discussion quote

**From:** [source](../processed/file.md)
```

### 3. Process Entity Extractions

#### Route People to `knowledge/people/`

For each person identified:

1. Check if person profile exists
2. If exists: Update with new information
3. If new: Create new profile

File format: `knowledge/people/<firstname>-<lastname>.md`

```markdown
---
type: person
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources:
  - processed/source1.md
---

# Full Name

## Basic Info
| Field | Value |
|-------|-------|
| Role | Title |
| Team | Team Name |
| Expertise | Areas |

## Document Mentions
| Date | Document | Context |
|------|----------|---------|
| YYYY-MM-DD | file.md | Brief context |
```

#### Route Definitions to `knowledge/definitions/`

For each term/definition:

1. Check if definition exists
2. If exists: Enhance with new context
3. If new: Create new definition

File format: `knowledge/definitions/<term>.md`

```markdown
---
type: definition
term: Term Name
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources:
  - processed/source1.md
---

# Term Name

**Also known as:** Alias1, Alias2

## Definition
Clear definition text.

## Context
How it's used in the project.

## Sources
- First defined: [document](../processed/file.md)
```

### 4. Process Meeting Notes Extractions

Route meeting notes to `knowledge/meetings/`:

For each meeting extraction file (`*-meeting.md`):

1. Extract meeting date and topic from frontmatter
2. Create file in knowledge/meetings/

File format: `knowledge/meetings/YYYY-MM-DD-<topic>.md`

```markdown
---
type: meeting-notes
meeting_date: YYYY-MM-DD
meeting_type: sprint-planning | architecture-review | standup | etc.
meeting_topic: Topic Name
source_document: processed/YYYY-MM-DD-source.md
participants:
  - Name 1
  - Name 2
created: YYYY-MM-DD
---

# Meeting: <Topic>

**Date:** YYYY-MM-DD
**Type:** <Meeting Type>
**Participants:** Name 1, Name 2
**Source:** [Original Document](../processed/filename.md)

## Executive Summary & Talking Points

### Executive Summary
<Content from extraction>

### Key Talking Points
<Content from extraction>

## Action Items & Next Steps

### Action Items
<Table from extraction>

### Next Steps
<Content from extraction>

## Key Decisions & Architectural Principles

### Decisions Made
<Content from extraction>

### Architectural Principles
<Content from extraction>

## Risks, Blockers, & Open Questions

### Risks
<Content from extraction>

### Blockers
<Content from extraction>

### Open Questions
<Content from extraction>

---

**Extracted:** YYYY-MM-DD
```

### 5. Process Summary Extractions

#### Route Decisions/Status to `knowledge/project-status/`

1. Identify project from context
2. Update or create project status file

File format: `knowledge/project-status/<project>-status.md`

```markdown
---
type: status
project: project-name
updated: YYYY-MM-DD
sources:
  - processed/source1.md
---

# Project Name - Status

## Latest Update
**Date:** YYYY-MM-DD
**Source:** [meeting](../processed/file.md)

### Summary
Brief current state.

### Recent Decisions
- Decision 1 (YYYY-MM-DD)
- Decision 2 (YYYY-MM-DD)

### Current Focus
- Focus area 1
- Focus area 2
```

### 6. Process Wiki Content Extractions (Proposals Only)

**IMPORTANT**: Wiki content is NOT directly written to `knowledge/wiki/`. Instead, generate proposals in `proposed-updates/` for human review.

For each wiki extraction file (`*-wiki.md`):

1. Read existing wiki articles in `knowledge/wiki/`
2. For each wiki item in the extraction:
   - If article exists: Generate UPDATE proposal
   - If article is new: Generate CREATE proposal
3. Write proposal to `proposed-updates/`

#### Proposal for New Wiki Article

File: `proposed-updates/wiki-new-NNN-<topic>.md`

```markdown
---
type: proposed-update
proposal_id: wiki-new-001
created: YYYY-MM-DD
target_file: knowledge/wiki/<topic>.md
change_type: create
source_document: processed/<file>.md
wiki_category: technical | best-practices | product-business
confidence: high | medium | low
status: pending_review
---

# Proposed: New Wiki Article - <Topic>

## Summary

<Why this article should be created based on source content>

## Proposed Content

```markdown
---
type: wiki
topic: <Topic>
category: <category>
created: YYYY-MM-DD
sources:
  - processed/<source>.md
---

# <Topic>

## Overview
<Content extracted from source>

## Details
<Detailed content>

## Sources
- [Source Document](../processed/<file>.md)
```

## Source Evidence

> "<Relevant quote from the document>"
> — <Speaker/Author>

## Confidence

**<Level>** - <Rationale for confidence level>

---

## Review Actions

- [ ] Approve and apply
- [ ] Modify and apply
- [ ] Reject
- [ ] Defer

**Reviewer Notes:**
_Add notes here when reviewing_
```

#### Proposal for Wiki Update

File: `proposed-updates/wiki-update-NNN-<topic>.md`

```markdown
---
type: proposed-update
proposal_id: wiki-update-001
created: YYYY-MM-DD
target_file: knowledge/wiki/<existing-topic>.md
change_type: update
source_document: processed/<file>.md
wiki_category: technical | best-practices | product-business
confidence: high | medium | low
status: pending_review
---

# Proposed: Update Wiki - <Topic>

## Summary

<Why this update should be made>

## Target

**File:** knowledge/wiki/<topic>.md
**Section:** <Which section to update, if specific>

## Current Content

```markdown
<Current content of the section being updated>
```

## Proposed Addition/Change

```markdown
<New or modified content to add>
```

## Rationale

<Why this change improves the article>

## Source Evidence

> "<Quote from new document>"
> — <Speaker/Author>

## Confidence

**<Level>** - <Rationale>

---

## Review Actions

- [ ] Approve and apply
- [ ] Modify and apply
- [ ] Reject
- [ ] Defer

**Reviewer Notes:**
_Add notes here when reviewing_
```

### 7. Mark Extractions as Organized

After organizing, update extraction files:

```yaml
---
# ... existing frontmatter ...
organized: true
organized_date: YYYY-MM-DD
organized_to:
  - knowledge/tasks/project-tasks.md
  - knowledge/people/john-smith.md
  - knowledge/meetings/2024-01-15-sprint-planning.md
  - proposed-updates/wiki-new-001-deployment.md
---
```

### 8. Log Results

Append to `logs/organize-YYYY-MM-DD.md`:

```markdown
## Organization Log - <timestamp>

| Category | New | Updated | Proposals |
|----------|-----|---------|-----------|
| Tasks | 3 | 2 | - |
| People | 2 | 1 | - |
| Definitions | 4 | 0 | - |
| Meetings | 2 | - | - |
| JIRA Drafts | 2 | - | - |
| Wiki | - | - | 3 |
| Status | 1 | 1 | - |
```

## Output

Report what was organized:

```
Organization Complete

Extractions Processed: X

Tasks:
- 3 new tasks added to project-alpha-tasks.md
- 2 tasks updated in project-beta-tasks.md
- 2 JIRA drafts created

People:
- 2 new profiles created (john-smith, jane-doe)
- 1 profile updated (bob-wilson)

Definitions:
- 4 new terms added to glossary

Meetings:
- 2 meeting notes created (sprint-planning, architecture-review)

Wiki Proposals:
- 3 proposals created in proposed-updates/
  - wiki-new-001: deployment-process (high confidence)
  - wiki-new-002: api-patterns (medium confidence)
  - wiki-update-001: architecture-overview (high confidence)

Project Status:
- 1 status update added to project-alpha

See knowledge/ directory for organized content.
Run /review to apply wiki proposals.
```

## Duplicate Handling

When content might be duplicate:
- Tasks: Compare description and assignee
- People: Match by normalized name
- Definitions: Match by term (case-insensitive)
- Meetings: Match by date + topic
- If duplicate detected: Update existing, don't create new
- If unsure: Create entry but flag for review

## Error Handling

- If extractions/ empty: "No extractions to organize"
- If extraction already organized: Skip (unless force flag)
- If knowledge directory missing: Create it
- If write fails: Log error, continue with others
