#!/usr/bin/env python3
"""
Improved organization with intelligent filtering.
Stage 3 of the document pipeline.
"""

import sys
import os
import re
import yaml
from pathlib import Path
from datetime import datetime
from collections import defaultdict


# Common false positives to filter out (same as processor)
COMMON_WORDS = {
    'am', 'pm', 'jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec',
    'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'from',
    'as', 'is', 'was', 'are', 'were', 'be', 'been', 'being', 'what', 'when', 'where', 'who',
    'why', 'how', 'which', 'a', 'i', 'an', 'ad', 'about', 'above', 'after', 'again', 'against',
    'all', 'also', 'although', 'always', 'another', 'any', 'anything', 'anyone', 'anywhere',
    'around', 'because', 'before', 'behind', 'below', 'between', 'both', 'during', 'each',
    'either', 'enough', 'even', 'every', 'everything', 'everyone', 'everywhere', 'few', 'first',
    'follow', 'following', 'however', 'instead', 'into', 'just', 'last', 'later', 'least', 'less',
    'like', 'many', 'more', 'most', 'much', 'never', 'next', 'now', 'often', 'once', 'one',
    'only', 'other', 'others', 'otherwise', 'our', 'over', 'own', 'same', 'several', 'should',
    'since', 'some', 'something', 'someone', 'somewhere', 'still', 'such', 'than', 'that',
    'their', 'them', 'then', 'there', 'these', 'they', 'this', 'those', 'through', 'too',
    'under', 'unless', 'until', 'very', 'well', 'when', 'where', 'whether', 'while', 'who',
    'whom', 'whose', 'will', 'with', 'within', 'without', 'would', 'your', 'avoid', 'assistance'
}


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


def normalize_name(name):
    """Normalize a person's name for file naming."""
    name = name.strip()
    name = re.sub(r'[^\w\s-]', '', name)
    name = name.lower()
    name = re.sub(r'\s+', '-', name)
    return name


def normalize_term(term):
    """Normalize a term for file naming."""
    term = term.strip()
    term = re.sub(r'[^\w\s-]', '', term)
    term = term.lower()
    term = re.sub(r'\s+', '-', name)
    return term


def is_valid_person(name):
    """Check if a person name is likely valid."""
    if not name or len(name) < 4:
        return False

    normalized = name.lower().strip()

    # Filter out common words
    if normalized in COMMON_WORDS:
        return False

    # Must have at least two parts
    parts = name.split()
    if len(parts) < 2:
        return False

    # Filter out names that start with common words
    if parts[0].lower() in {'and', 'or', 'but', 'the', 'a', 'an', 'as', 'is', 'are', 'was', 'were'}:
        return False

    # Each part should be at least 2 characters
    if any(len(part) < 2 for part in parts):
        return False

    return True


def is_valid_term(term):
    """Check if a term is likely a meaningful definition."""
    if not term or len(term) < 3:
        return False

    normalized = term.lower().strip()

    # Filter out common words
    if normalized in COMMON_WORDS:
        return False

    # Filter out pure numbers or single letters
    if len(term.replace('-', '').replace(' ', '')) < 2:
        return False

    return True


