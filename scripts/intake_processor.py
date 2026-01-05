#!/usr/bin/env python3
"""
Intake processor for the document pipeline.
Converts .docx files, detects source type, adds metadata, and moves to to-process/
"""

import sys
import os
import re
from pathlib import Path
from datetime import datetime
import shutil

# Import the docx converter
sys.path.insert(0, str(Path(__file__).parent))
from docx_to_markdown import convert_docx_to_markdown


def detect_source_type(content):
    """Detect document source type from content patterns."""
    content_lower = content.lower()

    # Zoom transcript patterns
    zoom_patterns = [
        r'\d{2}:\d{2}:\d{2}',  # Timestamps HH:MM:SS
        r'^\w+\s+\w+:\s',  # Speaker: format
        'you\'re on mute',
        'can you hear me',
        'share my screen',
        'webvtt'
    ]
    zoom_score = sum(1 for pattern in zoom_patterns if re.search(pattern, content_lower, re.MULTILINE))

    # Slack patterns
    slack_patterns = [
        r'\d{1,2}:\d{2}\s*[AP]M',  # Time format
        r'#[\w-]+',  # Channel references
        r'@[\w-]+',  # User mentions
        'slack',
        'replied to a thread',
        r':\w+:',  # Emoji patterns
    ]
    slack_score = sum(1 for pattern in slack_patterns if re.search(pattern, content, re.MULTILINE))

    # JIRA patterns
    jira_patterns = [
        r'[A-Z]{2,}-\d+',  # Ticket IDs
        'summary:',
        'description:',
        'acceptance criteria',
        'story points',
        'sprint',
        'in progress',
        'to do',
        'done',
        'blocked'
    ]
    jira_score = sum(1 for pattern in jira_patterns if re.search(pattern, content_lower, re.MULTILINE))

    # Email patterns
    email_patterns = [
        r'^from:',
        r'^to:',
        r'^subject:',
        r'^date:',
        r'^sent:',
        r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b',  # Email addresses
        r'^re:',
        r'^fwd:',
        'best regards',
        'sincerely',
    ]
    email_score = sum(1 for pattern in email_patterns if re.search(pattern, content_lower, re.MULTILINE))

    # Meeting notes patterns
    meeting_patterns = [
        'agenda',
        'attendees',
        'minutes',
        'action items',
        'meeting notes',
        'next steps',
        'decisions',
        'discussion'
    ]
    meeting_score = sum(1 for pattern in meeting_patterns if re.search(pattern, content_lower, re.MULTILINE))

    # Confluence/Wiki patterns
    wiki_patterns = [
        'confluence',
        'table of contents',
        'wiki',
        r'^\s*={3,}',  # Wiki-style headers
        'page information',
        'space'
    ]
    wiki_score = sum(1 for pattern in wiki_patterns if re.search(pattern, content_lower, re.MULTILINE))

    # Determine source type based on scores
    scores = {
        'zoom': zoom_score,
        'slack': slack_score,
        'jira': jira_score,
        'email': email_score,
        'meeting': meeting_score,
        'wiki': wiki_score
    }

    max_score = max(scores.values())
    if max_score >= 3:
        source = max(scores, key=scores.get)
        confidence = 'high' if max_score >= 5 else 'medium'
        return source, confidence
    elif max_score >= 1:
        source = max(scores, key=scores.get)
        return source, 'low'
    else:
        return 'notes', 'low'


def extract_date_from_content(content):
    """Try to extract a date from document content."""
    # Common date patterns
    patterns = [
        r'\b(\d{4})-(\d{2})-(\d{2})\b',  # YYYY-MM-DD
        r'\b(\d{1,2})/(\d{1,2})/(\d{4})\b',  # MM/DD/YYYY or DD/MM/YYYY
        r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+(\d{1,2}),?\s+(\d{4})\b',  # Month DD, YYYY
    ]

    for pattern in patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            try:
                groups = match.groups()
                if len(groups) == 3 and groups[0].isdigit() and len(groups[0]) == 4:
                    # YYYY-MM-DD format
                    return f"{groups[0]}-{groups[1]}-{groups[2]}"
                elif len(groups) == 3 and groups[2].isdigit() and len(groups[2]) == 4:
                    # Month name format
                    month_map = {
                        'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04',
                        'may': '05', 'jun': '06', 'jul': '07', 'aug': '08',
                        'sep': '09', 'oct': '10', 'nov': '11', 'dec': '12'
                    }
                    month = month_map.get(groups[0][:3].lower())
                    if month:
                        day = groups[1].zfill(2)
                        return f"{groups[2]}-{month}-{day}"
            except:
                pass

    return None


def extract_date_from_filename(filename):
    """Try to extract a date from filename."""
    # Look for YYYY-MM-DD pattern
    match = re.search(r'(\d{4})-(\d{2})-(\d{2})', filename)
    if match:
        return f"{match.group(1)}-{match.group(2)}-{match.group(3)}"

    # Look for YYYY-MM-DD at start
    match = re.match(r'^(\d{4})-(\d{2})-(\d{2})', filename)
    if match:
        return f"{match.group(1)}-{match.group(2)}-{match.group(3)}"

    return None


