#!/usr/bin/env python3
"""
Populate knowledge base with high-confidence extracted entities.
"""

import sys
import re
import yaml
from pathlib import Path
from datetime import datetime


# Final validation - common words that should never be in names
INVALID_WORDS = {
    # Common verbs/words
    'be', 'have', 'do', 'say', 'get', 'make', 'go', 'know', 'take', 'see', 'come',
    'want', 'look', 'use', 'find', 'give', 'tell', 'work', 'call', 'try', 'ask',
    'need', 'feel', 'become', 'leave', 'put', 'mean', 'keep', 'let', 'begin', 'seem',
    'got', 'said', 'went', 'made', 'took', 'came', 'gave', 'told', 'asked',
    've', 're', 'll', 's', 't', 'm', 'd',  # Contractions
    # Common adjectives/adverbs
    'some', 'other', 'new', 'old', 'first', 'last', 'long', 'little', 'own', 'small',
    'good', 'bad', 'high', 'low', 'right', 'left', 'next', 'early', 'late', 'hard',
    'general', 'user', 'full', 'initial', 'current', 'database', 'data', 'stream',
    # Common nouns that aren't names
    'thing', 'time', 'day', 'year', 'way', 'part', 'place', 'case', 'week', 'point',
    'fact', 'group', 'company', 'problem', 'hand', 'side', 'room', 'home', 'world',
    'migration', 'request', 'pull', 'processing', 'catalog', 'goals', 'sentiment',
    'morning', 'afternoon', 'evening', 'night', 'load', 'sync',
    # Filler words
    'yeah', 'okay', 'yes', 'no', 'well', 'just', 'also', 'even', 'now', 'back',
    'still', 'only', 'very', 'really', 'actually', 'basically', 'definitely',
    'tomorrow', 'yesterday', 'today', 'sometimes', 'always', 'never', 'maybe',
    # More false positive patterns
    'daxter', 'purpose', 'topics', 'primary', 'discussed', 'glue',
    'fq', 'of', 'or', 'and', 'the', 'to', 'in', 'for', 'on', 'at', 'with', 'by',
    # Common transcript artifacts
    'lingarajan',  # This is a last name, but it appears without first name
}

# Known first names that can't appear as last names (to detect "FirstName FirstName" patterns)
KNOWN_FIRST_NAMES = {
    'russ', 'phil', 'lokesh', 'zee', 'sunny', 'danyil', 'phuc', 'samer', 'ankit',
    'marc', 'tom', 'michael', 'brian', 'sreehari', 'mubee', 'luke', 'lawrence',
    'poorna', 'rebecca', 'richard', 'yogi', 'raghvendra', 'victoria', 'ryan',
    'jessica', 'david', 'tony', 'zeeshan', 'daniel',
}

# Valid person names to always include (from document analysis)
KNOWN_VALID_PEOPLE = {
    'Russ Goldstein', 'Phil Edie', 'Lokesh Lingarajan', 'Danyil Tymoshuk',
    'Zee Qureshi', 'Zeeshan Qureshi', 'Sunny Pachunuri', 'Michael Kreiner',
    'Sreehari Guntupalli', 'Mubee Ashraf', 'Phuc Tran', 'Marc Reicher',
    'Samer Khatib', 'Luke Raymer', 'Lawrence Lui', 'Ankit Khandelwal',
    'Victoria Chu', 'Brian Mapes', 'Poorna', 'Rebecca', 'Richard', 'Ryan',
    'Jessica', 'David', 'Tony', 'Yogi', 'Raghvendra', 'Michael Burns',
}

# Minimum thresholds
MIN_PERSON_MENTIONS = 50  # Must appear at least this many times
MIN_TERM_MENTIONS = 20    # Must appear at least this many times


def is_valid_person_name(name):
    """Final validation for person names."""
    parts = name.split()

    # Must have exactly 2 parts (first + last)
    if len(parts) != 2:
        return False

    first, last = parts

    # Check each part
    for part in parts:
        # Too short or too long
        if len(part) < 2 or len(part) > 20:
            return False

        # Must start with capital
        if not part[0].isupper():
            return False

        # Must not be in invalid words
        if part.lower() in INVALID_WORDS:
            return False

    # Check for "FirstName FirstName" pattern (two first names)
    if last.lower() in KNOWN_FIRST_NAMES:
        return False

    return True


def normalize_name(name):
    """Normalize a name for file naming."""
    return name.lower().replace(' ', '-').replace('.', '')