def organize_tasks(extraction_path, kb_dir, stats):
    """Organize task extractions into knowledge/tasks/."""
    frontmatter, body = read_frontmatter(extraction_path)

    if not frontmatter or frontmatter.get('organized'):
        return

    tasks_dir = kb_dir / 'tasks'
    tasks_dir.mkdir(exist_ok=True)

    source_doc = frontmatter.get('source_document', 'unknown')

    # Determine project from filename
    project = 'general'
    filename = extraction_path.name.lower()

    if 'iceberg' in filename:
        project = 'apache-iceberg'
    elif 'medallion' in filename:
        project = 'medallion-architecture'
    elif 'compliance' in filename:
        project = 'compliance'
    elif 'mongo' in filename or 'atlas' in filename:
        project = 'mongodb'

    task_file = tasks_dir / f"{project}-tasks.md"

    if task_file.exists():
        task_fm, task_body = read_frontmatter(task_file)
        if not task_fm:
            task_fm = {'type': 'task-collection', 'project': project, 'created': datetime.now().strftime('%Y-%m-%d')}
            task_body = f"# {project.replace('-', ' ').title()} - Tasks\n\n## Active Tasks\n\n"

        sources = task_fm.get('sources', [])
        if source_doc not in sources:
            sources.append(source_doc)
        task_fm['sources'] = sources
        task_fm['updated'] = datetime.now().strftime('%Y-%m-%d')

        task_count = frontmatter.get('task_count', 0)
        if task_count > 0:
            task_body += f"\n### Tasks from {source_doc}\n"
            task_body += f"**Extracted:** {frontmatter.get('extracted_date')}\n\n"
            task_body += f"{task_count} tasks identified.\n"
            task_body += f"See: [source](../processed/{Path(source_doc).name})\n\n---\n\n"
            stats['tasks_updated'] += 1
    else:
        task_fm = {
            'type': 'task-collection',
            'project': project,
            'created': datetime.now().strftime('%Y-%m-%d'),
            'updated': datetime.now().strftime('%Y-%m-%d'),
            'sources': [source_doc]
        }
        task_count = frontmatter.get('task_count', 0)
        task_body = f"# {project.replace('-', ' ').title()} - Tasks\n\n## Active Tasks\n\n"
        if task_count > 0:
            task_body += f"### Tasks from {source_doc}\n"
            task_body += f"**Extracted:** {frontmatter.get('extracted_date')}\n\n"
            task_body += f"{task_count} tasks identified.\n"
            task_body += f"See: [source](../processed/{Path(source_doc).name})\n\n---\n\n"
        stats['tasks_new'] += 1

    write_frontmatter(task_file, task_fm, task_body)

    frontmatter['organized'] = True
    frontmatter['organized_date'] = datetime.now().strftime('%Y-%m-%d')
    frontmatter['organized_to'] = [f"knowledge/tasks/{task_file.name}"]
    write_frontmatter(extraction_path, frontmatter, body)


def organize_entities(extraction_path, kb_dir, stats):
    """Organize entity extractions with intelligent filtering."""
    frontmatter, body = read_frontmatter(extraction_path)

    if not frontmatter or frontmatter.get('organized'):
        return

    source_doc = frontmatter.get('source_document', 'unknown')
    organized_to = []

    # Extract people (with filtering)
    people_section = re.search(r'## People\n\n(.*?)(?=\n## |\Z)', body, re.DOTALL)
    if people_section:
        people_lines = [line.strip('- ').strip() for line in people_section.group(1).split('\n') if line.strip().startswith('-')]

        people_dir = kb_dir / 'people'
        people_dir.mkdir(exist_ok=True)

        for person in people_lines:
            if not is_valid_person(person):
                continue

            normalized = normalize_name(person)
            person_file = people_dir / f"{normalized}.md"

            if person_file.exists():
                person_fm, person_body = read_frontmatter(person_file)
                if person_fm:
                    sources = person_fm.get('sources', [])
                    if source_doc not in sources:
                        sources.append(source_doc)
                    person_fm['sources'] = sources
                    person_fm['updated'] = datetime.now().strftime('%Y-%m-%d')
                    person_body += f"\n- **{frontmatter.get('extracted_date')}**: Mentioned in [{Path(source_doc).name}](../processed/{Path(source_doc).name})\n"
                    write_frontmatter(person_file, person_fm, person_body)
                    stats['people_updated'] += 1
            else:
                person_fm = {
                    'type': 'person',
                    'created': datetime.now().strftime('%Y-%m-%d'),
                    'updated': datetime.now().strftime('%Y-%m-%d'),
                    'sources': [source_doc]
                }
                person_body = f"# {person}\n\n## Document Mentions\n\n"
                person_body += f"- **{frontmatter.get('extracted_date')}**: First mentioned in [{Path(source_doc).name}](../processed/{Path(source_doc).name})\n"
                write_frontmatter(person_file, person_fm, person_body)
                stats['people_new'] += 1

            organized_to.append(f"knowledge/people/{person_file.name}")

    # Extract terms (with filtering)
    terms_section = re.search(r'## Technical Terms & Acronyms\n\n(.*?)(?=\n## |\Z)', body, re.DOTALL)
    if terms_section:
        terms_lines = [line.strip('- ').strip() for line in terms_section.group(1).split('\n') if line.strip().startswith('-')]

        defs_dir = kb_dir / 'definitions'
        defs_dir.mkdir(exist_ok=True)

        for term in terms_lines:
            if not is_valid_term(term):
                continue

            normalized = normalize_term(term)
            term_file = defs_dir / f"{normalized}.md"

            if term_file.exists():
                term_fm, term_body = read_frontmatter(term_file)
                if term_fm:
                    sources = term_fm.get('sources', [])
                    if source_doc not in sources:
                        sources.append(source_doc)
                    term_fm['sources'] = sources
                    term_fm['updated'] = datetime.now().strftime('%Y-%m-%d')
                    write_frontmatter(term_file, term_fm, term_body)
                    stats['definitions_updated'] += 1
            else:
                term_fm = {
                    'type': 'definition',
                    'term': term,
                    'created': datetime.now().strftime('%Y-%m-%d'),
                    'updated': datetime.now().strftime('%Y-%m-%d'),
                    'sources': [source_doc]
                }
                term_body = f"# {term}\n\n## Definition\n\nTechnical term identified in project documents.\n\n## Sources\n\n"
                term_body += f"- First mentioned: [{Path(source_doc).name}](../processed/{Path(source_doc).name})\n"
                write_frontmatter(term_file, term_fm, term_body)
                stats['definitions_new'] += 1

            organized_to.append(f"knowledge/definitions/{term_file.name}")

    frontmatter['organized'] = True
    frontmatter['organized_date'] = datetime.now().strftime('%Y-%m-%d')
    frontmatter['organized_to'] = organized_to
    write_frontmatter(extraction_path, frontmatter, body)


