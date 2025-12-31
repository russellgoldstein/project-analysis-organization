# Definition Entry Template

Use this template when creating or updating definition entries in `knowledge/definitions/`.

## Definition File

File location: `knowledge/definitions/<term>.md` (lowercase, hyphens for spaces)

```markdown
---
type: definition
term: Term Name
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources:
  - processed/source1.md
  - processed/source2.md
aliases:
  - Alias1
  - Alias2
tags:
  - category1
  - category2
---

# Term Name

**Also known as:** Alias1, Alias2, Abbreviation

**Type:** Acronym / Concept / Tool / Process / System

## Definition

Clear, concise definition of the term. Should be understandable without additional context.

## Expanded Definition

More detailed explanation if needed:

- Key aspect 1
- Key aspect 2
- Key aspect 3

## Context in Project

How this term is used specifically in this project:

> "Quote showing usage in context"
> — Source document

## Examples

**Example 1:** Description of example

**Example 2:** Description of example

## Related Terms

- [[related-term-1]] - How it relates
- [[related-term-2]] - How it relates
- [[related-term-3]] - How it relates

## Sources

| Date | Document | Context |
|------|----------|---------|
| YYYY-MM-DD | [source.md](../processed/source.md) | First defined |
| YYYY-MM-DD | [source2.md](../processed/source2.md) | Additional context |

## Notes

Any additional notes, caveats, or clarifications.

## History

- YYYY-MM-DD: Created from [source]
- YYYY-MM-DD: Updated with additional context from [source]
```

## Quick Definition (for simple terms)

```markdown
---
type: definition
term: API
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources:
  - processed/source.md
---

# API

**Also known as:** Application Programming Interface

**Type:** Acronym

## Definition

A set of protocols and tools that allows different software applications to communicate with each other.

## Related Terms

- [[rest-api]]
- [[graphql]]
```

## Term Categories

### Acronyms
- Short form: API
- Long form: Application Programming Interface
- Definition: What it means

### Concepts
- Name: Data Mesh
- Category: Architecture pattern
- Definition: What it is and how it works

### Tools/Systems
- Name: Airflow
- Type: Internal/External tool
- Definition: What it does, how it's used

### Processes
- Name: Sprint Planning
- Type: Team process
- Definition: How and when it happens

## Naming Convention

- Use lowercase: `data-mesh.md` not `Data-Mesh.md`
- Use hyphens for spaces: `api-gateway.md` not `api gateway.md`
- Use full terms not abbreviations: `application-programming-interface.md` redirects to `api.md`
- For acronyms, use the acronym: `api.md` not `application-programming-interface.md`
