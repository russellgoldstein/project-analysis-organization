---
description: Archive old files and clean up logs to save space
allowed-tools: Glob, Read, Write, Bash
argument-hint: [--processed=<days>] [--logs=<days>] [--dry-run]
---

# Cleanup

Archive old processed files and clean up logs.

## Arguments

`$ARGUMENTS` - Optional:
- `--processed=<days>` - Archive processed files older than N days (default: 90)
- `--logs=<days>` - Delete logs older than N days (default: 30)
- `--extractions` - Also archive old extraction files
- `--dry-run` - Show what would be cleaned without doing it

## Examples

```bash
/cleanup                          # Default cleanup
/cleanup --dry-run                # Preview cleanup
/cleanup --processed=60           # Archive older than 60 days
/cleanup --logs=14                # Delete logs older than 14 days
/cleanup --processed=30 --logs=7  # Aggressive cleanup
```

## Task

### 1. Analyze Current State

```markdown
## Current Space Usage

| Directory | Files | Size |
|-----------|-------|------|
| processed/ | 145 | 2.3 MB |
| extractions/ | 435 | 4.1 MB |
| logs/ | 90 | 512 KB |
| knowledge/ | 78 | 890 KB |
| **Total** | **748** | **7.8 MB** |
```

### 2. Identify Files to Clean

**Processed files older than 90 days:**
- Count files by age bracket
- Identify which can be archived

**Log files older than 30 days:**
- Count log entries
- Identify for deletion

**Empty or orphaned files:**
- Extraction files with no content
- Files not referenced anywhere

### 3. Show Cleanup Plan

```markdown
## Cleanup Plan

**Processed Files (archive)**
- 45 files older than 90 days
- Will move to: archive/processed/
- Space to archive: 1.2 MB

**Extraction Files (archive)**
- 135 files older than 90 days
- Will move to: archive/extractions/
- Space to archive: 2.1 MB

**Log Files (delete)**
- 60 files older than 30 days
- Will delete permanently
- Space to free: 380 KB

**Empty Files (delete)**
- 3 empty extraction files
- Will delete permanently

---

Total space to archive: 3.3 MB
Total space to free: 380 KB

Proceed? (yes/no)
```

### 4. Execute Cleanup

If confirmed:

1. **Create archive directories:**
   ```
   archive/
   ├── processed/
   │   └── 2024-Q3/
   └── extractions/
       └── 2024-Q3/
   ```

2. **Move old processed files:**
   - Group by quarter for organization
   - Preserve directory structure

3. **Move old extractions:**
   - Match with processed files
   - Keep linkage intact

4. **Delete old logs:**
   - Remove log files older than threshold
   - Keep recent logs

5. **Delete empty files:**
   - Remove files with no content
   - Log what was deleted

### 5. Report Results

```
Cleanup Complete!

Archived:
- 45 processed files → archive/processed/2024-Q3/
- 135 extraction files → archive/extractions/2024-Q3/

Deleted:
- 60 log files (380 KB freed)
- 3 empty files

Space Summary:
- Before: 7.8 MB
- After: 4.1 MB
- Archived: 3.3 MB
- Freed: 380 KB

Archive location: archive/

To restore archived files, move them back from archive/
```

## Dry Run Mode

With `--dry-run`:

```
Cleanup Dry Run (no changes made)
=================================

Would archive:
- 45 files from processed/
- 135 files from extractions/

Would delete:
- 60 log files
- 3 empty files

Run without --dry-run to execute cleanup.
```

## Safety Features

1. **Never deletes knowledge base** - Only archives processed/extractions
2. **Preserves archive** - Old files are archived, not deleted
3. **Dry run first** - Always preview with --dry-run
4. **Logs actions** - Creates cleanup log for reference

## Scheduled Cleanup Suggestion

```
Tip: Run cleanup monthly to keep project tidy.

Suggested schedule:
- Weekly: /cleanup --logs=7 (just logs)
- Monthly: /cleanup (full cleanup)
- Quarterly: Review archive/, delete if not needed
```
