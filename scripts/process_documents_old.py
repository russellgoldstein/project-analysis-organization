#!/usr/bin/env python3
"""
Process documents from to-process/ and create extraction files.
Stage 2 of the document pipeline.
"""

import sys
import os
import re
import yaml
from pathlib import Path
from datetime import datetime
from collections import defaultdict


def read_frontmatter(file_path):
    """Extract YAML frontmatter from markdown file."""
    content = file_path.read_text(encoding='utf-8')

    # Check for frontmatter
    if not content.startswith('---'):
        return None, content

    # Find end of frontmatter
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


def count_document_stats(body):
    """Quick stats from document body."""
    lines = body.split('\n')
    word_count = len(body.split())

    # Count potential tasks (lines starting with action verbs or containing "TODO", "ACTION", etc.)
    task_indicators = ['todo', 'action item', 'follow up', 'task:', '- [ ]', 'assigned to']
    potential_tasks = sum(1 for line in lines if any(ind in line.lower() for ind in task_indicators))

    # Count people mentions (capitalized names)
    people_pattern = r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+\b'
    people_matches = re.findall(people_pattern, body)
    unique_people = len(set(people_matches))

    # Count definitions/acronyms
    definition_patterns = [
        r'\b[A-Z]{2,}\b',  # Acronyms
        r'is defined as',
        r'refers to',
        r'means that'
    ]
    potential_definitions = sum(1 for pattern in definition_patterns for match in re.finditer(pattern, body))

    return {
        'word_count': word_count,
        'estimated_tasks': min(potential_tasks, 10),  # Cap at 10
        'estimated_people': unique_people,
        'estimated_definitions': min(potential_definitions, 5)
    }


def create_summary_extraction(doc_path, source_doc_name, stats):
    """Create a summary extraction file (simplified version without LLM)."""
    frontmatter, body = read_frontmatter(doc_path)

    # Extract title
    title_match = re.search(r'^#\s+(.+)$', body, re.MULTILINE)
    title = title_match.group(1) if title_match else source_doc_name

    # Extract first few paragraphs for summary
    paragraphs = [p.strip() for p in body.split('\n\n') if p.strip() and not p.startswith('#')]
    summary_text = paragraphs[0] if paragraphs else "No summary available"

    # Extract headings as key points
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
- Estimated tasks: {stats['estimated_tasks']}
- Estimated people mentioned: {stats['estimated_people']}

## Themes/Tags
{chr(10).join(f'- {tag}' for tag in (frontmatter.get('tags', []) or []))}
"""

    return summary_content


def create_tasks_extraction(doc_path, source_doc_name, stats):
    """Create a tasks extraction file (simplified version)."""
    frontmatter, body = read_frontmatter(doc_path)

    # Find task-like patterns
    task_patterns = [
        r'(?:TODO|Action Item|Task|Follow[- ]up):\s*(.+)',
        r'-\s*\[\s*\]\s*(.+)',  # Markdown checkboxes
        r'assigned to\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
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
    """Create an entities extraction file (simplified version)."""
    frontmatter, body = read_frontmatter(doc_path)

    # Extract people (capitalized names)
    people_pattern = r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+\b'
    people = list(set(re.findall(people_pattern, body)))[:20]

    # Extract acronyms
    acronym_pattern = r'\b[A-Z]{2,}\b'
    acronyms = list(set(re.findall(acronym_pattern, body)))[:20]

    entities_content = f"""---
type: extraction
extraction_type: entities
source_document: to-process/{source_doc_name}
extracted_date: {datetime.now().strftime('%Y-%m-%d')}
---

# Entities: {source_doc_name}

## People

{chr(10).join(f'- {person}' for person in people)}

## Terms & Acronyms

{chr(10).join(f'- {term}' for term in acronyms)}

## Notes

This is an automated extraction. Manual review recommended for accuracy.
"""

    return entities_content


def process_document(doc_path, project_dir):
    """Process a single document through Stage 2."""
    frontmatter, body = read_frontmatter(doc_path)

    if not frontmatter:
        print(f"  Warning: {doc_path.name} missing frontmatter, skipping")
        return None

    # Check if already processed
    if frontmatter.get('status') == 'processed':
        return None

    # Get stats
    stats = count_document_stats(body)

    # Create extraction files
    base_name = doc_path.stem
    extractions_dir = project_dir / 'extractions'
    extractions_dir.mkdir(exist_ok=True)

    extraction_files = {}

    # Summary
    summary_path = extractions_dir / f"{base_name}-summary.md"
    summary_content = create_summary_extraction(doc_path, doc_path.name, stats)
    summary_path.write_text(summary_content, encoding='utf-8')
    extraction_files['summary'] = f"extractions/{summary_path.name}"

    # Tasks
    tasks_path = extractions_dir / f"{base_name}-tasks.md"
    tasks_content = create_tasks_extraction(doc_path, doc_path.name, stats)
    tasks_path.write_text(tasks_content, encoding='utf-8')
    extraction_files['tasks'] = f"extractions/{tasks_path.name}"

    # Entities
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

    # Write updated document
    write_frontmatter(doc_path, frontmatter, body)

    # Move to processed
    processed_dir = project_dir / 'processed'
    processed_dir.mkdir(exist_ok=True)
    dest_path = processed_dir / doc_path.name

    # Handle duplicates
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
        print("Usage: python3 process_documents.py <project_dir>")
        sys.exit(1)

    project_dir = Path(sys.argv[1]).expanduser()
    to_process_dir = project_dir / 'to-process'

    if not to_process_dir.exists():
        print(f"Error: to-process/ not found in {project_dir}")
        sys.exit(1)

    # Get files
    files = list(to_process_dir.glob('*.md'))

    if not files:
        print("No files to process in to-process/")
        return

    print(f"\nProcessing Documents (Stage 2)")
    print(f"==============================")
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

    # Summary
    print(f"\n\nProcessing Complete")
    print(f"===================")
    print(f"Processed: {len(results)} documents")

    if errors:
        print(f"Errors: {len(errors)} documents failed")

    # Aggregate stats
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

    log_content = f"## Processing Log - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    log_content += "| Document | Tasks | People | Definitions |\n"
    log_content += "|----------|-------|--------|-------------|\n"

    for r in results[:50]:  # Log first 50
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
