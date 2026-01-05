# Wiki Article Template

Use this template when creating wiki articles in `knowledge/wiki/`.

## Wiki Article Categories

Wiki articles are organized into three categories:

| Category | Slug | Use For |
|----------|------|---------|
| **Technical Implementation** | `technical` | Architecture, APIs, data models, system design |
| **Best Practices & Patterns** | `best-practices` | Standards, procedures, guidelines, patterns |
| **Product & Business Context** | `product-business` | Requirements, business rules, domain knowledge |

## Wiki Article File

File location: `knowledge/wiki/<topic-slug>.md` (lowercase, hyphenated)

```markdown
---
type: wiki
topic: Topic Name
category: technical | best-practices | product-business
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources:
  - processed/source1.md
  - processed/source2.md
related:
  - wiki/related-topic-1.md
  - wiki/related-topic-2.md
tags:
  - tag1
  - tag2
---

# Topic Name

## Overview

A 2-3 sentence overview explaining what this article covers and why it's important. Provide enough context for someone unfamiliar with the topic to understand its relevance.

## Details

### Section 1: Subtitle

Detailed content for the first major section. Include:
- Explanations of concepts
- Technical specifications
- Process steps
- Business rules

### Section 2: Subtitle

Detailed content for the second section.

### Section 3: Subtitle

Additional sections as needed.

## Examples

Practical examples demonstrating the concepts (if applicable):

### Example 1: Title

```
Code or configuration example
```

Explanation of the example.

### Example 2: Title

Description of a real-world scenario.

## Related Topics

Links to related wiki articles:

- [Related Article 1](related-topic-1.md) - Brief description of relationship
- [Related Article 2](related-topic-2.md) - Brief description of relationship

## Sources

Documents that informed this article:

- [Source Document 1](../processed/source1.md) - What information came from this source
- [Source Document 2](../processed/source2.md) - What information came from this source

## History

| Date | Change | Source |
|------|--------|--------|
| YYYY-MM-DD | Initial creation | source.md |
| YYYY-MM-DD | Added section on X | source2.md |
| YYYY-MM-DD | Updated based on Y | source3.md |
```

## Category-Specific Templates

### Technical Implementation Article

```markdown
---
type: wiki
topic: Data Pipeline Architecture
category: technical
created: 2024-01-15
updated: 2024-01-15
sources:
  - processed/2024-01-15-zoom-architecture-review.md
tags:
  - architecture
  - data-pipeline
  - spark
---

# Data Pipeline Architecture

## Overview

Overview of the data pipeline architecture and its role in the system.

## Architecture

### High-Level Design

Description of the overall architecture.

```
[Component Diagram or ASCII art]
```

### Components

| Component | Purpose | Technology |
|-----------|---------|------------|
| Ingestion | Data collection | Kafka |
| Processing | Transformation | Spark |
| Storage | Persistence | S3/Iceberg |

### Data Flow

1. Step 1: Description
2. Step 2: Description
3. Step 3: Description

## Technical Details

### Configuration

Key configuration settings and their purposes.

### Dependencies

External systems and services this depends on.

### Performance Considerations

Performance characteristics and optimization notes.

## Sources

- [Architecture Review](../processed/2024-01-15-zoom-architecture-review.md)
```

### Best Practices Article

```markdown
---
type: wiki
topic: Code Review Process
category: best-practices
created: 2024-01-15
updated: 2024-01-15
sources:
  - processed/2024-01-10-notes-engineering-standards.md
tags:
  - code-review
  - process
  - quality
---

# Code Review Process

## Overview

Standards and procedures for conducting code reviews.

## Process

### Before Review

Checklist for PR authors:

- [ ] Item 1
- [ ] Item 2
- [ ] Item 3

### During Review

Guidelines for reviewers:

1. Step 1
2. Step 2
3. Step 3

### After Review

Post-merge procedures.

## Standards

### What to Look For

| Area | Check For |
|------|-----------|
| Code Quality | ... |
| Testing | ... |
| Documentation | ... |

### What to Avoid

Common anti-patterns to flag during review.

## Examples

### Good Example

Description of a well-executed review.

### Improvement Opportunity

Description of something that could be improved.

## Sources

- [Engineering Standards](../processed/2024-01-10-notes-engineering-standards.md)
```

### Product/Business Context Article

```markdown
---
type: wiki
topic: Enterprise Authentication Requirements
category: product-business
created: 2024-01-15
updated: 2024-01-15
sources:
  - processed/2024-01-12-notes-product-requirements.md
tags:
  - authentication
  - enterprise
  - requirements
---

# Enterprise Authentication Requirements

## Overview

Business requirements for enterprise customer authentication.

## Background

### Business Context

Why this requirement exists and who it serves.

### Customer Need

What enterprise customers need and why.

## Requirements

### Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| AUTH-001 | Description | Must Have |
| AUTH-002 | Description | Should Have |

### Non-Functional Requirements

- Performance: ...
- Security: ...
- Compliance: ...

## Acceptance Criteria

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Constraints

Limitations or boundaries on implementation.

## Related Features

- [[feature-1]]
- [[feature-2]]

## Sources

- [Product Requirements](../processed/2024-01-12-notes-product-requirements.md)
```

## Guidelines

### Creating Articles

- Use descriptive, specific topic names
- Choose the most appropriate category
- Always include sources with context
- Add related article links when relevant
- Include a History section for tracking changes

### Updating Articles

- Add new sources to the sources list
- Update the `updated` date in frontmatter
- Add an entry to the History section
- Mark new or changed sections
- Preserve attribution for existing content

### Naming Conventions

- Use lowercase with hyphens: `deployment-process.md`
- Be specific: `aws-s3-configuration.md` not `storage.md`
- Avoid abbreviations unless universal: `api-authentication.md` not `auth.md`

### Source Attribution

Always trace content back to its source:

```markdown
## Sources

- [Sprint Planning](../processed/2024-01-15-zoom-sprint.md) - Initial architecture decision
- [Architecture Review](../processed/2024-01-20-zoom-arch.md) - Updated based on feedback
```

### Linking Standards

- Link to related wiki articles: `[Article Name](filename.md)`
- Link to people profiles: `[[firstname-lastname]]`
- Link to source documents: `[Description](../processed/filename.md)`
