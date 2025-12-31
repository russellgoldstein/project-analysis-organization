---
description: Check knowledge base consistency - broken links, missing sources, frontmatter issues
allowed-tools: Glob, Read, Grep
argument-hint: [--fix] [--type=<type>]
---

# Validate Knowledge Base

Check the knowledge base for consistency issues and problems.

## Arguments

`$ARGUMENTS` - Optional:
- `--fix` - Attempt to auto-fix simple issues
- `--type=<type>` - Only validate specific type: links, sources, frontmatter, orphans

## Examples

```bash
/validate                   # Full validation
/validate --fix             # Validate and fix what's possible
/validate --type=links      # Only check links
```

## Task

### 1. Check Internal Links

Find all `[[link]]` and `[text](path)` references:
- Verify target files exist
- Check for broken links
- Identify redirects needed

### 2. Check Source References

For each knowledge entry:
- Verify `sources` in frontmatter point to existing files
- Check that processed files still exist
- Identify orphaned references

### 3. Validate Frontmatter

Check all markdown files for:
- Required fields present (type, created, updated)
- Valid date formats
- Valid enum values (type, status, priority)
- Consistent field naming

### 4. Find Orphaned Files

Identify files that:
- Are not referenced by any other file
- Have no incoming links
- May be candidates for cleanup

### 5. Check Relationships

Verify relationship consistency:
- Person A "works with" B → B should "work with" A
- Task assigned to person → Person profile should exist
- Definition referenced → Definition file should exist

### 6. Generate Report

```markdown
# Knowledge Base Validation Report

**Date:** January 15, 2024
**Files Scanned:** 156
**Issues Found:** 12

---

## Summary

| Category | Issues | Severity |
|----------|--------|----------|
| Broken Links | 3 | High |
| Missing Sources | 2 | Medium |
| Frontmatter Issues | 5 | Low |
| Orphaned Files | 2 | Info |

**Overall Health:** ⚠️ Needs Attention

---

## 🔴 Broken Links (3)

### knowledge/wiki/api-guide.md:45
```markdown
See [[api-v2-spec]] for details
```
**Issue:** File `knowledge/definitions/api-v2-spec.md` not found
**Suggestion:** Create file or update link to `api-spec.md`

### knowledge/tasks/auth-tasks.md:23
```markdown
Assigned to [Bob Wilson](../people/bob-wilson.md)
```
**Issue:** File `knowledge/people/bob-wilson.md` not found
**Suggestion:** Create person profile or fix name

### knowledge/project-status/q1-status.md:67
```markdown
Source: [sprint-review](../../processed/2024-01-05-zoom-sprint.md)
```
**Issue:** File was archived or deleted
**Suggestion:** Update to archive path or remove reference

---

## 🟡 Missing Sources (2)

### knowledge/definitions/dag.md
- Lists source: `processed/2023-12-01-meeting.md`
- File not found (may be archived)
**Fix:** Update source path or remove

### knowledge/people/jane-doe.md
- No sources listed
- Cannot verify information origin
**Fix:** Add source references

---

## 🟢 Frontmatter Issues (5)

### knowledge/tasks/old-tasks.md
- Missing `updated` field
- **Fix:** Add `updated: 2024-01-15`

### knowledge/definitions/etl.md
- Invalid date format: `created: Jan 1, 2024`
- **Fix:** Change to `created: 2024-01-01`

### knowledge/people/alex-chen.md
- Unknown field: `title` (should be `role`)
- **Fix:** Rename field

### knowledge/wiki/deployment.md
- Missing `type` field
- **Fix:** Add `type: wiki`

### knowledge/tasks/api-tasks.md
- Invalid status: `status: WIP`
- **Fix:** Change to `status: in-progress`

---

## ℹ️ Orphaned Files (2)

### knowledge/definitions/legacy-api.md
- Not referenced anywhere
- Last updated: 6 months ago
- **Suggestion:** Archive or delete if obsolete

### knowledge/wiki/old-process.md
- Not referenced anywhere
- Last updated: 4 months ago
- **Suggestion:** Review relevance

---

## Relationship Inconsistencies

### Person-Task Mismatch
- Task "Review PR" assigned to "Bob" but no matching person profile
- **Fix:** Create bob.md or update task assignee

### Asymmetric Relationships
- john-smith.md: "works with Jane Doe"
- jane-doe.md: Does not mention John
- **Fix:** Add relationship to jane-doe.md

---

## Auto-Fix Available

These issues can be auto-fixed with `--fix`:
- 3 frontmatter issues (missing/invalid fields)
- 2 date format corrections

Run `/validate --fix` to apply these fixes.

---

## Recommendations

1. **Fix broken links** - These prevent navigation
2. **Update archived sources** - Point to archive location
3. **Review orphaned files** - May be outdated
4. **Run monthly** - Keep KB healthy

---

## Quick Commands

- Fix auto-fixable: /validate --fix
- Check only links: /validate --type=links
- Find stale content: /stale
- Cleanup old files: /cleanup
```

## Auto-Fix Mode

With `--fix`:

```
Auto-Fix Results
================

Fixed:
✓ Added missing 'updated' field to 3 files
✓ Corrected date format in 2 files
✓ Renamed 'title' to 'role' in 1 file

Cannot auto-fix (manual review needed):
✗ 3 broken links
✗ 2 missing source files
✗ 2 orphaned files

See full report above for manual fixes.
```
