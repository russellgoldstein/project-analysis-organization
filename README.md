# Project Analysis & Organization Framework

A Claude Code framework for processing and organizing project-related documents (Zoom transcripts, Slack conversations, JIRA tickets, meeting notes, emails, etc.) into a structured, searchable knowledge base.

## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Pipeline Stages](#pipeline-stages)
- [Commands Reference](#commands-reference)
- [Directory Structure](#directory-structure)
- [File Flows](#file-flows)
- [Configuration](#configuration)
- [Examples](#examples)
- [Components](#components)

---

## Overview

This framework provides a 4-stage pipeline that transforms raw project documents into organized, cross-referenced knowledge:

```
┌─────────┐    ┌─────────────┐    ┌───────────┐    ┌───────────┐    ┌──────────┐
│  raw/   │───▶│ to-process/ │───▶│ processed/│───▶│ knowledge/│───▶│ proposed │
│         │    │             │    │           │    │           │    │ updates/ │
└─────────┘    └─────────────┘    └───────────┘    └───────────┘    └──────────┘
     │              │                   │                │                │
     │              │                   │                │                │
  /intake        /process           /organize        /crossref        /review
   Stage 1        Stage 2            Stage 3          Stage 4         Apply
```

**Key Features:**
- Auto-detects document source type (Zoom, Slack, JIRA, email, etc.)
- Extracts tasks, people, definitions, and project status
- Builds a people registry from context over time
- Generates draft JIRA tickets from action items
- Cross-references new info with existing knowledge
- Proposes updates for human review (never auto-updates)

---

## Quick Start

### 1. Initialize a Project

```bash
# In Claude Code, run:
/init-project /path/to/my-project
```

This creates:
```
my-project/
├── .env                    # Configuration
├── raw/                    # Drop files here
├── to-process/
├── processed/
├── extractions/
├── knowledge/
│   ├── project-status/
│   ├── tasks/
│   ├── definitions/
│   ├── wiki/
│   ├── people/
│   └── jira-drafts/
├── proposed-updates/
├── logs/
└── templates/
```

### 2. Add Raw Files

Drop your files into `raw/`:
```
my-project/raw/
├── zoom-transcript.txt
├── slack-export.txt
└── meeting-notes.md
```

### 3. Run the Pipeline

```bash
# Run full pipeline
/run

# Or run stages individually
/intake
/process
/organize
/crossref
```

### 4. Review Proposed Updates

```bash
/review
```

---

## Pipeline Stages

### Stage 1: Intake (`/intake`)

**Purpose:** Prepare raw files for processing

**Input:** Files in `raw/`
**Output:** Renamed files with metadata in `to-process/`

**What happens:**
1. Reads each file in `raw/`
2. Auto-detects source type (Zoom, Slack, JIRA, email, meeting, notes)
3. Extracts or infers document date
4. Generates descriptive filename
5. Adds YAML frontmatter with metadata
6. Moves to `to-process/`

**Example transformation:**

```
raw/zoom-call-jan15.txt
         │
         ▼
to-process/2024-01-15-zoom-sprint-planning.md
```

**Frontmatter added:**
```yaml
---
source: zoom
original_filename: zoom-call-jan15.txt
intake_date: 2024-01-15
document_date: 2024-01-15
status: pending
participants:
  - John Smith
  - Jane Doe
tags: []
source_confidence: high
---
```

---

### Stage 2: Process (`/process`)

**Purpose:** Analyze documents and extract structured information

**Input:** Files in `to-process/`
**Output:**
- Updated files moved to `processed/`
- Extraction files in `extractions/`

**What happens:**
1. Loads document from `to-process/`
2. Runs specialized subagents:
   - `document-analyzer` → Summary, key points, decisions, themes
   - `task-extractor` → Action items with assignees, deadlines, priorities
   - `entity-extractor` → People, projects, terms, definitions
3. Creates extraction files
4. Updates document metadata
5. Moves to `processed/`

**Files created:**

```
extractions/
├── 2024-01-15-zoom-sprint-planning-summary.md
├── 2024-01-15-zoom-sprint-planning-tasks.md
└── 2024-01-15-zoom-sprint-planning-entities.md
```

**Summary extraction example:**
```markdown
---
type: extraction
extraction_type: summary
source_document: to-process/2024-01-15-zoom-sprint-planning.md
extracted_date: 2024-01-15
---

# Summary: Sprint Planning Meeting

## Executive Summary
The team reviewed Q1 goals and planned the upcoming sprint focused on authentication features.

## Key Points
- Authentication epic is top priority
- John taking lead on OAuth implementation
- Target launch date: end of month

## Decisions Made
- Using OAuth2 instead of custom auth
- Mobile app auth deferred to next sprint
```

**Tasks extraction example:**
```markdown
---
type: extraction
extraction_type: tasks
source_document: to-process/2024-01-15-zoom-sprint-planning.md
extracted_date: 2024-01-15
task_count: 3
---

# Tasks: Sprint Planning Meeting

## Task Summary
| Assignee | Count | High Priority |
|----------|-------|---------------|
| John Smith | 2 | 1 |
| Jane Doe | 1 | 0 |

## Tasks

### Task: Implement OAuth2 authentication
| Field | Value |
|-------|-------|
| Assignee | John Smith |
| Deadline | 2024-01-25 |
| Priority | High |
| Status | Pending |

**Description:** Implement OAuth2 flow with Google and GitHub providers

**Source Quote:**
> "John, can you take the OAuth implementation? We need it by end of next week."
```

---

### Stage 3: Organize (`/organize`)

**Purpose:** Route extracted information to the knowledge base

**Input:** Files in `extractions/`
**Output:** Organized entries in `knowledge/`

**What happens:**
1. Reads extraction files
2. Categorizes content using taxonomy rules:
   - Tasks → `knowledge/tasks/`
   - People → `knowledge/people/`
   - Definitions → `knowledge/definitions/`
   - Status/Decisions → `knowledge/project-status/`
   - Reference content → `knowledge/wiki/`
   - JIRA candidates → `knowledge/jira-drafts/`
3. Creates or updates knowledge base entries
4. Marks extractions as organized

**Knowledge base structure after organizing:**

```
knowledge/
├── tasks/
│   └── auth-epic-tasks.md           # Grouped tasks
├── people/
│   ├── john-smith.md                # Person profile
│   └── jane-doe.md
├── definitions/
│   ├── oauth2.md                    # Term definition
│   └── jwt.md
├── project-status/
│   └── auth-project-status.md       # Project status
├── wiki/
│   └── authentication-architecture.md
└── jira-drafts/
    └── draft-implement-oauth.md     # Ready to create in JIRA
```

**Person profile example (`knowledge/people/john-smith.md`):**
```markdown
---
type: person
created: 2024-01-15
updated: 2024-01-15
sources:
  - processed/2024-01-15-zoom-sprint-planning.md
---

# John Smith

## Basic Info
| Field | Value |
|-------|-------|
| Role | Senior Engineer |
| Team | Platform Team |
| Expertise | Backend, Auth |

## Document Mentions
| Date | Document | Context |
|------|----------|---------|
| 2024-01-15 | sprint-planning.md | Assigned OAuth implementation |
```

**JIRA draft example (`knowledge/jira-drafts/draft-implement-oauth.md`):**
```markdown
---
type: jira-draft
created: 2024-01-15
source_document: processed/2024-01-15-zoom-sprint-planning.md
suggested_project: AUTH
suggested_type: Story
priority: High
---

# [Draft] Implement OAuth2 Authentication

## Summary
> Implement OAuth2 authentication with Google and GitHub providers

## Acceptance Criteria
- [ ] User can log in with Google
- [ ] User can log in with GitHub
- [ ] Sessions persist across browser refresh
- [ ] Logout invalidates session

## Source Context
> "John, can you take the OAuth implementation? We need it by end of next week."
> — Sprint Planning, January 15, 2024
```

---

### Stage 4: Cross-Reference (`/crossref`)

**Purpose:** Find updates, contradictions, and relationships

**Input:** Recently processed documents + existing knowledge base
**Output:** Proposed updates in `proposed-updates/`

**What happens:**
1. Loads recent documents
2. Scans knowledge base for related content
3. Uses `crossref-analyzer` to find:
   - Contradictions (conflicting information)
   - Updates needed (new info about existing topics)
   - Relationships (connections between documents)
   - Duplicates (redundant entries)
4. Generates proposals for each finding
5. **Never auto-applies changes**

**Proposal example (`proposed-updates/update-001-task-status.md`):**
```markdown
---
type: proposed-update
proposal_id: update-001
created: 2024-01-20
target_file: knowledge/tasks/auth-epic-tasks.md
change_type: update
source_document: processed/2024-01-20-zoom-standup.md
confidence: high
status: pending_review
---

# Proposed Update: Task Status Change

## Target
**File:** knowledge/tasks/auth-epic-tasks.md
**Section:** Task "Implement OAuth2 authentication"

## Current Content
```markdown
| Status | In Progress |
```

## Proposed Content
```markdown
| Status | Done |
| Completed | 2024-01-20 |
```

## Rationale
John confirmed OAuth implementation is complete and merged.

## Source Evidence
**Document:** processed/2024-01-20-zoom-standup.md
> "OAuth is done, merged it yesterday. Ready for QA."
> — John Smith

## Review Actions
- [ ] Approve and apply
- [ ] Modify and apply
- [ ] Reject
- [ ] Defer
```

---

### Review & Apply (`/review`)

**Purpose:** Review proposed updates and apply approved changes

**Input:** Files in `proposed-updates/`
**Output:** Applied changes to `knowledge/`, archived proposals

**Commands:**
```bash
/review                  # Interactive review of all proposals
/review update-001       # Review specific proposal
/review --list           # List pending proposals
/review --apply-high     # Auto-apply high-confidence proposals
```

**Interactive flow:**
1. Shows proposal diff (current vs proposed)
2. Shows rationale and source evidence
3. Asks for decision:
   - **(a) Approve** - Apply change, archive proposal
   - **(m) Modify** - Edit before applying
   - **(r) Reject** - Don't apply, archive with reason
   - **(d) Defer** - Keep pending for later
4. Applies approved changes
5. Moves processed proposals to `proposed-updates/archive/`

---

## Commands Reference

### Pipeline Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/init-project <path>` | Initialize project directory | `/init-project ~/projects/data-lake` |
| `/intake [file\|all]` | Process raw files (Stage 1) | `/intake` or `/intake meeting.txt` |
| `/process [file\|all]` | Analyze documents (Stage 2) | `/process` |
| `/organize [type]` | Organize to knowledge base (Stage 3) | `/organize tasks` |
| `/crossref [file\|all]` | Cross-reference (Stage 4) | `/crossref` |
| `/run [flags]` | Run full pipeline | `/run` or `/run --skip-crossref` |
| `/review [id\|flags]` | Review proposed updates | `/review` or `/review update-001` |
| `/status` | Show pipeline dashboard | `/status` |

### Search & Query Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/search <query>` | Full-text search across KB | `/search authentication` |
| `/ask <question>` | Natural language Q&A | `/ask Who is working on auth?` |
| `/find <person>` | Person profile, tasks, discussions, decisions | `/find John Smith` |

### Quick Capture Commands

These create files in `raw/` to go through the full pipeline.

| Command | Description | Example |
|---------|-------------|---------|
| `/note <text>` | Quick capture note/task/decision | `/note Review PR #123 by Friday` |
| `/define <term> <def>` | Quick add a definition | `/define ETL Extract Transform Load` |

### Reporting Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/weekly-digest [date]` | Generate weekly summary | `/weekly-digest` or `/weekly-digest 2024-01-15` |
| `/brief` | Generate project briefing | `/brief` |

### Task Management Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/my-tasks` | Show your assigned tasks | `/my-tasks` |
| `/overdue` | List overdue tasks | `/overdue` |
| `/blocked` | Show blocked tasks | `/blocked` |

### Maintenance Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/stale [days]` | Find stale entries | `/stale 30` |
| `/cleanup` | Archive old files | `/cleanup --dry-run` |
| `/validate` | Check KB consistency | `/validate --fix` |

### Export & Backup Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/export [format]` | Export KB | `/export html` or `/export pdf` |
| `/backup` | Create timestamped backup | `/backup --compress` |

### Command Flags

**`/run` Flags:**
- `--skip-crossref` - Run stages 1-3 only
- `--dry-run` - Show what would happen without changes

**`/review` Options:**
- `--list` - List pending proposals
- `--apply-high` - Auto-apply high-confidence proposals
- `--archive-rejected` - Archive all rejected proposals

**`/cleanup` Options:**
- `--processed=<days>` - Archive files older than N days (default: 90)
- `--logs=<days>` - Delete logs older than N days (default: 30)
- `--dry-run` - Preview without changes

**`/export` Formats:**
- `markdown` - Plain markdown (default)
- `html` - Static website with navigation
- `pdf` - Single PDF document
- `obsidian` - Obsidian-compatible vault

**`/backup` Options:**
- `--compress` - Create .tar.gz archive
- `--keep=<n>` - Keep only last N backups (default: 5)

---

## Directory Structure

### Framework Directory

```
project-analysis-organization/     # This framework
├── CLAUDE.md                      # Framework instructions
├── README.md                      # This file
├── .env.example                   # Config template
├── .claude/
│   ├── commands/                  # Slash commands
│   │   ├── init-project.md
│   │   ├── intake.md
│   │   ├── process.md
│   │   ├── organize.md
│   │   ├── crossref.md
│   │   ├── run.md
│   │   ├── review.md
│   │   └── status.md
│   ├── agents/                    # Subagents
│   │   ├── document-analyzer.md
│   │   ├── task-extractor.md
│   │   ├── entity-extractor.md
│   │   └── crossref-analyzer.md
│   └── skills/                    # Auto-invoked skills
│       ├── source-detection/
│       ├── document-formatting/
│       ├── knowledge-taxonomy/
│       └── people-registry/
└── templates/                     # Default templates
    ├── document-metadata.md
    ├── task-entry.md
    ├── definition-entry.md
    ├── person-profile.md
    ├── project-status.md
    ├── proposed-update.md
    └── jira-draft.md
```

### Project Directory (created by `/init-project`)

```
my-project/
├── .env                           # Project configuration
│
├── raw/                           # INPUT: Drop files here
│   └── *.txt, *.md                # Unprocessed documents
│
├── to-process/                    # After Stage 1
│   └── YYYY-MM-DD-source-desc.md  # Renamed with metadata
│
├── processed/                     # After Stage 2
│   └── YYYY-MM-DD-source-desc.md  # Analyzed documents
│
├── extractions/                   # Stage 2 output
│   ├── *-summary.md               # Document summaries
│   ├── *-tasks.md                 # Extracted tasks
│   └── *-entities.md              # People, terms, definitions
│
├── knowledge/                     # After Stage 3
│   ├── project-status/            # Status updates, decisions
│   │   └── project-name-status.md
│   ├── tasks/                     # Action items
│   │   └── project-name-tasks.md
│   ├── definitions/               # Glossary
│   │   └── term-name.md
│   ├── wiki/                      # Reference articles
│   │   └── topic-name.md
│   ├── people/                    # Team profiles
│   │   └── firstname-lastname.md
│   └── jira-drafts/               # Draft tickets
│       └── draft-title.md
│
├── proposed-updates/              # After Stage 4
│   ├── update-001-description.md  # Pending proposals
│   └── archive/                   # Processed proposals
│
├── logs/                          # Processing logs
│   ├── intake-YYYY-MM-DD.md
│   ├── process-YYYY-MM-DD.md
│   ├── organize-YYYY-MM-DD.md
│   ├── crossref-YYYY-MM-DD.md
│   └── review-YYYY-MM-DD.md
│
└── templates/                     # Project-specific overrides
```

---

## File Flows

### Complete Pipeline Flow

```
                                    STAGE 1: INTAKE
                                    ───────────────
raw/meeting-notes.txt ─────────────────────────────────────────────────────────┐
    │                                                                          │
    │  • Detect source type (zoom/slack/jira/email/meeting/notes)             │
    │  • Extract date from content or filename                                 │
    │  • Generate new filename: YYYY-MM-DD-source-description.md              │
    │  • Add YAML frontmatter with metadata                                    │
    │                                                                          │
    ▼                                                                          │
to-process/2024-01-15-meeting-sprint-planning.md ◄─────────────────────────────┘
    │
    │                               STAGE 2: PROCESS
    │                               ────────────────
    │  • document-analyzer → Summary, themes, decisions
    │  • task-extractor → Action items with assignees
    │  • entity-extractor → People, terms, definitions
    │
    ├──────────────────────────────────────────────────────────────────────────┐
    │                                                                          │
    ▼                                                                          ▼
processed/2024-01-15-meeting-sprint-planning.md    extractions/
    │                                               ├── ...-summary.md
    │                                               ├── ...-tasks.md
    │                                               └── ...-entities.md
    │                                                          │
    │                               STAGE 3: ORGANIZE          │
    │                               ─────────────────          │
    │                                                          │
    │  • Route tasks → knowledge/tasks/                        │
    │  • Route people → knowledge/people/                      │
    │  • Route terms → knowledge/definitions/                  │
    │  • Route status → knowledge/project-status/              │
    │  • Create JIRA drafts → knowledge/jira-drafts/           │
    │                                                          │
    │                                                          ▼
    │                                              knowledge/
    │                                               ├── tasks/project-tasks.md
    │                                               ├── people/john-smith.md
    │                                               ├── definitions/oauth2.md
    │                                               ├── project-status/project.md
    │                                               └── jira-drafts/draft-auth.md
    │                                                          │
    │                               STAGE 4: CROSSREF          │
    │                               ─────────────────          │
    │                                                          │
    └───────────────────────────────┬──────────────────────────┘
                                    │
                                    │  • Compare new docs to knowledge base
                                    │  • Find contradictions and updates
                                    │  • Discover relationships
                                    │  • Generate proposals (never auto-apply)
                                    │
                                    ▼
                        proposed-updates/
                         └── update-001-task-status.md
                                    │
                                    │              REVIEW & APPLY
                                    │              ──────────────
                                    │
                                    │  • /review shows each proposal
                                    │  • User approves/modifies/rejects
                                    │  • Approved changes applied to knowledge/
                                    │  • Proposals archived
                                    │
                                    ▼
                        proposed-updates/archive/
                         └── update-001-task-status.md (applied)
```

### Document Lifecycle

```
┌────────────────────────────────────────────────────────────────────────────┐
│                           DOCUMENT LIFECYCLE                                │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  1. RAW INPUT                                                              │
│     └── raw/zoom-call.txt                                                  │
│         Status: Unprocessed                                                │
│                                                                            │
│  2. AFTER INTAKE                                                           │
│     └── to-process/2024-01-15-zoom-sprint-planning.md                     │
│         Status: pending                                                    │
│         Frontmatter: source, date, participants                           │
│                                                                            │
│  3. AFTER PROCESSING                                                       │
│     ├── processed/2024-01-15-zoom-sprint-planning.md                      │
│     │   Status: processed                                                  │
│     │   Frontmatter: + extracted counts, tags                             │
│     │                                                                      │
│     └── extractions/                                                       │
│         ├── 2024-01-15-zoom-sprint-planning-summary.md                    │
│         ├── 2024-01-15-zoom-sprint-planning-tasks.md                      │
│         └── 2024-01-15-zoom-sprint-planning-entities.md                   │
│                                                                            │
│  4. AFTER ORGANIZING                                                       │
│     └── knowledge/                                                         │
│         ├── tasks/auth-epic-tasks.md (tasks added)                        │
│         ├── people/john-smith.md (profile created/updated)                │
│         └── definitions/oauth2.md (term added)                            │
│                                                                            │
│  5. AFTER CROSSREF                                                         │
│     └── proposed-updates/update-001-task-status.md                        │
│         Status: pending_review                                             │
│                                                                            │
│  6. AFTER REVIEW                                                           │
│     ├── knowledge/tasks/auth-epic-tasks.md (updated)                      │
│     └── proposed-updates/archive/update-001-task-status.md                │
│         Status: approved                                                   │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## Configuration

### `.env` File

```bash
# Project Settings
PROJECT_NAME=my-project
PROJECT_DESCRIPTION="Description of the project"
USER_NAME=Your Name
USER_ALIASES=nickname,shortname

# Processing
DEFAULT_TIMEZONE=America/Los_Angeles
DEFAULT_SOURCE=notes
LOG_LEVEL=info

# Knowledge Base
KB_TASK_GROUPING=project    # project|epic|assignee
KB_AUTO_LINK=true

# Cross-Reference
CROSSREF_THRESHOLD=0.7
CROSSREF_MAX_PROPOSALS=20

# People Tracking
TRACK_PEOPLE=true
PEOPLE_INFERENCE=true
```

---

## Examples

### Example 1: Process a Zoom Transcript

**Input:** `raw/team-sync-call.txt`
```
WEBVTT

00:00:15.000 --> 00:00:20.000
John Smith: Good morning everyone. Let's start with updates.

00:00:21.000 --> 00:00:35.000
Jane Doe: I finished the API documentation yesterday. Ready for review.

00:00:36.000 --> 00:00:45.000
John Smith: Great! Bob, can you review it by Friday?

00:00:46.000 --> 00:00:50.000
Bob Wilson: Sure, I'll have comments by end of day Friday.
```

**Run:**
```bash
/run
```

**Results:**

1. **Intake creates:** `to-process/2024-01-15-zoom-team-sync.md`
2. **Process extracts:**
   - 1 task: "Review API documentation" (Bob Wilson, due Friday)
   - 3 people: John Smith, Jane Doe, Bob Wilson
3. **Organize creates:**
   - `knowledge/tasks/team-tasks.md` with the review task
   - `knowledge/people/john-smith.md`, `jane-doe.md`, `bob-wilson.md`

---

### Example 2: Process Slack Export

**Input:** `raw/slack-discussion.txt`
```
#data-pipeline
Monday, January 15th

@john.smith 10:30 AM
The ETL job failed again last night. Looking into it.

@jane.doe 10:32 AM
Is it the same issue as last week? The memory problem?

@john.smith 10:35 AM
Different issue. Looks like the source API changed their response format.
I'll need to update our parser. Should have a fix by EOD.

@jane.doe 10:36 AM
:+1: Let me know if you need help testing
```

**Results:**

1. **Detected as:** Slack (confidence: high)
2. **Task extracted:** "Update parser for new API format" (John, EOD deadline)
3. **Definition candidate:** "ETL" if not already in glossary
4. **Project status:** Pipeline issue being addressed

---

### Example 3: Weekly Workflow

```bash
# Monday: Drop weekend meeting notes
cp ~/Downloads/zoom-*.txt ~/projects/data-lake/raw/

# Process everything
/run

# Review what was found
/status

# Review and apply updates
/review

# Check specific person's tasks
cat ~/projects/data-lake/knowledge/people/john-smith.md

# Create JIRA tickets from drafts
cat ~/projects/data-lake/knowledge/jira-drafts/
```

---

## Components

### Subagents

| Agent | Purpose | Model |
|-------|---------|-------|
| `document-analyzer` | Summarization, themes, decisions | sonnet |
| `task-extractor` | Action items, deadlines, assignees | sonnet |
| `entity-extractor` | People, projects, terms, definitions | sonnet |
| `crossref-analyzer` | Contradictions, updates, relationships | opus |

### Skills (Auto-Invoked)

| Skill | Purpose |
|-------|---------|
| `source-detection` | Detect document type from content patterns |
| `document-formatting` | Standard markdown and metadata formatting |
| `knowledge-taxonomy` | Categorization rules for knowledge base |
| `people-registry` | Person identification and profile management |

### Source Detection

The framework auto-detects these source types:

| Source | Detection Patterns |
|--------|-------------------|
| `zoom` | WEBVTT, HH:MM:SS timestamps, speaker labels |
| `slack` | #channels, @mentions, thread indicators, :emoji: |
| `jira` | PROJ-1234 IDs, Acceptance Criteria, Status fields |
| `confluence` | Wiki formatting, Page/Space references |
| `email` | From/To/Subject headers, Re:/Fwd: prefixes |
| `meeting` | Agenda, Attendees, Action Items sections |
| `notes` | Default for unstructured content |

---

## Tips

1. **Consistent file drops:** Establish a routine for dropping files into `raw/`
2. **Regular reviews:** Run `/review` frequently to keep knowledge base current
3. **JIRA drafts:** Check `knowledge/jira-drafts/` weekly for tickets to create
4. **People registry:** The more documents processed, the better person profiles become
5. **Custom templates:** Override templates in project's `templates/` directory
6. **Bulk import:** Use `/run --skip-crossref` for initial large imports, then `/crossref` after

---

## License

MIT License - Use freely for personal and commercial projects.