def read_extracted_entities(project_dir):
    """Read the extracted entities file."""
    entities_file = project_dir / 'extracted_entities.md'

    if not entities_file.exists():
        print("Error: extracted_entities.md not found. Run smart_entity_extractor.py first.")
        return None, None

    content = entities_file.read_text()

    # Parse people section
    people = {}
    in_people = False
    for line in content.split('\n'):
        if line.startswith('## People'):
            in_people = True
            continue
        if line.startswith('## Technical Terms'):
            in_people = False
            continue

        if in_people and line.startswith('|') and not line.startswith('| Name'):
            parts = [p.strip() for p in line.split('|')[1:-1]]
            if len(parts) >= 3:
                name = parts[0]
                try:
                    count = int(parts[1])
                    name_type = parts[2]
                    people[name] = {'count': count, 'type': name_type}
                except:
                    pass

    # Parse terms section
    terms = {}
    in_terms = False
    for line in content.split('\n'):
        if line.startswith('## Technical Terms'):
            in_terms = True
            continue

        if in_terms and line.startswith('|') and not line.startswith('| Term'):
            parts = [p.strip() for p in line.split('|')[1:-1]]
            if len(parts) >= 4:
                term = parts[0]
                try:
                    count = int(parts[1])
                    term_type = parts[2]
                    definition = parts[3] if len(parts) > 3 else ''
                    terms[term] = {'count': count, 'type': term_type, 'definition': definition}
                except:
                    pass

    return people, terms


def write_person_file(people_dir, name, info):
    """Write a person profile file."""
    filename = normalize_name(name) + '.md'
    filepath = people_dir / filename

    frontmatter = {
        'type': 'person',
        'created': datetime.now().strftime('%Y-%m-%d'),
        'updated': datetime.now().strftime('%Y-%m-%d'),
        'mention_count': info['count']
    }

    content = f"""---
{yaml.dump(frontmatter, default_flow_style=False)}---

# {name}

## Overview

Identified as a team member based on {info['count']} mentions across project documents.

## Document Mentions

- Appears frequently in meeting transcripts and discussions
"""

    filepath.write_text(content)
    return filepath


def write_term_file(defs_dir, term, info):
    """Write a definition file."""
    filename = term.lower().replace(' ', '-').replace('/', '-') + '.md'
    filepath = defs_dir / filename

    definition = info.get('definition', '')

    frontmatter = {
        'type': 'definition',
        'term': term,
        'created': datetime.now().strftime('%Y-%m-%d'),
        'updated': datetime.now().strftime('%Y-%m-%d'),
        'mention_count': info['count'],
        'term_type': info.get('type', 'unknown')
    }

    content = f"""---
{yaml.dump(frontmatter, default_flow_style=False)}---

# {term}

"""

    if definition:
        content += f"**Definition:** {definition}\n\n"

    content += f"""## Overview

Technical term identified from project documents with {info['count']} mentions.

## Type

{info.get('type', 'Unknown').title()}
"""

    filepath.write_text(content)
    return filepath


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 populate_knowledge_base.py <project_dir>")
        sys.exit(1)

    project_dir = Path(sys.argv[1]).expanduser()
    kb_dir = project_dir / 'knowledge'

    print("\nPopulating Knowledge Base")
    print("=========================\n")

    # Read extracted entities
    people, terms = read_extracted_entities(project_dir)

    if people is None:
        sys.exit(1)

    print(f"Found {len(people)} extracted people")
    print(f"Found {len(terms)} extracted terms")

    # Filter people
    valid_people = {}
    for name, info in people.items():
        # Always include known valid people
        if name in KNOWN_VALID_PEOPLE:
            valid_people[name] = info
            continue

        # Check minimum mentions
        if info['count'] < MIN_PERSON_MENTIONS:
            continue

        # Validate name
        if not is_valid_person_name(name):
            continue

        valid_people[name] = info

    # Filter terms
    valid_terms = {}
    for term, info in terms.items():
        # Check minimum mentions
        if info['count'] < MIN_TERM_MENTIONS:
            continue

        valid_terms[term] = info

    print(f"\nHigh-confidence people: {len(valid_people)}")
    print(f"High-confidence terms: {len(valid_terms)}")

    # Create directories
    people_dir = kb_dir / 'people'
    defs_dir = kb_dir / 'definitions'
    people_dir.mkdir(parents=True, exist_ok=True)
    defs_dir.mkdir(parents=True, exist_ok=True)

    # Clear existing files
    for f in people_dir.glob('*.md'):
        f.unlink()
    for f in defs_dir.glob('*.md'):
        f.unlink()

    # Write people files
    print(f"\nWriting people profiles...")
    for name, info in sorted(valid_people.items(), key=lambda x: x[1]['count'], reverse=True):
        write_person_file(people_dir, name, info)
        print(f"  ✓ {name} ({info['count']} mentions)")

    # Write term files
    print(f"\nWriting term definitions...")
    for term, info in sorted(valid_terms.items(), key=lambda x: x[1]['count'], reverse=True):
        write_term_file(defs_dir, term, info)
        definition = info.get('definition', '')
        if definition:
            print(f"  ✓ {term} ({info['count']}x) = {definition[:50]}...")
        else:
            print(f"  ✓ {term} ({info['count']}x)")

    # Summary
    print(f"\n\nKnowledge Base Populated")
    print(f"========================")
    print(f"People profiles: {len(valid_people)}")
    print(f"Term definitions: {len(valid_terms)}")
    print(f"\nFiles written to:")
    print(f"  - {people_dir}")
    print(f"  - {defs_dir}")


if __name__ == '__main__':
    main()
