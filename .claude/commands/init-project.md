---
description: Initialize a new project directory with the document organization structure
allowed-tools: Bash, Write, Read
argument-hint: <project-path>
---

# Initialize Project Structure

Create the standard directory structure for a new project.

## Arguments

The project path is required: `$ARGUMENTS`

If no path is provided, ask the user for the project directory path.

## Task

Create the following directory structure at the specified path:

```
<project>/
├── .env                    # Project configuration
├── raw/                    # Input files (drop zone)
├── to-process/             # After intake (renamed with metadata)
├── processed/              # After processing (analyzed)
├── extractions/            # Extracted info before organization
├── knowledge/              # Organized knowledge base
│   ├── meetings/           # Per-meeting structured notes
│   ├── project-status/     # Status updates, sprint summaries, decisions
│   ├── tasks/              # Action items, to-dos
│   ├── definitions/        # Glossary, terms, acronyms
│   ├── wiki/               # Reference articles, how-tos
│   ├── people/             # Team profiles, contacts
│   └── jira-drafts/        # Draft JIRA tickets to create
├── proposed-updates/       # Cross-reference change proposals
├── logs/                   # Processing logs
└── templates/              # Project-specific template overrides
```

## Steps

1. **Validate path**: Ensure the path is provided and is a valid directory location
2. **Check if exists**: If directory exists, check if it's empty or already initialized
3. **Create directories**: Create all required subdirectories
4. **Create .env file**: Copy from the framework's .env.example, updating PROJECT_NAME based on directory name
5. **Create README**: Add a simple README.md explaining the project structure
6. **Report success**: List what was created

## .env Template

Create `.env` with these defaults (derive PROJECT_NAME from the directory name):

```
PROJECT_NAME=<derived-from-path>
PROJECT_DESCRIPTION=""
USER_NAME=
USER_ALIASES=
DEFAULT_TIMEZONE=America/Los_Angeles
DEFAULT_SOURCE=notes
LOG_LEVEL=info
LOG_RETENTION_DAYS=30
KB_TASK_GROUPING=project
KB_AUTO_LINK=true
CROSSREF_THRESHOLD=0.7
CROSSREF_MAX_PROPOSALS=20
TRACK_PEOPLE=true
PEOPLE_INFERENCE=true
```

## README Template

Create `README.md` with:

```markdown
# <Project Name>

Project initialized with the Project Analysis & Organization Framework.

## Quick Start

1. Drop raw files (transcripts, notes, etc.) into `raw/`
2. Run `/run` to process all files through the pipeline
3. Or run individual stages: `/intake`, `/process`, `/organize`, `/crossref`
4. Check status with `/status`

## Directory Structure

- `raw/` - Drop input files here
- `to-process/` - Files after intake (renamed with metadata)
- `processed/` - Fully analyzed documents
- `extractions/` - Extracted information
- `knowledge/` - Organized knowledge base
  - `meetings/` - Per-meeting structured notes
  - `wiki/` - Reference articles, how-tos
  - `people/` - Team profiles
  - `tasks/` - Action items
  - `definitions/` - Glossary and terms
- `proposed-updates/` - Pending change proposals (review before applying)
- `logs/` - Processing logs

## Configuration

Edit `.env` to customize settings.
```

## Error Handling

- If path not provided: Ask for it
- If directory exists and is not empty: Warn and ask for confirmation
- If parent directory doesn't exist: Create it (with confirmation)
- On success: Show summary of created structure