def organize_summaries(extraction_path, kb_dir, stats):
    """Organize summary extractions into knowledge/project-status/."""
    frontmatter, body = read_frontmatter(extraction_path)

    if not frontmatter or frontmatter.get('organized'):
        return

    source_doc = frontmatter.get('source_document', 'unknown')

    status_dir = kb_dir / 'project-status'
    status_dir.mkdir(exist_ok=True)

    # Extract project from filename
    project = 'general'
    filename = extraction_path.name.lower()

    if 'iceberg' in filename:
        project = 'apache-iceberg'
    elif 'medallion' in filename:
        project = 'medallion-architecture'
    elif 'compliance' in filename:
        project = 'compliance'
    elif 'mongo' in filename or 'atlas' in filename:
        project = 'mongodb-atlas'
    elif 'deployment' in filename or 'prod' in filename:
        project = 'deployment'

    status_file = status_dir / f"{project}-status.md"

    date_match = re.search(r'(\d{4}-\d{2}-\d{2})', source_doc)
    doc_date = date_match.group(1) if date_match else datetime.now().strftime('%Y-%m-%d')

    if status_file.exists():
        status_fm, status_body = read_frontmatter(status_file)
        if not status_fm:
            status_fm = {'type': 'status', 'project': project, 'created': datetime.now().strftime('%Y-%m-%d')}
            status_body = f"# {project.replace('-', ' ').title()} - Status\n\n"

        sources = status_fm.get('sources', [])
        if source_doc not in sources:
            sources.append(source_doc)
        status_fm['sources'] = sources
        status_fm['updated'] = datetime.now().strftime('%Y-%m-%d')

        status_body += f"\n## Update: {doc_date}\n"
        status_body += f"**Source:** [{Path(source_doc).name}](../processed/{Path(source_doc).name})\n\n"
        status_body += "Activity recorded.\n\n---\n\n"

        write_frontmatter(status_file, status_fm, status_body)
        stats['status_updated'] += 1
    else:
        status_fm = {
            'type': 'status',
            'project': project,
            'created': datetime.now().strftime('%Y-%m-%d'),
            'updated': datetime.now().strftime('%Y-%m-%d'),
            'sources': [source_doc]
        }
        status_body = f"# {project.replace('-', ' ').title()} - Status\n\n"
        status_body += f"## Update: {doc_date}\n"
        status_body += f"**Source:** [{Path(source_doc).name}](../processed/{Path(source_doc).name})\n\n"
        status_body += "Initial status entry.\n\n"

        write_frontmatter(status_file, status_fm, status_body)
        stats['status_new'] += 1

    frontmatter['organized'] = True
    frontmatter['organized_date'] = datetime.now().strftime('%Y-%m-%d')
    frontmatter['organized_to'] = [f"knowledge/project-status/{status_file.name}"]
    write_frontmatter(extraction_path, frontmatter, body)


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 organize_extractions_improved.py <project_dir> [filter]")
        sys.exit(1)

    project_dir = Path(sys.argv[1]).expanduser()
    filter_type = sys.argv[2] if len(sys.argv) > 2 else 'all'

    extractions_dir = project_dir / 'extractions'
    kb_dir = project_dir / 'knowledge'

    if not extractions_dir.exists():
        print("Error: extractions/ directory not found")
        sys.exit(1)

    kb_dir.mkdir(exist_ok=True)
    for subdir in ['tasks', 'people', 'definitions', 'project-status', 'wiki', 'jira-drafts']:
        (kb_dir / subdir).mkdir(exist_ok=True)

    files = list(extractions_dir.glob('*.md'))

    if not files:
        print("No extractions to organize")
        return

    print(f"\nOrganizing Extractions (Stage 3 - Improved)")
    print(f"============================================")
    print(f"Extractions to process: {len(files)}\n")

    stats = {
        'tasks_new': 0,
        'tasks_updated': 0,
        'people_new': 0,
        'people_updated': 0,
        'definitions_new': 0,
        'definitions_updated': 0,
        'status_new': 0,
        'status_updated': 0,
        'wiki_new': 0,
        'jira_drafts': 0
    }

    for i, file_path in enumerate(sorted(files), 1):
        if i % 50 == 0:
            print(f"Progress: {i}/{len(files)}")

        try:
            if file_path.name.endswith('-tasks.md') and filter_type in ['all', 'tasks']:
                organize_tasks(file_path, kb_dir, stats)
            elif file_path.name.endswith('-entities.md') and filter_type in ['all', 'people', 'definitions']:
                organize_entities(file_path, kb_dir, stats)
            elif file_path.name.endswith('-summary.md') and filter_type in ['all', 'status', 'wiki']:
                organize_summaries(file_path, kb_dir, stats)
        except Exception as e:
            print(f"  Error organizing {file_path.name}: {e}")

    print(f"\n\nOrganization Complete")
    print(f"=====================\n")

    print(f"Tasks:")
    print(f"- {stats['tasks_new']} new task collections created")
    print(f"- {stats['tasks_updated']} task collections updated")

    print(f"\nPeople:")
    print(f"- {stats['people_new']} new profiles created")
    print(f"- {stats['people_updated']} profiles updated")

    print(f"\nDefinitions:")
    print(f"- {stats['definitions_new']} new terms added")
    print(f"- {stats['definitions_updated']} terms updated")

    print(f"\nProject Status:")
    print(f"- {stats['status_new']} new status files created")
    print(f"- {stats['status_updated']} status files updated")

    # Write log
    log_dir = project_dir / 'logs'
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / f"organize-{datetime.now().strftime('%Y-%m-%d')}.md"

    log_content = f"## Organization Log (Improved) - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    log_content += "| Category | New | Updated |\n"
    log_content += "|----------|-----|----------|\n"
    log_content += f"| Tasks | {stats['tasks_new']} | {stats['tasks_updated']} |\n"
    log_content += f"| People | {stats['people_new']} | {stats['people_updated']} |\n"
    log_content += f"| Definitions | {stats['definitions_new']} | {stats['definitions_updated']} |\n"
    log_content += f"| Project Status | {stats['status_new']} | {stats['status_updated']} |\n\n"

    if log_file.exists():
        existing = log_file.read_text()
        log_file.write_text(existing + "\n" + log_content)
    else:
        log_file.write_text(log_content)

    print(f"\nLog written to: {log_file}")
    print(f"See knowledge/ directory for organized content")


if __name__ == '__main__':
    main()