def extract_participants(content, source):
    """Extract participants based on source type."""
    participants = []

    if source == 'zoom':
        # Look for speaker patterns
        matches = re.findall(r'^([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*:', content, re.MULTILINE)
        participants = list(set(matches))

    elif source == 'slack':
        # Look for @mentions
        matches = re.findall(r'@([\w-]+)', content)
        participants = list(set(matches))

    elif source in ['email', 'meeting']:
        # Look for From/To/Attendees
        for line in content.split('\n')[:20]:  # Check first 20 lines
            if re.match(r'^(from|to|attendees):', line.lower()):
                # Extract names
                names = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+\b', line)
                participants.extend(names)

    return list(set(participants))[:10]  # Limit to 10


def generate_short_description(content, filename, source):
    """Generate a short description for the filename."""
    # Try to extract from filename first
    name_parts = Path(filename).stem.split()

    # Remove date patterns
    filtered_parts = []
    for part in name_parts:
        if not re.match(r'^\d{4}(-\d{2}){0,2}$', part):
            filtered_parts.append(part)

    if filtered_parts:
        desc = '-'.join(filtered_parts[:5])  # Max 5 words
        desc = re.sub(r'[^\w-]', '', desc.lower())
        if len(desc) > 50:
            desc = desc[:50]
        return desc

    # Fall back to content
    lines = content.split('\n')
    for line in lines:
        line = line.strip()
        if line and len(line) > 5:
            # Clean and truncate
            desc = re.sub(r'[^\w\s-]', '', line.lower())
            desc = '-'.join(desc.split()[:5])
            if len(desc) > 50:
                desc = desc[:50]
            return desc

    return 'document'


def process_file(input_path, project_dir):
    """Process a single file through intake."""
    print(f"Processing: {input_path.name}")

    # Convert docx to markdown if needed
    if input_path.suffix.lower() == '.docx':
        try:
            content = convert_docx_to_markdown(input_path)
        except Exception as e:
            print(f"  Error converting {input_path.name}: {e}")
            return None
    else:
        # Read as text
        try:
            content = input_path.read_text(encoding='utf-8')
        except Exception as e:
            print(f"  Error reading {input_path.name}: {e}")
            return None

    # Detect source type
    source, confidence = detect_source_type(content)

    # Extract date
    doc_date = extract_date_from_filename(input_path.name)
    if not doc_date:
        doc_date = extract_date_from_content(content)
    if not doc_date:
        doc_date = datetime.fromtimestamp(input_path.stat().st_mtime).strftime('%Y-%m-%d')

    # Extract participants
    participants = extract_participants(content, source)

    # Generate short description
    short_desc = generate_short_description(content, input_path.name, source)

    # Generate new filename
    new_filename = f"{doc_date}-{source}-{short_desc}.md"

    # Create output with frontmatter
    frontmatter = f"""---
source: {source}
original_filename: {input_path.name}
intake_date: {datetime.now().strftime('%Y-%m-%d')}
document_date: {doc_date}
status: pending
participants:
{chr(10).join(f'  - {p}' for p in participants) if participants else '  []'}
tags: []
source_confidence: {confidence}
---

{content}
"""

    # Write to to-process
    output_path = project_dir / 'to-process' / new_filename

    # Handle duplicates
    counter = 1
    while output_path.exists():
        stem = output_path.stem
        new_filename = f"{stem}-{counter}.md"
        output_path = project_dir / 'to-process' / new_filename
        counter += 1

    try:
        output_path.write_text(frontmatter, encoding='utf-8')
    except Exception as e:
        print(f"  Error writing {output_path.name}: {e}")
        return None

    print(f"  → {output_path.name} ({source}, {confidence} confidence)")

    return {
        'original': input_path.name,
        'new': output_path.name,
        'source': source,
        'confidence': confidence
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 intake_processor.py <project_dir> [file_pattern]")
        sys.exit(1)

    project_dir = Path(sys.argv[1]).expanduser()
    raw_dir = project_dir / 'raw'

    if not raw_dir.exists():
        print(f"Error: raw/ directory not found in {project_dir}")
        sys.exit(1)

    # Get files to process
    if len(sys.argv) >= 3:
        pattern = sys.argv[2]
        files = list(raw_dir.glob(pattern))
    else:
        files = [f for f in raw_dir.iterdir() if f.is_file()]

    if not files:
        print("No files to process in raw/")
        return

    print(f"\nIntake Processing")
    print(f"=================")
    print(f"Files to process: {len(files)}\n")

    results = []
    for file_path in sorted(files):
        result = process_file(file_path, project_dir)
        if result:
            results.append(result)

    print(f"\nIntake Complete")
    print(f"===============")
    print(f"Processed: {len(results)} files")

    # Create log entry
    log_dir = project_dir / 'logs'
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / f"intake-{datetime.now().strftime('%Y-%m-%d')}.md"

    log_content = f"## Intake Log - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    log_content += "| Original | New Name | Source | Confidence |\n"
    log_content += "|----------|----------|--------|------------|\n"

    for r in results:
        log_content += f"| {r['original']} | {r['new']} | {r['source']} | {r['confidence']} |\n"

    log_content += "\n"

    # Append to log
    if log_file.exists():
        existing = log_file.read_text()
        log_file.write_text(existing + log_content)
    else:
        log_file.write_text(log_content)

    print(f"\nLog written to: {log_file}")
    print(f"Files moved to: to-process/")


if __name__ == '__main__':
    main()
