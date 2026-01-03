---
description: Convert .docx files in raw/ to markdown format before processing
allowed-tools: Read, Write, Bash, Glob
argument-hint: [filename|all]
---

# Convert DOCX to Markdown

Convert Microsoft Word (.docx) files to markdown format so they can be processed by the intake pipeline.

## Arguments

`$ARGUMENTS` - Optional:
- Specific filename to convert (e.g., `document.docx`)
- `all` to convert all .docx files in raw/
- If empty, convert all .docx files

## Prerequisites

- `python-docx` library must be installed (`pip install python-docx`)
- Working directory should be the project directory (contains `raw/`, etc.)

## Task

### 1. Find .docx Files

Search for .docx files in the `raw/` directory:
- If a specific filename is provided, look for that file
- Otherwise, find all .docx files

### 2. Convert Each File

For each .docx file found:

1. Run the conversion script:
   ```bash
   python3 <framework-path>/scripts/docx_to_markdown.py "<input.docx>" "<output.md>"
   ```

2. Output file naming:
   - Same name as input, with `.md` extension
   - Place in `raw/` directory (same location)
   - Example: `raw/Architecture Overview.docx` → `raw/Architecture Overview.md`

3. Handle the original .docx file:
   - Keep the original .docx file (don't delete)
   - The intake process will skip .docx files

### 3. Report Results

```
DOCX Conversion Complete
========================

Converted: X files

Files:
- Architecture Overview.docx → Architecture Overview.md
- Customer Pipeline.docx → Customer Pipeline.md

Original .docx files retained in raw/

Next step: Run /intake or /run to process the markdown files
```

## Error Handling

- **No .docx files found**: Report "No .docx files found in raw/"
- **Conversion error**: Report the error and continue with other files
- **Missing python-docx**: Report installation instructions
- **File already exists**: Overwrite with warning

## Example Usage

```
/convert-docx                    # Convert all .docx files
/convert-docx all                # Same as above
/convert-docx "My Document.docx" # Convert specific file
```

## Notes

- The conversion preserves:
  - Headings (converted to # markdown headings)
  - Bold and italic text
  - Bulleted and numbered lists
  - Tables (converted to markdown tables)
  - Basic paragraph structure

- Not preserved:
  - Images (docx images are not extracted)
  - Complex formatting (colors, fonts, etc.)
  - Page layout features
  - Comments and track changes
