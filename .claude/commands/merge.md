---
description: Interactively merge duplicate or similar knowledge base entries
allowed-tools: Read, Write, Edit, Glob, Bash
argument-hint: <file1> <file2>
---

# Merge Entries

Merge two duplicate or similar knowledge base entries into one.

## Arguments

`$ARGUMENTS` - Two file paths to merge:
- `<file1>` - First file (will be the target)
- `<file2>` - Second file (will be merged into first, then archived)

## Examples

```bash
/merge knowledge/definitions/api.md knowledge/definitions/api-v1.md
/merge knowledge/people/john-smith.md knowledge/people/jsmith.md
```

## Task

### 1. Read Both Files

Load content from both files:
- Parse frontmatter
- Extract content sections
- Identify unique vs. overlapping content

### 2. Analyze Differences

```markdown
## Merge Analysis

**File 1:** knowledge/definitions/api.md
**File 2:** knowledge/definitions/api-v1.md

### Metadata Comparison

| Field | File 1 | File 2 |
|-------|--------|--------|
| Created | 2024-01-01 | 2023-11-15 |
| Updated | 2024-01-10 | 2023-12-01 |
| Sources | 3 files | 2 files |

### Content Comparison

**Identical Sections:**
- Definition (90% similar)

**Unique to File 1:**
- "Context in Project" section
- Related terms list

**Unique to File 2:**
- Version history
- Deprecation notes

### Recommendation

Merge File 2 into File 1:
- Keep File 1's definition (more recent)
- Add File 2's version history
- Combine sources lists
```

### 3. Generate Merged Content

```markdown
## Proposed Merged Content

---
type: definition
term: API
created: 2023-11-15
updated: 2024-01-15
sources:
  - [combined sources from both]
aliases:
  - API v1
  - REST API
---

# API

## Definition

[Best definition from both files]

## Context in Project

[From File 1]

## Version History

[From File 2]

## Related Terms

[Combined from both]

## Sources

[Combined, deduplicated]
---
```

### 4. Ask for Confirmation

```
Merge Summary
=============

Target: knowledge/definitions/api.md
Source: knowledge/definitions/api-v1.md

Changes:
+ Added version history section
+ Added "API v1" as alias
+ Combined 5 sources (2 duplicates removed)
+ Updated timestamp

After merge:
- File 1 will contain merged content
- File 2 will be moved to knowledge/archive/

Proceed with merge? (yes/no)
```

### 5. Execute Merge

If confirmed:
1. Write merged content to File 1
2. Create `knowledge/archive/` if needed
3. Move File 2 to `knowledge/archive/`
4. Update any references to File 2

### 6. Report Results

```
Merge Complete!

Updated: knowledge/definitions/api.md
Archived: knowledge/archive/api-v1.md

References updated:
- knowledge/wiki/api-guide.md (1 reference)
- processed/2024-01-05-zoom-api-discussion.md (1 reference)

To undo: Restore from knowledge/archive/api-v1.md
```

## Conflict Handling

If content conflicts:

```
Content Conflict Detected

## Definition Section

**File 1:**
> "An API is a set of protocols..."

**File 2:**
> "API stands for Application Programming Interface..."

Choose:
1. Keep File 1's version
2. Keep File 2's version
3. Combine both
4. Edit manually

Your choice (1/2/3/4):
```

## Dry Run Mode

Add `--dry-run` to see what would happen without making changes:

```bash
/merge file1.md file2.md --dry-run
```

## Auto-Detect Duplicates

Run without arguments to find potential duplicates:

```bash
/merge
```

Output:
```
Potential Duplicates Found

1. knowledge/definitions/api.md ↔ knowledge/definitions/api-v1.md
   Similarity: 85%

2. knowledge/people/john-smith.md ↔ knowledge/people/jsmith.md
   Similarity: 92%

3. knowledge/wiki/auth.md ↔ knowledge/wiki/authentication.md
   Similarity: 78%

To merge: /merge <file1> <file2>
```
