---
description: Cross-reference new documents with existing knowledge, generate proposed updates
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task
argument-hint: [filename|all]
---

# Cross-Reference Pipeline (Stage 4)

Analyze relationships between new documents and existing knowledge base, generating proposed updates for review.

## Arguments

`$ARGUMENTS` - Optional:
- Specific filename to cross-reference
- "all" to cross-reference all recent documents
- If empty, cross-reference documents processed today

## Prerequisites

- Documents must have been processed and organized
- Knowledge base should have existing content to compare against

## Task

Compare new/recent documents against existing knowledge to find updates, contradictions, and relationships.

### 1. Identify Target Documents

Determine which documents to cross-reference:
- If filename specified: that document only
- If "all": all processed documents not yet cross-referenced
- If empty: documents processed in last 24 hours

### 2. Load Knowledge Base Context

Build context from existing knowledge:
- `knowledge/tasks/` - Current task status
- `knowledge/definitions/` - Existing definitions
- `knowledge/people/` - Known people and roles
- `knowledge/project-status/` - Current project state
- `knowledge/wiki/` - Reference articles

### 3. Run Cross-Reference Analysis

Use the `crossref-analyzer` subagent to:

#### Find Contradictions
- Task status conflicts (done vs in-progress)
- Role/team changes for people
- Definition conflicts
- Decision reversals

#### Find Updates Needed
- New information about existing topics
- Progress updates on tracked tasks
- Additional context for definitions
- Role changes for people

#### Find Relationships
- Documents discussing same topics
- People connected through projects
- Tasks related to each other
- Terms used across documents

#### Find Duplicates
- Same info in multiple places
- Similar definitions
- Redundant task entries

### 4. Generate Proposed Updates

For each finding, create a proposal in `proposed-updates/`:

**File naming:** `update-<NNN>-<brief-description>.md`

```markdown
---
type: proposed-update
proposal_id: update-001
created: YYYY-MM-DD
target_file: knowledge/tasks/project-alpha-tasks.md
change_type: update
source_document: processed/2024-01-15-zoom-sprint-review.md
confidence: high
status: pending_review
---

# Proposed Update: Task Status Change

## Target

**File:** knowledge/tasks/project-alpha-tasks.md
**Section:** Task "Implement authentication"

## Change Type

`update` - Status change for existing task

## Current Content

```markdown
| Status | Pending |
```

## Proposed Content

```markdown
| Status | Done |
| Completed | 2024-01-15 |
```

## Rationale

In the sprint review, John Smith confirmed the authentication task was completed and merged.

## Source Evidence

**Document:** processed/2024-01-15-zoom-sprint-review.md

> "The authentication work is done, we merged it yesterday and it's in production now."
> — John Smith

## Confidence

**High** - Explicit statement from task owner confirming completion.

---

## Review Actions

- [ ] Approve and apply
- [ ] Modify and apply
- [ ] Reject
- [ ] Defer

**Reviewer Notes:**
_Add notes here when reviewing_
```

### 5. Generate Summary Report

Create a summary of all findings:

```markdown
## Cross-Reference Summary

**Analysis Date:** YYYY-MM-DD
**Documents Analyzed:** X
**Knowledge Base Entries Scanned:** Y

### Findings Overview

| Category | Count | Action Required |
|----------|-------|-----------------|
| Contradictions | 2 | Review needed |
| Updates | 5 | Proposals created |
| Relationships | 8 | Links suggested |
| Duplicates | 1 | Merge suggested |

### Proposed Updates Created

| ID | Target | Type | Confidence |
|----|--------|------|------------|
| update-001 | tasks/project.md | Status change | High |
| update-002 | people/john.md | Role update | Medium |
| update-003 | definitions/term.md | Clarification | Low |

### No Action Needed

- wiki/architecture.md: Content matches, no update
- people/jane.md: New mention, profile current

### Manual Review Recommended

- Contradiction between meeting-1 and meeting-2 on timeline
- Possible duplicate definitions: "API Gateway" vs "Gateway Service"
```

### 6. Mark Documents as Cross-Referenced

Update processed documents:

```yaml
---
# ... existing frontmatter ...
crossref_date: YYYY-MM-DD
crossref_proposals:
  - proposed-updates/update-001.md
  - proposed-updates/update-002.md
---
```

### 7. Log Results

Append to `logs/crossref-YYYY-MM-DD.md`:

```markdown
## Cross-Reference Log - <timestamp>

Documents: X analyzed
Proposals: Y generated
- update-001: task status (high)
- update-002: person role (medium)

Contradictions found: Z
Relationships discovered: W
```

## Output

Report what was found:

```
Cross-Reference Complete

Documents Analyzed: 3
Knowledge Base Entries Scanned: 47

Findings:
- 2 contradictions requiring review
- 5 update proposals created
- 8 relationships discovered
- 1 potential duplicate found

Proposals Created:
- update-001: Task status change (high confidence)
- update-002: Person role update (medium confidence)
- update-003: Definition clarification (low confidence)
- update-004: Project status update (high confidence)
- update-005: New wiki article suggested (medium confidence)

Review proposals in: proposed-updates/

IMPORTANT: No changes were auto-applied. Review each proposal before applying.
```

## Important Notes

**NO AUTO-UPDATES**: This stage NEVER modifies existing knowledge base files automatically. All changes are proposed only.

**Review Required**: Every proposal must be reviewed by a human before applying.

**Confidence Matters**: Low confidence proposals may be incorrect and should be carefully reviewed.

## Error Handling

- If no documents to analyze: "No documents to cross-reference"
- If knowledge base empty: "Knowledge base empty, nothing to compare against"
- If crossref agent fails: Log error, partial results if available
- If proposal write fails: Log error, continue with others
