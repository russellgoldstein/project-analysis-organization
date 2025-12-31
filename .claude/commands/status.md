---
description: Show pipeline status dashboard - file counts, knowledge base stats, pending proposals
allowed-tools: Bash, Glob, Read
---

# Pipeline Status Dashboard

Display the current state of the document processing pipeline.

## Task

Scan the project directory and report on all pipeline stages.

## Status Report Format

Generate a report like this:

```
Pipeline Status Report
======================
Project: <project-name>
Generated: YYYY-MM-DD HH:MM

PIPELINE STAGES
---------------
Raw (Intake Queue):        X files waiting
To-Process (Analysis):     X files pending
Processed (Complete):      X files done
Extractions (Organize):    X files pending

KNOWLEDGE BASE
--------------
Project Status:    X entries
Tasks:             X entries
Definitions:       X entries
Wiki Articles:     X entries
People Profiles:   X entries
JIRA Drafts:       X drafts

REVIEW QUEUE
------------
Proposed Updates:  X pending review

RECENT ACTIVITY
---------------
Last intake:   YYYY-MM-DD (X files)
Last process:  YYYY-MM-DD (X files)
Last organize: YYYY-MM-DD
Last crossref: YYYY-MM-DD (X proposals)
```

## Implementation Steps

1. **Load Configuration**
   - Read `.env` for PROJECT_NAME
   - Default to directory name if not set

2. **Count Files in Pipeline Stages**
   - `raw/` - Count .txt and .md files
   - `to-process/` - Count .md files
   - `processed/` - Count .md files
   - `extractions/` - Count .md files

3. **Count Knowledge Base Entries**
   - `knowledge/project-status/` - Count .md files
   - `knowledge/tasks/` - Count .md files
   - `knowledge/definitions/` - Count .md files
   - `knowledge/wiki/` - Count .md files
   - `knowledge/people/` - Count .md files
   - `knowledge/jira-drafts/` - Count .md files

4. **Count Pending Reviews**
   - `proposed-updates/` - Count .md files with status: pending_review

5. **Check Recent Activity**
   - Read latest log files from `logs/`
   - Extract dates and counts from log entries

6. **Format Output**
   - Use aligned columns for readability
   - Highlight any items needing attention (e.g., many pending files)

## Additional Details (if requested)

If the user asks for more details, show:

### Files in Each Stage

```
RAW FILES (3):
  - meeting-notes.txt (2.3 KB, modified today)
  - slack-export.txt (15 KB, modified yesterday)
  - transcript.vtt (45 KB, modified 3 days ago)

TO-PROCESS (2):
  - 2024-01-15-zoom-sprint-planning.md (source: zoom)
  - 2024-01-16-slack-discussion.md (source: slack)
```

### Pending Proposals

```
PROPOSED UPDATES (3):
  - update-001: Task status change (high confidence)
  - update-002: Person role update (medium confidence)
  - update-003: Definition clarification (low confidence)
```

## Error Handling

- If directory doesn't exist: Report as "0 (directory not found)"
- If `.env` missing: Use defaults, note configuration needed
- If completely empty project: Suggest running `/init-project` first
