#!/usr/bin/env python3
"""
LEGACY: Regex-based document processor.

This script uses regex-based extraction which has been superseded by
LLM-based subagents for higher quality extraction.

Primary extraction now uses the /process command with Claude subagents:
- document-analyzer
- task-extractor
- entity-extractor
- meeting-notes-extractor
- wiki-content-extractor

This script is kept as a fallback for:
- Environments without Claude API access
- Bulk processing with cost constraints
- Quick local processing without API calls

For best results, use the /process command instead.
"""

import sys
import os
import re
import yaml
from pathlib import Path
from datetime import datetime
from collections import Counter


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


# Common false positives to filter out
COMMON_WORDS = {
    # Time/date
    'am', 'pm', 'jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec',
    'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday',

    # Common sentence starters
    'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'from',
    'as', 'is', 'was', 'are', 'were', 'be', 'been', 'being',

    # Question words
    'what', 'when', 'where', 'who', 'why', 'how', 'which',

    # Common tech words that aren't acronyms
    'api', 'url', 'uri', 'http', 'https', 'html', 'css', 'xml', 'json',

    # Single/double letters
    'a', 'i', 'an', 'ad', 'am', 'as', 'at', 'be', 'by', 'do', 'go', 'he', 'if', 'in', 'is', 'it',
    'me', 'my', 'no', 'of', 'on', 'or', 'so', 'to', 'up', 'us', 'we',

    # Common non-person capitalized words
    'about', 'above', 'after', 'again', 'against', 'all', 'also', 'although', 'always',
    'another', 'any', 'anything', 'anyone', 'anywhere', 'around', 'because', 'before',
    'behind', 'below', 'between', 'both', 'during', 'each', 'either', 'enough', 'even',
    'every', 'everything', 'everyone', 'everywhere', 'few', 'first', 'follow', 'following',
    'however', 'instead', 'into', 'just', 'last', 'later', 'least', 'less', 'like',
    'many', 'more', 'most', 'much', 'never', 'next', 'now', 'often', 'once', 'one',
    'only', 'other', 'others', 'otherwise', 'our', 'over', 'own', 'same', 'several',
    'should', 'since', 'some', 'something', 'someone', 'somewhere', 'still', 'such',
    'than', 'that', 'their', 'them', 'then', 'there', 'these', 'they', 'this', 'those',
    'through', 'too', 'under', 'unless', 'until', 'very', 'well', 'when', 'where',
    'whether', 'while', 'who', 'whom', 'whose', 'will', 'with', 'within', 'without',
    'would', 'your'
}


def is_valid_person_name(name):
    """Check if a name is likely a real person, not a false positive."""
    if not name or len(name) < 4:
        return False

    # Normalize
    normalized = name.lower().strip()

    # Filter out common false positives
    if normalized in COMMON_WORDS:
        return False

    # Must have at least two parts (first and last name)
    parts = name.split()
    if len(parts) < 2:
        return False

    # Filter out names that start with common words
    if parts[0].lower() in {'and', 'or', 'but', 'the', 'a', 'an', 'as', 'is', 'are', 'was', 'were'}:
        return False

    # Each part should be at least 2 characters
    if any(len(part) < 2 for part in parts):
        return False

    # Each part should start with capital letter
    if not all(part[0].isupper() for part in parts):
        return False

    # Filter out common product/tech names
    tech_terms = {'apache', 'google', 'amazon', 'microsoft', 'github', 'gitlab', 'docker',
                  'kubernetes', 'terraform', 'confluence', 'jira', 'slack'}
    if any(part.lower() in tech_terms for part in parts):
        return False

    return True


