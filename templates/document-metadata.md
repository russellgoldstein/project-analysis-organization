# Document Metadata Template

Use this template for YAML frontmatter on all documents.

## Intake Stage (to-process/)

```yaml
---
source: zoom|slack|jira|confluence|email|meeting|notes
original_filename: original-name.txt
intake_date: YYYY-MM-DD
document_date: YYYY-MM-DD
status: pending
participants:
  - Name One
  - Name Two
tags: []
source_confidence: high|medium|low
---
```

## Processed Stage (processed/)

```yaml
---
source: zoom|slack|jira|confluence|email|meeting|notes
original_filename: original-name.txt
intake_date: YYYY-MM-DD
document_date: YYYY-MM-DD
processed_date: YYYY-MM-DD
status: processed
participants:
  - Name One
  - Name Two
tags:
  - extracted-tag1
  - extracted-tag2
extracted:
  summary: extractions/filename-summary.md
  tasks: extractions/filename-tasks.md
  entities: extractions/filename-entities.md
  task_count: 5
  people_count: 3
  definition_count: 2
related_documents:
  - path/to/related.md
crossref_date: YYYY-MM-DD
crossref_proposals:
  - proposed-updates/update-001.md
---
```

## Knowledge Base Entry

```yaml
---
type: task|definition|wiki|person|status|jira-draft
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources:
  - processed/source-document.md
tags:
  - tag1
  - tag2
---
```

## Extraction File

```yaml
---
type: extraction
extraction_type: summary|tasks|entities
source_document: to-process/filename.md
extracted_date: YYYY-MM-DD
organized: false
organized_date: null
organized_to: []
---
```

## Proposed Update

```yaml
---
type: proposed-update
proposal_id: update-NNN
created: YYYY-MM-DD
target_file: knowledge/category/file.md
change_type: update|add|merge|archive
source_document: processed/source.md
confidence: high|medium|low
status: pending_review|approved|rejected|deferred
reviewed_date: null
reviewer_notes: ""
---
```
