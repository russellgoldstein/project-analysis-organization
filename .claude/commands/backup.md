---
description: Create timestamped backup of the entire knowledge base
allowed-tools: Glob, Read, Bash
argument-hint: [--compress] [--keep=<n>]
---

# Backup Knowledge Base

Create a complete backup of the knowledge base and project data.

## Arguments

`$ARGUMENTS` - Optional:
- `--compress` - Create compressed .tar.gz archive
- `--keep=<n>` - Keep only the last N backups (default: 5)
- `--include-raw` - Also backup raw/ and to-process/ directories
- `--dry-run` - Show what would be backed up without doing it

## Examples

```bash
/backup                       # Standard backup
/backup --compress            # Compressed archive
/backup --keep=3              # Keep only 3 most recent
/backup --include-raw         # Include unprocessed files
/backup --compress --keep=10  # Compressed, keep 10
```

## Task

### 1. Analyze Current State

Check what will be backed up:

```markdown
## Backup Analysis

**Date:** January 15, 2024, 14:30:00
**Backup ID:** 2024-01-15-143000

### Directories to Backup

| Directory | Files | Size |
|-----------|-------|------|
| knowledge/ | 78 | 890 KB |
| processed/ | 145 | 2.3 MB |
| extractions/ | 435 | 4.1 MB |
| proposed-updates/ | 3 | 12 KB |
| templates/ | 7 | 28 KB |
| .env | 1 | 1 KB |
| **Total** | **669** | **7.3 MB** |

### Existing Backups

| Backup | Date | Size |
|--------|------|------|
| 2024-01-14-093000 | Jan 14, 09:30 | 6.8 MB |
| 2024-01-10-160000 | Jan 10, 16:00 | 5.2 MB |
| 2024-01-05-110000 | Jan 5, 11:00 | 4.1 MB |

**Keep setting:** 5 (will retain all)
```

### 2. Create Backup Directory

```bash
mkdir -p backups/2024-01-15-143000
```

Structure:
```
backups/
└── 2024-01-15-143000/
    ├── knowledge/
    │   ├── tasks/
    │   ├── people/
    │   ├── definitions/
    │   ├── wiki/
    │   ├── project-status/
    │   └── jira-drafts/
    ├── processed/
    ├── extractions/
    ├── proposed-updates/
    ├── templates/
    ├── .env
    └── backup-manifest.md
```

### 3. Copy Files

Copy all relevant directories:
- `knowledge/` - The knowledge base
- `processed/` - Processed source documents
- `extractions/` - Extracted information
- `proposed-updates/` - Pending updates
- `templates/` - Project templates
- `.env` - Configuration

If `--include-raw`:
- `raw/` - Unprocessed input files
- `to-process/` - Files pending processing

### 4. Generate Manifest

Create `backup-manifest.md`:

```markdown
# Backup Manifest

**Backup ID:** 2024-01-15-143000
**Created:** January 15, 2024 at 14:30:00
**Source:** /path/to/project

## Contents

### Knowledge Base
- 25 tasks
- 12 people profiles
- 18 definitions
- 8 wiki articles
- 5 status updates
- 10 jira drafts

### Processed Documents
- 145 documents processed
- Date range: 2023-10-01 to 2024-01-15

### Extractions
- 435 extraction files

### Configuration
- .env backed up
- 7 templates

## File Counts

| Directory | Files |
|-----------|-------|
| knowledge/ | 78 |
| processed/ | 145 |
| extractions/ | 435 |
| proposed-updates/ | 3 |
| templates/ | 7 |
| Config files | 1 |
| **Total** | **669** |

## Restore Instructions

To restore this backup:

1. Stop any running processes
2. Copy backup contents to project root:
   ```bash
   cp -r backups/2024-01-15-143000/* /path/to/project/
   ```
3. Verify .env settings
4. Run /validate to check consistency

---

*Backup created with Project Analysis Framework*
```

### 5. Optional Compression

With `--compress`:

```bash
cd backups
tar -czf 2024-01-15-143000.tar.gz 2024-01-15-143000/
rm -rf 2024-01-15-143000/
```

Result:
```
backups/
└── 2024-01-15-143000.tar.gz  (2.1 MB compressed)
```

### 6. Cleanup Old Backups

With `--keep=5`:

```
Keeping last 5 backups...

Removed:
- 2023-12-01-090000 (45 days old)
- 2023-11-15-140000 (61 days old)

Kept:
- 2024-01-15-143000 (just created)
- 2024-01-14-093000 (1 day old)
- 2024-01-10-160000 (5 days old)
- 2024-01-05-110000 (10 days old)
- 2024-01-01-100000 (14 days old)
```

### 7. Report Results

```
Backup Complete!

Backup ID: 2024-01-15-143000
Location: backups/2024-01-15-143000/
Size: 7.3 MB

Contents:
- 78 knowledge base files
- 145 processed documents
- 435 extraction files
- 3 pending updates
- 7 templates
- 1 config file

Total files: 669

Manifest: backups/2024-01-15-143000/backup-manifest.md

To restore:
  cp -r backups/2024-01-15-143000/* .

Existing backups: 5
Next cleanup at: 6 backups
```

## Compressed Backup Report

```
Backup Complete!

Backup ID: 2024-01-15-143000
Location: backups/2024-01-15-143000.tar.gz
Original size: 7.3 MB
Compressed size: 2.1 MB (71% reduction)

To restore:
  cd backups && tar -xzf 2024-01-15-143000.tar.gz
  cp -r 2024-01-15-143000/* ..
```

## Dry Run Mode

With `--dry-run`:

```
Backup Dry Run (no changes made)
================================

Would create: backups/2024-01-15-143000/

Would backup:
- knowledge/ (78 files, 890 KB)
- processed/ (145 files, 2.3 MB)
- extractions/ (435 files, 4.1 MB)
- proposed-updates/ (3 files, 12 KB)
- templates/ (7 files, 28 KB)
- .env (1 KB)

Total: 669 files, 7.3 MB

Would remove (--keep=5):
- 2023-12-01-090000
- 2023-11-15-140000

Run without --dry-run to create backup.
```

## Restore Process

To restore from a backup:

```bash
# 1. Extract if compressed
cd backups
tar -xzf 2024-01-15-143000.tar.gz

# 2. Review manifest
cat 2024-01-15-143000/backup-manifest.md

# 3. Restore (overwrites current)
cp -r 2024-01-15-143000/knowledge/ ../
cp -r 2024-01-15-143000/processed/ ../
cp -r 2024-01-15-143000/extractions/ ../
cp 2024-01-15-143000/.env ../

# 4. Validate
/validate
```

## Scheduled Backup Suggestion

```
Tip: Create regular backups to protect your knowledge base.

Suggested schedule:
- Daily: /backup --compress --keep=7
- Weekly: /backup --compress --keep=4 (to weekly/ folder)
- Before major changes: /backup

Automate with cron:
0 2 * * * cd /path/to/project && claude /backup --compress --keep=7
```

## Backup Best Practices

1. **Before major operations:** Run `/backup` before `/cleanup` or bulk imports
2. **Regular schedule:** Daily or weekly backups
3. **Test restores:** Periodically verify backups work
4. **Off-site copies:** Copy compressed backups to cloud storage
5. **Version control:** Consider git for knowledge/ directory

