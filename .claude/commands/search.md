---
description: Full-text search across knowledge base, processed documents, and extractions
allowed-tools: Grep, Glob, Read
argument-hint: <query> [--type=tasks|people|definitions] [--since=YYYY-MM-DD]
---

# Search Knowledge Base

Search across all project knowledge for matching content.

## Arguments

`$ARGUMENTS` - Search query and optional filters:
- `<query>` - Text to search for (required)
- `--type=<type>` - Filter by content type: tasks, people, definitions, wiki, status
- `--since=<date>` - Only files modified since date (YYYY-MM-DD)
- `--in=<dir>` - Search only in specific directory: knowledge, processed, extractions

## Task

### 1. Parse Arguments

Extract:
- Search query (everything before flags)
- Type filter (if provided)
- Date filter (if provided)
- Directory filter (if provided)

### 2. Determine Search Paths

Based on filters, search in:

**Default (no filter):**
- `knowledge/` - All knowledge base entries
- `processed/` - Processed documents
- `extractions/` - Extraction files

**With --type filter:**
- `tasks` → `knowledge/tasks/`
- `people` → `knowledge/people/`
- `definitions` → `knowledge/definitions/`
- `wiki` → `knowledge/wiki/`
- `status` → `knowledge/project-status/`

**With --in filter:**
- Search only in specified directory

### 3. Execute Search

Use Grep to search for the query in markdown files:
- Case-insensitive search
- Include context (lines before/after match)
- Return file path, line number, and matching content

### 4. Filter by Date (if --since provided)

For each result, check file's `updated` or `created` frontmatter field.
Exclude files older than the specified date.

### 5. Format Results

```
Search Results for: "<query>"
=============================
Found X matches in Y files

## knowledge/tasks/project-alpha-tasks.md

Line 45:
> **Assignee:** John Smith
> **Description:** Implement <query> feature
              ~~~~~~

Line 78:
> The <query> system needs to be...
     ~~~~~~

---

## processed/2024-01-15-zoom-sprint.md

Line 123:
> We discussed the <query> and decided...
                   ~~~~~~

---

X total matches across Y files
```

### 6. No Results Handling

If no matches found:
```
No results found for "<query>"

Suggestions:
- Try broader search terms
- Check spelling
- Remove filters to search all content
- Use /ask for natural language queries
```

## Examples

```bash
# Basic search
/search authentication

# Search only in tasks
/search auth --type=tasks

# Search recent content
/search database --since=2024-01-01

# Search in processed documents only
/search sprint planning --in=processed

# Combined filters
/search API --type=definitions --since=2024-01-15
```

## Output Format Options

Results are displayed with:
- File path (clickable/relative)
- Line number
- Matching line with context
- Query highlighted in results
