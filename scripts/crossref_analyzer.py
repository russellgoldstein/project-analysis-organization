#!/usr/bin/env python3
"""
Cross-reference processed documents with knowledge base.
Stage 4 of the document pipeline.
"""

import sys
import os
import re
import yaml
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict


def read_frontmatter(file_path):
    """Extract YAML frontmatter from markdown file."""
    content = file_path.read_text(encoding='utf-8')

    if not content.startswith('---'):
        return None, content

    end_match = re.search(r'\n---\n', content[3:])
    if not end_match:
        return None, content

    frontmatter_text = content[3:end_match.start() + 3]
    body = content[end_match.end() + 3:]

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
        return frontmatter, body
    except:
        return None, content


def write_frontmatter(file_path, frontmatter, body):
    """Write markdown file with YAML frontmatter."""
    frontmatter_text = yaml.dump(frontmatter, default_flow_style=False, sort_keys=False)
    content = f"---\n{frontmatter_text}---\n\n{body}"
    file_path.write_text(content, encoding='utf-8')


def analyze_document_relationships(doc_path, kb_dir):
    """Analyze relationships between document and knowledge base."""
    frontmatter, body = read_frontmatter(doc_path)

    if not frontmatter:
        return None

    relationships = {
        'people_mentioned': [],
        'terms_used': [],
        'projects_related': [],
        'potential_updates': []
    }

    # Extract people from document
    people_pattern = r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+\b'
    people_in_doc = set(re.findall(people_pattern, body))

    # Check against knowledge base people
    people_dir = kb_dir / 'people'
    if people_dir.exists():
        kb_people = {f.stem.replace('-', ' ').title() for f in people_dir.glob('*.md')}
        relationships['people_mentioned'] = list(people_in_doc & kb_people)

    # Extract acronyms/terms from document
    acronym_pattern = r'\b[A-Z]{2,}\b'
    terms_in_doc = set(re.findall(acronym_pattern, body))

    # Check against knowledge base definitions
    defs_dir = kb_dir / 'definitions'
    if defs_dir.exists():
        kb_terms = {f.stem.replace('-', ' ').upper() for f in defs_dir.glob('*.md')}
        relationships['terms_used'] = list(terms_in_doc & kb_terms)

    # Identify projects from filename/content
    filename = doc_path.name.lower()
    projects = []
    if 'iceberg' in filename:
        projects.append('apache-iceberg')
    if 'medallion' in filename:
        projects.append('medallion-architecture')
    if 'compliance' in filename:
        projects.append('compliance')
    if 'mongo' in filename or 'atlas' in filename:
        projects.append('mongodb-atlas')
    if 'deployment' in filename:
        projects.append('deployment')

    relationships['projects_related'] = projects

    return relationships


def generate_update_proposal(proposal_id, target_file, change_type, source_doc, confidence, rationale, evidence):
    """Generate a proposed update document."""
    proposal = f"""---
type: proposed-update
proposal_id: {proposal_id}
created: {datetime.now().strftime('%Y-%m-%d')}
target_file: {target_file}
change_type: {change_type}
source_document: {source_doc}
confidence: {confidence}
status: pending_review
---

# Proposed Update: {change_type.replace('-', ' ').title()}

## Target

**File:** {target_file}

## Change Type

`{change_type}` - {rationale}

## Source Evidence

**Document:** {source_doc}

{evidence}

## Confidence

**{confidence.title()}** - Based on analysis of document content.

---

## Review Actions

- [ ] Approve and apply
- [ ] Modify and apply
- [ ] Reject
- [ ] Defer

**Reviewer Notes:**
_Add notes here when reviewing_
"""
    return proposal


