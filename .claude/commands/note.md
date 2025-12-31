---
description: Quick-add a note - creates file in raw/ for pipeline processing
allowed-tools: Write, Bash
argument-hint: <note text>
---

# Quick Capture Note

Quickly add a note that will be processed through the pipeline.

## Arguments

`$ARGUMENTS` - The note content

## Examples

```bash
/note Remember to follow up with John about the API changes
/note The deployment process needs documentation
/note Consider using Redis for caching instead of Memcached
```

## Task

### 1. Parse Note Content

The entire `$ARGUMENTS` is the note content.

### 2. Generate Filename

Format: `raw/YYYY-MM-DD-note-<slug>.md`

Create slug from first few words:
- Take first 5-6 words
- Lowercase
- Replace spaces with hyphens
- Remove special characters
- Max 50 characters

Example: "Remember to follow up with John" → `remember-to-follow-up-with`

### 3. Create File

Write to `raw/` with frontmatter:

```markdown
---
source: manual-note
created: YYYY-MM-DD HH:MM
type: note
---

# Note

<note content>
```

### 4. Confirm Creation

```
Note captured!

File: raw/2024-01-15-note-remember-to-follow-up-with.md

To process this note into the knowledge base:
  /intake    - Process just this file
  /run       - Run full pipeline

Preview:
---
source: manual-note
created: 2024-01-15 14:30
type: note
---

# Note

Remember to follow up with John about the API changes
```

## Multi-line Notes

For longer notes, the user can include newlines:

```bash
/note Meeting with stakeholders went well.
Key points:
- Budget approved
- Timeline extended by 2 weeks
- Need to hire contractor
```

This creates:

```markdown
---
source: manual-note
created: 2024-01-15 14:30
type: note
---

# Note

Meeting with stakeholders went well.
Key points:
- Budget approved
- Timeline extended by 2 weeks
- Need to hire contractor
```

## Error Handling

- If no content provided: "Please provide note content: /note <your note>"
- If raw/ doesn't exist: Create it
- If file already exists: Add numeric suffix
