# Person Profile Template

Use this template when creating or updating person profiles in `knowledge/people/`.

## Person Profile File

File location: `knowledge/people/<firstname>-<lastname>.md` (lowercase)

```markdown
---
type: person
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources:
  - processed/source1.md
  - processed/source2.md
name_variations:
  - John
  - John S.
  - John Smith
  - jsmith
  - @john.smith
---

# John Smith

## Basic Info

| Field | Value | Confidence | Source |
|-------|-------|------------|--------|
| **Full Name** | John Smith | High | Multiple sources |
| **Role** | Senior Engineer | High | sprint-review.md |
| **Team** | Platform Team | High | team-sync.md |
| **Department** | Engineering | Medium | Inferred |
| **Location** | San Francisco | Low | Single mention |
| **Email** | john.smith@company.com | High | email.md |

## Expertise Areas

Areas of knowledge or specialization:

| Area | Evidence | Confidence |
|------|----------|------------|
| Backend Systems | Presented architecture review | High |
| API Design | Led API redesign initiative | High |
| Python | Mentioned as primary language | Medium |
| Data Pipelines | Discussed in context | Low |

## Responsibilities

Current responsibilities and duties:

- Lead technical design for Project Alpha
- Code review for platform services
- On-call rotation for data pipeline
- Mentoring junior engineers

## Active Projects

| Project | Role | Since | Status |
|---------|------|-------|--------|
| Project Alpha | Tech Lead | 2024-01 | Active |
| API Gateway | Contributor | 2023-10 | Active |
| Legacy Migration | Advisor | 2024-02 | Planning |

## Document Mentions

Chronological list of appearances in documents:

| Date | Document | Context |
|------|----------|---------|
| 2024-01-15 | [sprint-review.md](../processed/2024-01-15-zoom-sprint-review.md) | Led sprint review |
| 2024-01-10 | [team-sync.md](../processed/2024-01-10-zoom-team-sync.md) | Migration update |
| 2024-01-05 | [1-on-1.md](../processed/2024-01-05-notes-1on1.md) | Quarterly goals |

## Working Relationships

| Relationship | Person | Context |
|--------------|--------|---------|
| Works with | [[jane-doe]] | Same project team |
| Reports to | [[bob-wilson]] | Manager |
| Mentors | [[alex-chen]] | Junior on team |
| Collaborates | [[sarah-kim]] | API design partner |

## Communication Preferences

Notes about communication style or preferences (if known):

- Prefers async communication via Slack
- Usually available mornings (PT)
- Responsive in #platform channel

## Notes

Additional context or observations:

- Joined company in 2022
- Previously worked at [Company X]
- Known for thorough code reviews

## Historical Information

Past roles or team memberships:

| Period | Role | Team |
|--------|------|------|
| 2022-06 to 2023-06 | Engineer | Mobile Team |
| 2023-06 to present | Senior Engineer | Platform Team |

## Updates Log

- YYYY-MM-DD: Profile created from [source]
- YYYY-MM-DD: Added expertise area from [source]
- YYYY-MM-DD: Updated role from [source]
```

## Minimal Profile

For people with limited information:

```markdown
---
type: person
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources:
  - processed/source.md
name_variations:
  - Bob
needs_review: true
---

# Bob Wilson

## Basic Info

| Field | Value | Confidence |
|-------|-------|------------|
| **Name** | Bob Wilson | Medium |
| **Role** | Manager | Low |
| **Team** | Unknown | - |

## Document Mentions

| Date | Document | Context |
|------|----------|---------|
| 2024-01-15 | source.md | Mentioned as manager |

## Review Needed

- Full name confirmation needed
- Role needs verification
- Team affiliation unknown
```

## Guidelines

### Creating Profiles

- Create profile when person is mentioned with context
- Don't create for single passing mentions
- Include source for every piece of information
- Mark confidence levels appropriately

### Updating Profiles

- Add new sources to sources list
- Update confidence when evidence strengthens
- Add new document mentions
- Keep history of changes

### Name Handling

- Use full name as filename when known
- Track all name variations in frontmatter
- Handle name conflicts by adding context
