---
description: Quick-record a decision - creates file in raw/ for pipeline processing
allowed-tools: Write, Bash
argument-hint: <decision description> [--by=<person>] [--context=<context>]
---

# Quick Capture Decision

Quickly record a decision that will be processed through the pipeline.

## Arguments

`$ARGUMENTS` - Decision description with optional metadata:
- `--by=<name>` - Who made the decision
- `--context=<text>` - Why this decision was made

## Examples

```bash
/decision Use PostgreSQL instead of MySQL for the new service
/decision Delay launch by 2 weeks --by=Product Team
/decision Switch to OAuth2 for authentication --by=John --context=Better security and SSO support
```

## Task

### 1. Parse Arguments

Extract from `$ARGUMENTS`:
- **Decision**: Main text (everything except flags)
- **Decided by**: Text after `--by=`
- **Context/Rationale**: Text after `--context=`

### 2. Generate Filename

Format: `raw/YYYY-MM-DD-decision-<slug>.md`

Create slug from first few words of decision.

### 3. Create File

Write to `raw/`:

```markdown
---
source: manual-decision
created: YYYY-MM-DD HH:MM
type: decision
decided_by: <extracted or empty>
---

# Decision: <brief title>

## Decision

<full decision description>

## Date

YYYY-MM-DD

## Decided By

<name or "Not specified">

## Context/Rationale

<context if provided, or "To be documented">

## Impact

(To be analyzed during processing)

## Related

(To be identified during processing)
```

### 4. Confirm Creation

```
Decision recorded!

File: raw/2024-01-15-decision-use-postgresql-instead.md

Decision: Use PostgreSQL instead of MySQL for the new service
Decided by: Not specified
Date: 2024-01-15

To process into knowledge base:
  /intake    - Process this decision
  /run       - Run full pipeline

Once processed, find it in: knowledge/project-status/
```

## Examples with Output

### Simple Decision
```bash
/decision Use React for the new frontend
```
Creates:
```markdown
---
source: manual-decision
created: 2024-01-15 14:30
type: decision
---

# Decision: Use React for the new frontend

## Decision

Use React for the new frontend

## Date

2024-01-15

## Decided By

Not specified

## Context/Rationale

To be documented

## Impact

(To be analyzed during processing)

## Related

(To be identified during processing)
```

### Full Decision Record
```bash
/decision Migrate to Kubernetes --by=Platform Team --context=Need better scaling and deployment automation
```
Creates:
```markdown
---
source: manual-decision
created: 2024-01-15 14:30
type: decision
decided_by: Platform Team
---

# Decision: Migrate to Kubernetes

## Decision

Migrate to Kubernetes

## Date

2024-01-15

## Decided By

Platform Team

## Context/Rationale

Need better scaling and deployment automation

## Impact

(To be analyzed during processing)

## Related

(To be identified during processing)
```

## Processing Note

When this decision is processed through the pipeline:
1. It will be extracted and added to `knowledge/project-status/`
2. Cross-referencing may find related decisions or contradictions
3. Tasks may be created if action items are implied
