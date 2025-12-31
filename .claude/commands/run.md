---
description: Run the full document processing pipeline - intake, process, organize, crossref
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task
argument-hint: [--skip-crossref] [--dry-run]
---

# Full Pipeline Execution

Run all 4 stages of the document processing pipeline in sequence.

## Arguments

`$ARGUMENTS` - Optional flags:
- `--skip-crossref` - Skip Stage 4 (cross-reference)
- `--dry-run` - Show what would be done without making changes
- (empty) - Run full pipeline

## Pipeline Stages

```
Stage 1: INTAKE
raw/ → to-process/
├── Detect source types
├── Rename files
├── Add metadata headers
└── Move to to-process/

Stage 2: PROCESS
to-process/ → processed/ + extractions/
├── Analyze with document-analyzer
├── Extract tasks with task-extractor
├── Extract entities with entity-extractor
└── Create extraction files

Stage 3: ORGANIZE
extractions/ → knowledge/
├── Route tasks to knowledge/tasks/
├── Route people to knowledge/people/
├── Route definitions to knowledge/definitions/
├── Route status to knowledge/project-status/
├── Create JIRA drafts
└── Create wiki articles

Stage 4: CROSSREF
processed/ + knowledge/ → proposed-updates/
├── Compare new docs to knowledge base
├── Find contradictions and updates
├── Generate proposals
└── Never auto-apply changes
```

## Execution

### Pre-Flight Check

Before running:
1. Verify project structure exists
2. Count files in raw/
3. Check for pending work in other stages

Report:
```
Pipeline Pre-Flight Check
=========================
Project: <project-name>
Raw files to process: X
Already in to-process: Y
Already in processed: Z
Pending extractions: W

Ready to proceed? Running full pipeline...
```

### Stage 1: Intake

Run the intake process:
1. Process all files in raw/
2. Report results
3. Continue to Stage 2

```
Stage 1: INTAKE
===============
Processing raw/ files...

Results:
- 3 files processed
- zoom-call.txt → 2024-01-15-zoom-sprint-review.md
- slack-export.txt → 2024-01-15-slack-discussion.md
- notes.md → 2024-01-15-notes-architecture.md

Continuing to Stage 2...
```

### Stage 2: Process

Run the processing:
1. Analyze all files in to-process/
2. Create extractions
3. Move to processed/
4. Continue to Stage 3

```
Stage 2: PROCESS
================
Analyzing to-process/ files...

Results:
- 3 documents analyzed
- 8 tasks extracted
- 5 people identified
- 6 definitions found
- 3 JIRA candidates identified

Continuing to Stage 3...
```

### Stage 3: Organize

Run the organization:
1. Read extractions
2. Route to knowledge base
3. Continue to Stage 4 (unless skipped)

```
Stage 3: ORGANIZE
=================
Organizing extractions...

Results:
- 8 tasks added to knowledge/tasks/
- 5 people profiles updated
- 6 definitions added to glossary
- 3 JIRA drafts created
- 1 wiki article created

Continuing to Stage 4...
```

### Stage 4: Cross-Reference

Run cross-referencing (unless skipped):
1. Compare new docs to knowledge base
2. Generate proposals
3. Report findings

```
Stage 4: CROSSREF
=================
Cross-referencing with knowledge base...

Results:
- 3 documents analyzed
- 2 update proposals created
- 1 contradiction found
- 5 relationships discovered

Proposals in: proposed-updates/
```

## Final Summary

```
Pipeline Complete
=================

SUMMARY
-------
Raw files processed:     3
Documents analyzed:      3
Tasks extracted:         8
People identified:       5
Definitions found:       6
JIRA drafts created:     3
Update proposals:        2

NEXT STEPS
----------
1. Review JIRA drafts in knowledge/jira-drafts/
2. Review update proposals in proposed-updates/
3. Run /status for current pipeline state

REMINDERS
---------
- Proposed updates require manual review before applying
- JIRA drafts are ready to copy into your issue tracker
- New definitions may need expert review
```

## Error Handling

### Stage Failure

If a stage fails:
1. Stop pipeline
2. Report error
3. Show what completed
4. Suggest recovery steps

```
ERROR: Stage 2 failed
======================
Stage 1 completed successfully (3 files intake)
Stage 2 failed: document-analyzer error

Completed Work:
- Files in to-process/ ready to retry
- No extractions created

Recovery:
- Fix the issue and run /process
- Or run /run again to retry full pipeline
```

### Partial Success

If some files fail within a stage:
1. Continue with successful files
2. Report failures at end
3. Failed files remain in their stage

```
Stage 2: PROCESS (Partial)
==========================
Processed: 2 of 3 files

Failures:
- corrupt-file.md: Could not parse content

Continuing with successful files...
```

## Dry Run Mode

With `--dry-run`:

```
Pipeline Dry Run
================

Would process:
Stage 1: 3 files from raw/
Stage 2: 3 documents to analyze
Stage 3: Organize extractions to knowledge/
Stage 4: Cross-reference with knowledge base

No changes made. Remove --dry-run to execute.
```

## Skip Cross-Reference

With `--skip-crossref`:

Useful when:
- Initial bulk import
- Cross-ref taking too long
- Want to organize first, crossref later

```
Pipeline Complete (Stages 1-3)
==============================

Skipped Stage 4 (cross-reference) as requested.

To run cross-reference later:
  /crossref all
```

## Tips

- **First run**: Use `--skip-crossref` for initial bulk import
- **Regular use**: Run full pipeline for ongoing document processing
- **Check status**: Run `/status` before and after to see changes
- **Review proposals**: Always review `proposed-updates/` after running
