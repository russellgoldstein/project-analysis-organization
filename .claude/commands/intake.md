---
description: Process raw input files - detect source, rename, add metadata, move to to-process/
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
argument-hint: [filename|all]
---

# Document Intake Pipeline (Stage 1)

Process files from the `raw/` directory through the intake pipeline.

## Arguments

`$ARGUMENTS` - Optional:
- Specific filename to process
- "all" to process all files in raw/
- If empty, process all files

## Prerequisites

- Working directory should be the project directory (contains `raw/`, `to-process/`, etc.)
- Or the project path should be configured

## Task

For each file in `raw/`:

### 1. Read and Analyze Content

Read the file and detect the source type based on content patterns:

**Zoom Transcript** indicators:
- Timestamps like `00:15:32` or `HH:MM:SS` format
- Speaker labels followed by transcript: `John Smith: Hello everyone`
- Common phrases: "you're on mute", "can you hear me", "share my screen"
- WEBVTT header

**Slack Conversation** indicators:
- Time formats: `10:30 AM`, `2:45 PM`
- Channel references: `#channel-name`
- User mentions: `@username`
- Thread indicators: "replied to a thread", "in thread"
- Reactions: `:emoji:` patterns
- "Slack" in content

**JIRA Ticket** indicators:
- Ticket ID patterns: `PROJ-1234`, `[A-Z]+-\d+`
- Fields: "Summary:", "Description:", "Acceptance Criteria:", "Story Points:"
- Status values: "To Do", "In Progress", "Done", "Blocked"
- Sprint references

**Confluence/Wiki** indicators:
- Wiki-style headers with multiple `=` or `#`
- Table of contents patterns
- "Page" or "Space" references
- Confluence-specific formatting

**Email** indicators:
- Headers: "From:", "To:", "Subject:", "Date:", "Sent:"
- "Re:", "Fwd:", "FW:" prefixes
- Email address patterns
- Signature blocks ("--", "Best regards", etc.)

**Meeting Notes** indicators:
- "Agenda", "Attendees", "Minutes", "Action Items" sections
- Date headers at top
- Structured bullet points
- "Meeting Notes" or "Minutes" in title/content

**Default**: `notes` (general notes when no pattern matches)

### 2. Extract Date

Try to extract the document date from:
1. Content (meeting date, email date, transcript date)
2. Filename (if contains date pattern)
3. File modification date (fallback)

Use format: `YYYY-MM-DD`

### 3. Generate Short Description

Create a short description (max 50 chars, lowercase, hyphens for spaces):
- For meetings: topic or attendees
- For Slack: channel or main topic
- For JIRA: ticket ID and brief summary
- For email: subject line simplified
- Default: first meaningful words from content

### 4. Extract Participants

For Zoom/meetings: List of speaker names
For Slack: List of @mentioned users
For email: From/To/CC names
For JIRA: Reporter, Assignee
Otherwise: Empty list

### 5. Generate New Filename

Format: `YYYY-MM-DD-<source>-<short-description>.md`

Examples:
- `2024-01-15-zoom-sprint-planning.md`
- `2024-01-16-slack-data-pipeline-discussion.md`
- `2024-01-17-jira-proj-1234-auth-bug.md`
- `2024-01-18-email-quarterly-review.md`

### 6. Create Output File

Write to `to-process/` with YAML frontmatter:

```yaml
---
source: <detected-source>
original_filename: <original-filename>
intake_date: <today-YYYY-MM-DD>
document_date: <extracted-date>
status: pending
participants:
  - Name 1
  - Name 2
tags: []
source_confidence: high|medium|low
---

# <Title derived from content>

## Original Content

<original content preserved exactly>
```

### 7. Move/Archive Original

After successful processing:
- The original in `raw/` can be deleted or moved to an archive
- Log the action

### 8. Log Results

Append to `logs/intake-YYYY-MM-DD.md`:

```markdown
## Intake Log - <timestamp>

| Original | New Name | Source | Confidence |
|----------|----------|--------|------------|
| file1.txt | 2024-01-15-zoom-sprint.md | zoom | high |
```

## Output

Report what was processed:

```
Intake Complete

Processed: X files
- original.txt -> 2024-01-15-zoom-sprint-planning.md (zoom, high confidence)
- notes.md -> 2024-01-16-notes-architecture-review.md (notes, medium confidence)

Files moved to: to-process/
```

## Error Handling

- If `raw/` is empty: Report "No files to process in raw/"
- If file already exists in `to-process/`: Add numeric suffix or skip with warning
- If source detection fails: Use "notes" as default, mark as "low" confidence
- If date extraction fails: Use today's date
