# Project Analysis & Organization Framework

This is a Claude Code framework for processing and organizing project-related documents (Zoom transcripts, Slack chats, JIRA tickets, Confluence docs, meeting notes, emails, etc.) into a structured knowledge base.

## Quick Start

1. Initialize a new project: `/init-project /path/to/your/project`
2. Drop raw files into `<project>/raw/`
3. Run the full pipeline: `/run`
4. Or run individual stages: `/intake`, `/process`, `/organize`, `/crossref`
5. Check status anytime: `/status`

## Pipeline Overview

```
raw/ ──/intake──> to-process/ ──/process──> processed/ + extractions/
                                                │
                                    ──/organize──> knowledge/
                                                │
                                    ──/crossref──> proposed-updates/
```

### Stage 1: Intake (`/intake`)
- Detects source type (Zoom, Slack, JIRA, Confluence, email, notes)
- Renames files to `YYYY-MM-DD-<source>-<short-description>.md`
- Adds metadata headers (participants, tags, dates)
- Moves to `to-process/`

### Stage 2: Process (`/process`)
- Generates summaries and identifies themes
- Extracts action items with assignees and deadlines
- Identifies people, terms, and definitions
- Creates extraction files in `extractions/`
- Moves originals to `processed/`

### Stage 3: Organize (`/organize`)
- Routes extractions to appropriate knowledge directories
- Updates task lists, definitions, wiki articles
- Generates draft JIRA tickets for new action items
- Builds people registry from context

### Stage 4: Cross-Reference (`/crossref`)
- Compares new information with existing knowledge
- Identifies contradictions and updates
- Generates proposed changes in `proposed-updates/`
- **Never auto-updates** - all changes require review

## Available Commands

### Pipeline Commands
| Command | Description |
|---------|-------------|
| `/init-project <path>` | Initialize a new project directory |
| `/convert-docx [file]` | Convert .docx files to markdown (auto-runs in intake) |
| `/intake [file]` | Process raw files (Stage 1) |
| `/process [file]` | Analyze documents (Stage 2) |
| `/organize [type]` | Organize extractions (Stage 3) |
| `/crossref [file]` | Cross-reference with knowledge base (Stage 4) |
| `/run` | Run full pipeline (all 4 stages) |
| `/status` | Show pipeline dashboard |
| `/review [id]` | Review and apply proposed updates |

### Search & Query Commands
| Command | Description |
|---------|-------------|
| `/search <query>` | Full-text search across knowledge base |
| `/ask <question>` | Natural language Q&A about the project |
| `/find <person>` | Person profile, tasks, discussions, decisions, blockers |

### Quick Capture Commands
| Command | Description |
|---------|-------------|
| `/note <text>` | Quick-add note/task/decision → creates file in raw/ |
| `/define <term> <definition>` | Quick-add definition → creates file in raw/ |

### Reporting Commands
| Command | Description |
|---------|-------------|
| `/weekly-digest [date]` | Generate summary of past week's activity |
| `/brief` | Generate project briefing for onboarding |

### Task Management Commands
| Command | Description |
|---------|-------------|
| `/my-tasks` | Show tasks assigned to you (from USER_NAME) |
| `/overdue` | List tasks past their deadline |
| `/blocked` | Show blocked tasks and blockers |

### Maintenance Commands
| Command | Description |
|---------|-------------|
| `/stale [days]` | Find KB entries not updated in N days |
| `/cleanup` | Archive old files, clean up logs |
| `/validate` | Check KB consistency (links, refs, frontmatter) |

### Export & Backup Commands
| Command | Description |
|---------|-------------|
| `/export [format]` | Export KB to html, pdf, obsidian, or markdown |
| `/backup` | Create timestamped backup of knowledge base |

## Project Structure

After running `/init-project`, your project will have:

```
<project>/
├── .env                    # Project configuration
├── raw/                    # Drop raw files here
├── to-process/             # After intake
├── processed/              # After processing
├── extractions/            # Extracted information
├── knowledge/              # Organized knowledge base
│   ├── project-status/     # Status updates, decisions
│   ├── tasks/              # Action items
│   ├── definitions/        # Glossary/terms
│   ├── wiki/               # Reference articles
│   ├── people/             # Team profiles
│   └── jira-drafts/        # Draft tickets to create
├── proposed-updates/       # Pending change proposals
├── logs/                   # Processing logs
└── templates/              # Custom templates (optional)
```

## Configuration

Edit the `.env` file in your project directory:

```bash
PROJECT_NAME=my-project
PROJECT_DESCRIPTION="Project description"
DEFAULT_TIMEZONE=America/Los_Angeles
LOG_LEVEL=info
KB_TASK_GROUPING=project    # project|epic|assignee
CROSSREF_THRESHOLD=0.7
TRACK_PEOPLE=true
```

## Input Formats

The framework accepts plain text files (.txt, .md) and automatically converts:
- **Microsoft Word (.docx)**: Auto-converted to markdown during intake (requires `python-docx`)

Supported content types (auto-detected from patterns):
- **Zoom transcripts**: Speaker labels, timestamps
- **Slack exports**: @mentions, #channels, threads
- **JIRA content**: Ticket IDs (PROJ-123), acceptance criteria
- **Confluence/wiki**: Wiki-style formatting
- **Email threads**: From/To/Subject headers
- **Meeting notes**: Agenda, attendees, action items
- **General notes**: Any text content

Source type is auto-detected from content patterns.

### Requirements for .docx Support

Install python-docx: `pip install python-docx`

The conversion preserves headings, bold/italic text, lists, and tables. Images and complex formatting are not preserved.

## Workflow Tips

1. **Batch processing**: Drop multiple files in `raw/`, then run `/run`
2. **Incremental processing**: Run individual stages as needed
3. **Review proposals**: Always review `proposed-updates/` before applying
4. **Custom templates**: Override templates in `<project>/templates/`
5. **People registry**: Names are learned from context over time

## Framework Development

This framework lives in `project-analysis-organization/` and consists of:
- **Slash Commands** (`.claude/commands/`): User entry points
- **Subagents** (`.claude/agents/`): Specialized analysis workers
- **Skills** (`.claude/skills/`): Auto-invoked patterns
- **Templates** (`templates/`): Output format templates
