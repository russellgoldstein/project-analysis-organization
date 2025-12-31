# JIRA Draft Template

Use this template for draft JIRA tickets in `knowledge/jira-drafts/`.

## JIRA Draft File

File location: `knowledge/jira-drafts/draft-<brief-title>.md`

```markdown
---
type: jira-draft
created: YYYY-MM-DD
source_document: processed/2024-01-15-zoom-sprint-review.md
suggested_project: PROJ
suggested_type: Story
priority: High
status: draft
---

# [Draft] Implement User Authentication

## Ticket Information

| Field | Value |
|-------|-------|
| **Project** | PROJ (suggested) |
| **Type** | Story / Bug / Task / Epic |
| **Priority** | High / Medium / Low |
| **Suggested Assignee** | John Smith |
| **Sprint** | Current / Next / Backlog |
| **Story Points** | 5 (estimated) |
| **Labels** | auth, security, backend |

## Summary

One-line summary suitable for JIRA ticket title:

> Implement OAuth2-based user authentication system

## Description

### Background

Explain why this work is needed:

The current system lacks proper user authentication. Users are requesting secure login functionality to protect their data.

### Requirements

What needs to be done:

- Implement OAuth2 authentication flow
- Support Google and GitHub as identity providers
- Create secure session management
- Add login/logout UI components

### Technical Notes

Any technical context or constraints:

- Must integrate with existing user service
- Use JWT for session tokens
- Consider rate limiting for auth endpoints

## Acceptance Criteria

Checkboxes for definition of done:

- [ ] User can log in with Google OAuth
- [ ] User can log in with GitHub OAuth
- [ ] User session persists across browser refresh
- [ ] User can log out and session is invalidated
- [ ] Failed login attempts are rate-limited
- [ ] All auth endpoints have appropriate error handling
- [ ] Unit tests cover auth flow
- [ ] Documentation updated

## Dependencies

| Type | Item | Status |
|------|------|--------|
| Blocked by | User service API ready | Done |
| Blocks | User profile feature | Waiting |
| Related to | PROJ-123 | Reference |

## Source Context

Where this ticket idea came from:

**Document:** [sprint-review.md](../processed/2024-01-15-zoom-sprint-review.md)

**Original Discussion:**
> "We really need to add proper authentication. Users have been asking for it, and it's a blocker for the profile features. John, can you take this on?"
> — Jane Doe, Sprint Review

**Additional Context:**
- Discussed during sprint planning on 2024-01-15
- John Smith volunteered to lead implementation
- Estimated as 1-week effort

## Open Questions

Questions to resolve before creating ticket:

- [ ] Which OAuth providers are must-have vs nice-to-have?
- [ ] Do we need password-based auth as well?
- [ ] What's the deadline for this feature?

---

## Creation Checklist

Before creating in JIRA:

- [ ] Summary is clear and specific
- [ ] Description provides enough context
- [ ] Acceptance criteria are testable
- [ ] Dependencies are identified
- [ ] Open questions resolved
- [ ] Assignee confirmed
- [ ] Priority validated
- [ ] Sprint/timeline determined

## After Creation

Once created in JIRA:

**JIRA Ticket:** PROJ-XXX
**Created:** YYYY-MM-DD
**Created By:** Your Name

Update this file or delete after ticket is created.
```

## Quick JIRA Draft

For simpler tickets:

```markdown
---
type: jira-draft
created: YYYY-MM-DD
source_document: processed/source.md
suggested_project: PROJ
suggested_type: Bug
priority: Medium
status: draft
---

# [Draft] Fix Login Page Redirect Issue

## Summary

> Login page redirects to wrong URL after successful authentication

## Type & Priority

| Field | Value |
|-------|-------|
| Type | Bug |
| Priority | Medium |
| Assignee | Unassigned |

## Description

After successful login, users are redirected to `/dashboard` instead of the page they were trying to access.

## Acceptance Criteria

- [ ] User is redirected to original requested URL after login
- [ ] If no original URL, redirect to default dashboard
- [ ] Edge cases handled (expired sessions, deep links)

## Source

> "The login redirect is broken again"
> — From Slack #bugs channel

---

- [ ] Ready to create
```

## Bug Report Template

```markdown
---
type: jira-draft
created: YYYY-MM-DD
source_document: processed/source.md
suggested_project: PROJ
suggested_type: Bug
priority: High
status: draft
---

# [Draft] [Bug] Description of Issue

## Summary

> Clear one-line bug description

## Bug Details

| Field | Value |
|-------|-------|
| Type | Bug |
| Priority | High |
| Severity | Major |
| Environment | Production |
| Affected Users | All |

## Steps to Reproduce

1. Step one
2. Step two
3. Step three

## Expected Behavior

What should happen.

## Actual Behavior

What actually happens.

## Screenshots/Logs

[Include any relevant screenshots or error logs]

## Possible Cause

[If known, include possible cause]

## Suggested Fix

[If known, include suggested fix]

---

- [ ] Ready to create
```

## Ticket Type Guidelines

### Story
- User-facing feature
- Has clear user value
- Can be demoed

### Bug
- Something is broken
- Regression from expected behavior
- User-reported issue

### Task
- Technical work
- Refactoring
- Infrastructure changes

### Epic
- Large feature spanning multiple stories
- Theme of work
- Quarter-level initiative
