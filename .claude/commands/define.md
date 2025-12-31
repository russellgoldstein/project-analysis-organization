---
description: Quick-add a definition - creates file in raw/ for pipeline processing
allowed-tools: Write, Bash
argument-hint: <term> - <definition>
---

# Quick Capture Definition

Quickly add a term definition that will be processed through the pipeline.

## Arguments

`$ARGUMENTS` - Term and definition separated by ` - ` or `: `

## Examples

```bash
/define DAG - Directed Acyclic Graph, used for workflow orchestration
/define ETL: Extract, Transform, Load - a data processing pattern
/define Sprint - A fixed time period (usually 2 weeks) for completing work
```

## Task

### 1. Parse Arguments

Split `$ARGUMENTS` on ` - ` or `: ` to get:
- **Term**: The word or phrase being defined
- **Definition**: The explanation

If no separator found, treat the whole thing as a term and prompt for definition.

### 2. Generate Filename

Format: `raw/YYYY-MM-DD-definition-<term-slug>.md`

Term slug:
- Lowercase
- Replace spaces with hyphens
- Remove special characters

Example: "DAG" → `dag`, "API Gateway" → `api-gateway`

### 3. Create File

Write to `raw/`:

```markdown
---
source: manual-definition
created: YYYY-MM-DD HH:MM
type: definition
term: <term>
---

# <Term>

## Definition

<definition text>

## Context

(To be filled during processing)

## Related Terms

(To be identified during processing)
```

### 4. Confirm Creation

```
Definition captured!

File: raw/2024-01-15-definition-dag.md

Term: DAG
Definition: Directed Acyclic Graph, used for workflow orchestration

To process into knowledge base:
  /intake    - Process this definition
  /run       - Run full pipeline

Once processed, find it at: knowledge/definitions/dag.md
```

## Examples with Output

### Simple Definition
```bash
/define API - Application Programming Interface
```
Creates:
```markdown
---
source: manual-definition
created: 2024-01-15 14:30
type: definition
term: API
---

# API

## Definition

Application Programming Interface

## Context

(To be filled during processing)

## Related Terms

(To be identified during processing)
```

### Detailed Definition
```bash
/define Data Mesh - A decentralized data architecture where domain teams own their data as products, enabling self-service data access
```
Creates:
```markdown
---
source: manual-definition
created: 2024-01-15 14:30
type: definition
term: Data Mesh
---

# Data Mesh

## Definition

A decentralized data architecture where domain teams own their data as products, enabling self-service data access

## Context

(To be filled during processing)

## Related Terms

(To be identified during processing)
```

## Error Handling

- If no separator found: "Please use format: /define <term> - <definition>"
- If term is empty: "Please provide a term to define"
- If definition is empty: Prompt for definition