def is_valid_acronym(term, context=''):
    """Check if an acronym is meaningful and worth tracking."""
    if not term or len(term) < 3:  # Require at least 3 letters
        return False

    # Must be all uppercase
    if not term.isupper():
        return False

    # Filter out common false positives
    if term.lower() in COMMON_WORDS:
        return False

    # Filter out time indicators
    if term in {'AM', 'PM', 'EST', 'PST', 'CST', 'MST', 'UTC', 'GMT'}:
        return False

    # Filter out month abbreviations
    if term in {'JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'}:
        return False

    # Filter out common HTML/code artifacts
    if term in {'DIV', 'SPAN', 'HTML', 'HEAD', 'BODY', 'META', 'LINK', 'IMG', 'SRC', 'ALT', 'HREF'}:
        return False

    # Filter out single letter repeated
    if len(set(term)) == 1:
        return False

    # Likely valid technical acronyms (common patterns)
    tech_acronyms = {'AWS', 'API', 'SDK', 'CLI', 'REST', 'HTTP', 'HTTPS', 'SQL', 'CRUD',
                     'JSON', 'XML', 'YAML', 'CSV', 'URL', 'URI', 'UUID', 'JWT', 'CORS',
                     'ACID', 'RBAC', 'IAM', 'VPC', 'EC2', 'S3', 'RDS', 'SQS', 'SNS',
                     'CICD', 'ETL', 'ELT', 'OLAP', 'OLTP'}

    if term in tech_acronyms:
        return True

    # If it appears in a definition context, likely valid
    if any(indicator in context.lower() for indicator in ['stands for', 'short for', 'acronym for', 'refers to']):
        return True

    # Otherwise, be conservative
    return False


def extract_people(body):
    """Extract likely person names from document body."""
    # Pattern for person names (First Last or First Middle Last)
    name_pattern = r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)\b'

    # Find all potential names
    potential_names = re.findall(name_pattern, body)

    # Count occurrences
    name_counts = Counter(potential_names)

    # Filter and return only valid names that appear at least twice
    valid_names = []
    for name, count in name_counts.items():
        if is_valid_person_name(name) and count >= 2:
            valid_names.append(name)

    return sorted(valid_names)


def extract_acronyms(body):
    """Extract likely meaningful acronyms from document body."""
    # Pattern for acronyms (3+ uppercase letters)
    acronym_pattern = r'\b([A-Z]{3,})\b'

    # Find all potential acronyms with context
    acronyms = []
    for match in re.finditer(acronym_pattern, body):
        term = match.group(1)
        # Get surrounding context (100 chars before and after)
        start = max(0, match.start() - 100)
        end = min(len(body), match.end() + 100)
        context = body[start:end]

        if is_valid_acronym(term, context):
            acronyms.append(term)

    # Count occurrences
    acronym_counts = Counter(acronyms)

    # Return acronyms that appear at least twice
    return sorted([term for term, count in acronym_counts.items() if count >= 2])


def count_document_stats(body):
    """Improved stats from document body."""
    lines = body.split('\n')
    word_count = len(body.split())

    # Count tasks
    task_indicators = ['todo', 'action item', 'follow up', 'task:', '- [ ]', 'assigned to']
    potential_tasks = sum(1 for line in lines if any(ind in line.lower() for ind in task_indicators))

    # Extract people and acronyms
    people = extract_people(body)
    acronyms = extract_acronyms(body)

    return {
        'word_count': word_count,
        'estimated_tasks': min(potential_tasks, 10),
        'estimated_people': len(people),
        'estimated_definitions': len(acronyms),
        'people_list': people,
        'acronyms_list': acronyms
    }