def crossref_document(doc_path, kb_dir, proposals_dir, proposal_counter, stats):
    """Cross-reference a single document with knowledge base."""
    frontmatter, body = read_frontmatter(doc_path)

    if not frontmatter:
        return proposal_counter

    # Skip if already cross-referenced
    if frontmatter.get('crossref_date'):
        return proposal_counter

    # Analyze relationships
    relationships = analyze_document_relationships(doc_path, kb_dir)

    if not relationships:
        return proposal_counter

    # Track proposals for this document
    doc_proposals = []

    # Check for potential updates based on relationships
    if relationships['people_mentioned']:
        # Propose update to people profiles
        for person in relationships['people_mentioned'][:3]:  # Limit to 3
            proposal_id = f"update-{proposal_counter:03d}"
            proposal_counter += 1

            person_file = f"knowledge/people/{person.lower().replace(' ', '-')}.md"
            rationale = f"New mention of {person} in recent document"
            evidence = f"Person mentioned in context of: {doc_path.name}"

            proposal_content = generate_update_proposal(
                proposal_id,
                person_file,
                'mention-update',
                f"processed/{doc_path.name}",
                'medium',
                rationale,
                evidence
            )

            proposal_path = proposals_dir / f"{proposal_id}-person-{person.lower().replace(' ', '-')}.md"
            proposal_path.write_text(proposal_content, encoding='utf-8')
            doc_proposals.append(f"proposed-updates/{proposal_path.name}")
            stats['proposals_created'] += 1

    if relationships['projects_related']:
        # Propose update to project status
        for project in relationships['projects_related'][:2]:  # Limit to 2
            proposal_id = f"update-{proposal_counter:03d}"
            proposal_counter += 1

            status_file = f"knowledge/project-status/{project}-status.md"
            rationale = f"New activity for project {project}"
            evidence = f"Document contains discussion about {project}"

            proposal_content = generate_update_proposal(
                proposal_id,
                status_file,
                'status-update',
                f"processed/{doc_path.name}",
                'high',
                rationale,
                evidence
            )

            proposal_path = proposals_dir / f"{proposal_id}-status-{project}.md"
            proposal_path.write_text(proposal_content, encoding='utf-8')
            doc_proposals.append(f"proposed-updates/{proposal_path.name}")
            stats['proposals_created'] += 1

    # Mark document as cross-referenced
    frontmatter['crossref_date'] = datetime.now().strftime('%Y-%m-%d')
    frontmatter['crossref_proposals'] = doc_proposals
    write_frontmatter(doc_path, frontmatter, body)

    stats['documents_analyzed'] += 1
    stats['relationships_found'] += len(relationships['people_mentioned']) + len(relationships['terms_used'])

    return proposal_counter


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 crossref_analyzer.py <project_dir> [filter]")
        sys.exit(1)

    project_dir = Path(sys.argv[1]).expanduser()
    filter_arg = sys.argv[2] if len(sys.argv) > 2 else 'today'

    processed_dir = project_dir / 'processed'
    kb_dir = project_dir / 'knowledge'
    proposals_dir = project_dir / 'proposed-updates'

    if not processed_dir.exists():
        print("Error: processed/ directory not found")
        sys.exit(1)

    if not kb_dir.exists():
        print("Error: knowledge/ directory not found")
        sys.exit(1)

    proposals_dir.mkdir(exist_ok=True)

    # Get documents to analyze
    files = list(processed_dir.glob('*.md'))

    if filter_arg == 'today':
        # Filter to documents processed today
        today = datetime.now().date()
        files = [f for f in files if datetime.fromtimestamp(f.stat().st_mtime).date() == today]

    if not files:
        print("No documents to cross-reference")
        return

    # Count existing proposals to continue numbering
    existing_proposals = list(proposals_dir.glob('update-*.md'))
    proposal_counter = len(existing_proposals) + 1

    print(f"\nCross-Reference Analysis (Stage 4)")
    print(f"==================================")
    print(f"Documents to analyze: {len(files)}")
    print(f"Existing proposals: {len(existing_proposals)}\n")

    stats = {
        'documents_analyzed': 0,
        'proposals_created': 0,
        'relationships_found': 0,
        'contradictions_found': 0
    }

    # Process each document
    for i, doc_path in enumerate(sorted(files), 1):
        if i % 25 == 0:
            print(f"Progress: {i}/{len(files)}")

        try:
            proposal_counter = crossref_document(doc_path, kb_dir, proposals_dir, proposal_counter, stats)
        except Exception as e:
            print(f"  Error analyzing {doc_path.name}: {e}")

    print(f"\n\nCross-Reference Complete")
    print(f"========================\n")

    print(f"Documents Analyzed: {stats['documents_analyzed']}")
    print(f"Relationships Found: {stats['relationships_found']}")
    print(f"Update Proposals Created: {stats['proposals_created']}")

    if stats['contradictions_found'] > 0:
        print(f"Contradictions Found: {stats['contradictions_found']}")

    # Generate summary report
    summary_file = proposals_dir / f"_summary-{datetime.now().strftime('%Y-%m-%d')}.md"

    summary_content = f"""# Cross-Reference Summary

**Analysis Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Documents Analyzed:** {stats['documents_analyzed']}
**Knowledge Base Entries Scanned:** Multiple directories

## Findings Overview

| Category | Count |
|----------|-------|
| Documents Analyzed | {stats['documents_analyzed']} |
| Relationships Found | {stats['relationships_found']} |
| Update Proposals | {stats['proposals_created']} |
| Contradictions | {stats['contradictions_found']} |

## Proposed Updates

Total proposals created: {stats['proposals_created']}

See individual proposal files in this directory for details.

## Review Process

1. Review each `update-NNN-*.md` file
2. Check the evidence and rationale
3. Mark your decision in the "Review Actions" checklist
4. Use `/review <proposal-id>` to apply approved changes

## Important

**NO CHANGES WERE AUTO-APPLIED**

All proposals require manual review before being applied to the knowledge base.
"""

    summary_file.write_text(summary_content, encoding='utf-8')

    # Write log
    log_dir = project_dir / 'logs'
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / f"crossref-{datetime.now().strftime('%Y-%m-%d')}.md"

    log_content = f"## Cross-Reference Log - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    log_content += f"Documents Analyzed: {stats['documents_analyzed']}\n"
    log_content += f"Proposals Generated: {stats['proposals_created']}\n"
    log_content += f"Relationships Found: {stats['relationships_found']}\n"
    log_content += f"Contradictions Found: {stats['contradictions_found']}\n\n"

    if log_file.exists():
        existing = log_file.read_text()
        log_file.write_text(existing + "\n" + log_content)
    else:
        log_file.write_text(log_content)

    print(f"\nSummary written to: {summary_file}")
    print(f"Log written to: {log_file}")
    print(f"\nReview proposals in: proposed-updates/")
    print(f"\n⚠️  IMPORTANT: No changes were auto-applied. Review each proposal before applying.")


if __name__ == '__main__':
    main()
