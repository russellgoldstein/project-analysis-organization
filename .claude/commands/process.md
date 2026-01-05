---
description: Analyze documents in to-process/ - extract summaries, tasks, entities, meeting notes, wiki content
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task
argument-hint: [filename|all]
---

# Document Processing Pipeline (Stage 2)

Analyze documents in `to-process/` and extract structured information using LLM subagents.

## Arguments

`$ARGUMENTS` - Optional:
- Specific filename to process
- "all" to process all files in to-process/
- If empty, process all files

## Prerequisites

- Files must have been through intake (have proper frontmatter)
- Working directory should be the project directory

## Task

For each file in `to-process/`:

### 1. Load Document

Read the file and its frontmatter metadata:
- Verify it has proper intake frontmatter
- Note the source type, participants, document date
- Determine if this is a meeting-type document (source: `zoom`, `meeting`, or has meeting indicators)

### 2. Run Analysis Subagents

Use the Task tool to invoke specialized subagents. Run subagents in parallel where possible for efficiency.

#### Core Subagents (Always Run)

**Document Analyzer** (`document-analyzer`)
- Generate executive summary
- Identify key points and themes
- Extract decisions made
- Note open questions

**Task Extractor** (`task-extractor`)
- Find all action items and tasks
- Identify assignees and deadlines
- Assess priority levels
- Flag items that should become JIRA tickets

**Entity Extractor** (`entity-extractor`)
- Identify people mentioned
- Extract project/initiative names
- Find technical terms and acronyms
- Capture definitions (explicit and contextual)

#### Conditional Subagents

**Meeting Notes Extractor** (`meeting-notes-extractor`)
- **Condition**: Run when source is `zoom`, `meeting`, or document contains meeting indicators (agenda, attendees, minutes, action items)
- Extract structured meeting notes with 4 sections:
  - Executive Summary & Talking Points
  - Action Items & Next Steps
  - Key Decisions & Architectural Principles
  - Risks, Blockers, & Open Questions

**Wiki Content Extractor** (`wiki-content-extractor`)
- **Always run** on all documents
- Identify wiki-worthy content in 3 categories:
  - Technical Implementation Details
  - Best Practices & Patterns
  - Product Requirements & Business Context
- Generate proposals for new or updated wiki articles

### 3. Create Extraction Files

Write extraction results to `extractions/`:

#### Summary Extraction
File: `extractions/<original-name>-summary.md`

```markdown
---
type: extraction
extraction_type: summary
source_document: to-process/<filename>
extracted_date: YYYY-MM-DD
---

# Summary: <Document Title>

## Executive Summary
<2-3 sentence summary>

## Key Points
- Point 1
- Point 2

## Decisions Made
- Decision 1
- Decision 2

## Open Questions
- Question 1
- Question 2

## Themes/Tags
- theme1
- theme2
```

#### Tasks Extraction
File: `extractions/<original-name>-tasks.md`

```markdown
---
type: extraction
extraction_type: tasks
source_document: to-process/<filename>
extracted_date: YYYY-MM-DD
task_count: X
---

# Tasks: <Document Title>

## Task Summary

| Assignee | Count | High Priority |
|----------|-------|---------------|
| Name | X | X |

## Tasks

### Task 1: <Title>
| Field | Value |
|-------|-------|
| Assignee | Name |
| Deadline | YYYY-MM-DD |
| Priority | High/Med/Low |
| Status | Pending |

**Description:** Task description

### Task 2: <Title>
[Full task details]

## JIRA Candidates
- Task X - <rationale>
- Task Y - <rationale>
```

#### Entities Extraction
File: `extractions/<original-name>-entities.md`

```markdown
---
type: extraction
extraction_type: entities
source_document: to-process/<filename>
extracted_date: YYYY-MM-DD
---

# Entities: <Document Title>

## People

| Name | Role | Team | Confidence |
|------|------|------|------------|
| Name | Role | Team | High/Med/Low |

## Projects

| Name | Status | Description |
|------|--------|-------------|
| Name | Status | Brief |

## Terms & Definitions

| Term | Definition | Type |
|------|------------|------|
| Term | Definition | Acronym/Concept |

## Relationships
- Person → Project
- Term → Project
```

#### Meeting Notes Extraction (Conditional)
File: `extractions/<original-name>-meeting.md`

Only created when document is a meeting-type document.

