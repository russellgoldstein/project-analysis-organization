---
description: Export knowledge base to HTML, PDF, or Obsidian-compatible format
allowed-tools: Glob, Read, Write, Bash
argument-hint: [format] [--output=<path>]
---

# Export Knowledge Base

Export the knowledge base to different formats for sharing or backup.

## Arguments

`$ARGUMENTS` - Optional:
- `<format>` - Export format: html, pdf, obsidian, markdown (default: markdown)
- `--output=<path>` - Output directory (default: exports/)
- `--include=<dirs>` - Only include specific directories
- `--exclude=<dirs>` - Exclude specific directories

## Examples

```bash
/export                           # Markdown to exports/
/export html                      # HTML website
/export pdf                       # Single PDF document
/export obsidian                  # Obsidian vault format
/export html --output=~/Desktop   # HTML to specific location
/export --include=wiki,definitions  # Only wiki and definitions
```

## Task

### 1. Gather Content

Collect all files from:
- `knowledge/` - All knowledge base entries
- Optionally: `processed/` - If specified

### 2. Export by Format

#### Markdown Export (default)

```
exports/
└── YYYY-MM-DD-export/
    ├── README.md              # Index/navigation
    ├── tasks/
    │   └── *.md
    ├── people/
    │   └── *.md
    ├── definitions/
    │   └── *.md
    ├── wiki/
    │   └── *.md
    ├── project-status/
    │   └── *.md
    └── jira-drafts/
        └── *.md
```

- Copy all markdown files
- Convert internal links to relative paths
- Generate index README.md

#### HTML Export

```
exports/
└── YYYY-MM-DD-html/
    ├── index.html             # Home page with navigation
    ├── css/
    │   └── style.css          # Styling
    ├── tasks/
    │   └── *.html
    ├── people/
    │   └── *.html
    ├── definitions/
    │   └── *.html
    ├── wiki/
    │   └── *.html
    └── project-status/
        └── *.html
```

Features:
- Convert markdown to HTML
- Apply consistent styling
- Generate navigation sidebar
- Convert internal links
- Searchable (with simple JS search)

#### PDF Export

```
exports/
└── YYYY-MM-DD-knowledge-base.pdf
```

Features:
- Single PDF document
- Table of contents
- Hyperlinked internal references
- Professional formatting
- Sections by category

#### Obsidian Export

```
exports/
└── YYYY-MM-DD-obsidian/
    ├── .obsidian/
    │   └── (minimal config)
    ├── Tasks/
    │   └── *.md
    ├── People/
    │   └── *.md
    ├── Definitions/
    │   └── *.md
    ├── Wiki/
    │   └── *.md
    ├── Project Status/
    │   └── *.md
    └── Index.md
```

Features:
- Compatible with Obsidian app
- `[[wiki-style]]` links preserved
- Tags converted to Obsidian format
- Graph view ready

### 3. Generate Index

Create navigation index:

```markdown
# Knowledge Base Export

**Exported:** January 15, 2024
**Source:** /path/to/project

## Contents

### [Tasks](tasks/index.md) (25 entries)
Active tasks, assignments, and work items.

### [People](people/index.md) (12 entries)
Team member profiles and contacts.

### [Definitions](definitions/index.md) (18 entries)
Glossary of terms and concepts.

### [Wiki](wiki/index.md) (8 entries)
Reference documentation and guides.

### [Project Status](project-status/index.md) (5 entries)
Status updates and decision logs.

---

*Exported with Project Analysis Framework*
```

### 4. Report Results

```
Export Complete!

Format: HTML
Location: exports/2024-01-15-html/
Files: 68

Contents:
- 25 tasks
- 12 people profiles
- 18 definitions
- 8 wiki articles
- 5 status updates

Open in browser:
  open exports/2024-01-15-html/index.html

To share:
  zip -r knowledge-base.zip exports/2024-01-15-html/
```

## Format Comparison

| Feature | Markdown | HTML | PDF | Obsidian |
|---------|----------|------|-----|----------|
| Editable | Yes | No | No | Yes |
| Searchable | Text | Yes | Yes | Yes |
| Offline | Yes | Yes | Yes | Yes |
| Printable | - | Yes | Yes | - |
| Interactive | No | Yes | No | Yes |
| Size | Small | Medium | Large | Small |

## Use Cases

- **Markdown:** Backup, version control, another project
- **HTML:** Share with stakeholders, host on internal wiki
- **PDF:** Print, email, formal documentation
- **Obsidian:** Personal knowledge management, graph exploration