def create_summary_extraction(doc_path, source_doc_name, stats):
    """Create a summary extraction file."""
    frontmatter, body = read_frontmatter(doc_path)

    title_match = re.search(r'^#\s+(.+)$', body, re.MULTILINE)
    title = title_match.group(1) if title_match else source_doc_name

    paragraphs = [p.strip() for p in body.split('\n\n') if p.strip() and not p.startswith('#')]
    summary_text = paragraphs[0] if paragraphs else "No summary available"

    headings = re.findall(r'^#{2,3}\s+(.+)$', body, re.MULTILINE)
    key_points = headings[:10] if headings else []

    summary_content = f"""---
type: extraction
extraction_type: summary
source_document: to-process/{source_doc_name}
extracted_date: {datetime.now().strftime('%Y-%m-%d')}
---

# Summary: {title}

## Executive Summary
{summary_text[:500]}...

## Key Points
{chr(10).join(f'- {point}' for point in key_points)}

## Document Stats
- Word count: {stats['word_count']}
- People mentioned: {stats['estimated_people']}
- Technical terms: {stats['estimated_definitions']}

## Themes/Tags
{chr(10).join(f'- {tag}' for tag in (frontmatter.get('tags', []) or []))}
"""

    return summary_content


def create_tasks_extraction(doc_path, source_doc_name, stats):
    """Create a tasks extraction file."""
    frontmatter, body = read_frontmatter(doc_path)

    task_patterns = [
        r'(?:TODO|Action Item|Task|Follow[- ]up):\s*(.+)',
        r'-\s*\[\s*\]\s*(.+)',
    ]

    tasks_found = []
    for pattern in task_patterns:
        matches = re.finditer(pattern, body, re.IGNORECASE | re.MULTILINE)
        for match in matches:
            tasks_found.append(match.group(1))

    tasks_content = f"""---
type: extraction
extraction_type: tasks
source_document: to-process/{source_doc_name}
extracted_date: {datetime.now().strftime('%Y-%m-%d')}
task_count: {len(tasks_found)}
---

# Tasks: {source_doc_name}

## Task Summary

Estimated tasks found: {len(tasks_found)}

## Tasks Identified

{chr(10).join(f'{i+1}. {task}' for i, task in enumerate(tasks_found[:20]))}

## Notes

This is an automated extraction. Manual review recommended for accuracy.
"""

    return tasks_content


def create_entities_extraction(doc_path, source_doc_name, stats):
    """Create an entities extraction file with filtered, meaningful entities."""
    frontmatter, body = read_frontmatter(doc_path)

    people = stats['people_list']
    acronyms = stats['acronyms_list']

    entities_content = f"""---
type: extraction
extraction_type: entities
source_document: to-process/{source_doc_name}
extracted_date: {datetime.now().strftime('%Y-%m-%d')}
people_count: {len(people)}
terms_count: {len(acronyms)}
---

# Entities: {source_doc_name}

## People

{chr(10).join(f'- {person}' for person in people) if people else '(No people identified with sufficient confidence)'}

## Technical Terms & Acronyms

{chr(10).join(f'- {term}' for term in acronyms) if acronyms else '(No technical terms identified with sufficient confidence)'}

## Notes

Only entities appearing 2+ times in the document are included to reduce false positives.
This is an automated extraction. Manual review recommended for accuracy.
"""

    return entities_content


