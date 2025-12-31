---
description: Analyze documents in to-process/ - extract summaries, tasks, entities, definitions
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task
argument-hint: [filename|all]
---

# Document Processing Pipeline (Stage 2)

Analyze documents in `to-process/` and extract structured information.

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

### 2. Run Analysis Subagents

Delegate to specialized subagents for deep analysis:

#### Document Analyzer
Use the `document-analyzer` subagent to:
- Generate executive summary
- Identify key points and themes
- Extract decisions made
- Note open questions

#### Task Extractor
Use the `task-extractor` subagent to:
- Find all action items and tasks
- Identify assignees and deadlines
- Assess priority levels
- Flag items that should become JIRA tickets

#### Entity Extractor
Use the `entity-extractor` subagent to:
- Identify people mentioned
- Extract project/initiative names
- Find technical terms and acronyms
- Capture definitions (explicit and contextual)

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
[Full task details with all fields]

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
  task_count: X
  people_count: X
  definition_count: X
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

| Document | Tasks | People | Definitions |
|----------|-------|--------|-------------|
| file.md | 5 | 3 | 2 |

### Details
- file.md: 5 tasks (2 high priority), 3 people, 2 new definitions
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
- JIRA Candidates: 2 suggested

Extractions written to: extractions/
Documents moved to: processed/
```

## Error Handling

- If `to-process/` is empty: Report "No files to process"
- If document missing frontmatter: Skip with warning, leave in to-process/
- If subagent fails: Log error, mark as partial processing
- If extraction already exists: Add numeric suffix or update existing