```markdown
---
type: extraction
extraction_type: meeting-notes
source_document: to-process/<filename>
extracted_date: YYYY-MM-DD
meeting_date: YYYY-MM-DD
meeting_type: <type>
meeting_topic: <topic>
participants:
  - Name 1
  - Name 2
---

# Meeting Notes: <Topic>

## Executive Summary & Talking Points

### Executive Summary
<2-3 sentence summary>

### Key Talking Points
- **Point 1**: Description
- **Point 2**: Description

## Action Items & Next Steps

### Action Items

| Action | Assignee | Deadline | Priority |
|--------|----------|----------|----------|
| Task | Name | Date | High/Med/Low |

### Next Steps
- Follow-up 1
- Follow-up 2

## Key Decisions & Architectural Principles

### Decisions Made

| Decision | Decided By | Rationale |
|----------|------------|-----------|
| Decision | Name | Why |

### Architectural Principles
- **Principle**: Description

## Risks, Blockers, & Open Questions

### Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Risk | High/Med/Low | Mitigation |

### Blockers

| Blocker | Owner | Resolution Path |
|---------|-------|-----------------|
| Blocker | Name | Resolution |

### Open Questions

| Question | Needs Answer From | Urgency |
|----------|-------------------|---------|
| Question | Name/Team | High/Med/Low |
```

#### Wiki Content Extraction
File: `extractions/<original-name>-wiki.md`

```markdown
---
type: extraction
extraction_type: wiki-content
source_document: to-process/<filename>
extracted_date: YYYY-MM-DD
wiki_items_count: X
---

# Wiki Content: <Document Title>

## Summary
<Overview of wiki-worthy content found>

## Wiki Items

### Item 1: <Topic>

**Category:** Technical | Best Practices | Product/Business
**Action:** create | update
**Target:** knowledge/wiki/<slug>.md
**Confidence:** High | Medium | Low

**Content:**
<Extracted content for wiki article>

**Source Quote:**
> "<Quote from document>"
> — Speaker

### Item 2: <Topic>
[Repeat structure]
```

### 4. Update Original Document

Update the document in place with processing metadata:

```yaml
---
# ... existing frontmatter ...
status: processed
processed_date: YYYY-MM-DD
extracted:
  summary: extractions/<name>-summary.md
  tasks: extractions/<name>-tasks.md
  entities: extractions/<name>-entities.md
  meeting: extractions/<name>-meeting.md  # if applicable
  wiki: extractions/<name>-wiki.md
  task_count: X
  people_count: X
  definition_count: X
  wiki_items_count: X
tags:
  - extracted-theme1
  - extracted-theme2
---
```

### 5. Move to Processed

Move the updated document to `processed/`:
- Keep the same filename
- Original now has extraction references

### 6. Log Results

Append to `logs/process-YYYY-MM-DD.md`:

```markdown
## Processing Log - <timestamp>

| Document | Tasks | People | Definitions | Meeting Notes | Wiki Items |
|----------|-------|--------|-------------|---------------|------------|
| file.md | 5 | 3 | 2 | Yes | 2 |

### Details
- file.md: 5 tasks (2 high priority), 3 people, 2 definitions, meeting notes extracted, 2 wiki items
```

## Output

Report what was processed:

```
Processing Complete

Processed: X documents

Document: 2024-01-15-zoom-sprint-planning.md
- Summary: Generated
- Tasks: 5 extracted (2 high priority)
- People: 3 identified
- Definitions: 2 found
- Meeting Notes: Extracted (4 sections)
- Wiki Content: 2 items identified
- JIRA Candidates: 2 suggested

Extractions written to: extractions/
Documents moved to: processed/
```

## Subagent Orchestration

### Parallel Execution

For efficiency, run independent subagents in parallel using multiple Task tool calls in a single message:

```
1. Launch in parallel:
   - document-analyzer
   - task-extractor
   - entity-extractor
   - wiki-content-extractor

2. If meeting-type document, also launch:
   - meeting-notes-extractor
```

### Cost Management

- Use `model: sonnet` for all extraction subagents (cost-effective)
- Cache results in frontmatter to avoid re-processing
- Check `status: processed` before re-running
- Batch multiple documents when processing in bulk

## Error Handling

- If `to-process/` is empty: Report "No files to process"
- If document missing frontmatter: Skip with warning, leave in to-process/
- If subagent fails: Log error, mark as partial processing, continue with others
- If extraction already exists: Add numeric suffix or update existing