def process_document(doc_path, project_dir):
    """Process a single document through Stage 2."""
    frontmatter, body = read_frontmatter(doc_path)

    if not frontmatter:
        print(f"  Warning: {doc_path.name} missing frontmatter, skipping")
        return None

    if frontmatter.get('status') == 'processed':
        return None

    stats = count_document_stats(body)

    base_name = doc_path.stem
    extractions_dir = project_dir / 'extractions'
    extractions_dir.mkdir(exist_ok=True)

    extraction_files = {}

    # Create extractions
    summary_path = extractions_dir / f"{base_name}-summary.md"
    summary_content = create_summary_extraction(doc_path, doc_path.name, stats)
    summary_path.write_text(summary_content, encoding='utf-8')
    extraction_files['summary'] = f"extractions/{summary_path.name}"

    tasks_path = extractions_dir / f"{base_name}-tasks.md"
    tasks_content = create_tasks_extraction(doc_path, doc_path.name, stats)
    tasks_path.write_text(tasks_content, encoding='utf-8')
    extraction_files['tasks'] = f"extractions/{tasks_path.name}"

    entities_path = extractions_dir / f"{base_name}-entities.md"
    entities_content = create_entities_extraction(doc_path, doc_path.name, stats)
    entities_path.write_text(entities_content, encoding='utf-8')
    extraction_files['entities'] = f"extractions/{entities_path.name}"

    # Update frontmatter
    frontmatter['status'] = 'processed'
    frontmatter['processed_date'] = datetime.now().strftime('%Y-%m-%d')
    frontmatter['extracted'] = extraction_files
    frontmatter['task_count'] = stats['estimated_tasks']
    frontmatter['people_count'] = stats['estimated_people']
    frontmatter['definition_count'] = stats['estimated_definitions']

    write_frontmatter(doc_path, frontmatter, body)

    # Move to processed
    processed_dir = project_dir / 'processed'
    processed_dir.mkdir(exist_ok=True)
    dest_path = processed_dir / doc_path.name

    counter = 1
    while dest_path.exists():
        dest_path = processed_dir / f"{doc_path.stem}-{counter}{doc_path.suffix}"
        counter += 1

    doc_path.rename(dest_path)

    return {
        'original': doc_path.name,
        'tasks': stats['estimated_tasks'],
        'people': stats['estimated_people'],
        'definitions': stats['estimated_definitions']
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 process_documents_improved.py <project_dir>")
        sys.exit(1)

    project_dir = Path(sys.argv[1]).expanduser()
    to_process_dir = project_dir / 'to-process'

    if not to_process_dir.exists():
        print(f"Error: to-process/ not found in {project_dir}")
        sys.exit(1)

    files = list(to_process_dir.glob('*.md'))

    if not files:
        print("No files to process in to-process/")
        return

    print(f"\nProcessing Documents (Stage 2 - Improved)")
    print(f"==========================================")
    print(f"Files to process: {len(files)}\n")

    results = []
    errors = []

    for i, file_path in enumerate(sorted(files), 1):
        try:
            if i % 10 == 0:
                print(f"Progress: {i}/{len(files)}")

            result = process_document(file_path, project_dir)
            if result:
                results.append(result)
        except Exception as e:
            errors.append((file_path.name, str(e)))
            print(f"  Error processing {file_path.name}: {e}")

    print(f"\n\nProcessing Complete")
    print(f"===================")
    print(f"Processed: {len(results)} documents")

    if errors:
        print(f"Errors: {len(errors)} documents failed")

    total_tasks = sum(r['tasks'] for r in results)
    total_people = sum(r['people'] for r in results)
    total_defs = sum(r['definitions'] for r in results)

    print(f"\nAggregated Stats:")
    print(f"- Total tasks extracted: {total_tasks}")
    print(f"- Total people identified: {total_people}")
    print(f"- Total definitions found: {total_defs}")

    # Write log
    log_dir = project_dir / 'logs'
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / f"process-{datetime.now().strftime('%Y-%m-%d')}.md"

    log_content = f"## Processing Log (Improved) - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    log_content += "| Document | Tasks | People | Definitions |\n"
    log_content += "|----------|-------|--------|-------------|\n"

    for r in results[:50]:
        log_content += f"| {r['original']} | {r['tasks']} | {r['people']} | {r['definitions']} |\n"

    if len(results) > 50:
        log_content += f"\n... and {len(results) - 50} more documents\n"

    log_content += f"\n**Total:** {len(results)} documents processed\n"
    log_content += f"**Errors:** {len(errors)} documents failed\n\n"

    if errors:
        log_content += "### Errors\n\n"
        for filename, error in errors:
            log_content += f"- {filename}: {error}\n"

    if log_file.exists():
        existing = log_file.read_text()
        log_file.write_text(existing + "\n" + log_content)
    else:
        log_file.write_text(log_content)

    print(f"\nLog written to: {log_file}")
    print(f"Extractions written to: extractions/")
    print(f"Documents moved to: processed/")


if __name__ == '__main__':
    main()
