#!/usr/bin/env python3
"""
Aggressively clean up bad extractions (meaningless people/definitions).
"""

import sys
import re
from pathlib import Path


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
    'whom', 'whose', 'will', 'with', 'within', 'without', 'would', 'your', 'avoid', 'assistance',
    'based', 'using', 'according', 'including', 'regarding', 'concerning', 'following',
    'anything', 'everything', 'nothing', 'something'
}

# Known tech/product names (not people)
TECH_TERMS = {
    'apache', 'kafka', 'spark', 'hudi', 'iceberg', 'parquet', 'avro', 'orc',
    'aws', 'azure', 'google', 'amazon', 'microsoft', 'oracle', 'ibm',
    'docker', 'kubernetes', 'terraform', 'ansible', 'jenkins',
    'github', 'gitlab', 'bitbucket', 'jira', 'confluence', 'slack',
    'python', 'java', 'scala', 'javascript', 'typescript',
    'mongodb', 'postgres', 'mysql', 'redis', 'cassandra',
    'atlas', 'stream', 'processing', 'federation', 'app'
}

# Common non-person patterns
NON_PERSON_PATTERNS = [
    r'.*-layer$',
    r'.*-architecture$',
    r'.*-strategy$',
    r'.*-principles?$',
    r'.*-overview$',
    r'.*-request$',
    r'.*-streaming$',
    r'.*-processing$',
    r'.*-federation$',
    r'.*-pattern$',
    r'.*-model$',
    r'.*-framework$',
    r'.*-system$',
    r'.*-service$',
    r'.*-process$',
    r'.*-workflow$',
    r'.*-pipeline$',
    r'.*-deployment$',
    r'.*-configuration$',
    r'.*-implementation$',
    r'.*-infrastructure$',
    r'.*-management$',
    r'.*-optimization$',
    r'.*-hardening$',
    r'.*-branching$',
    r'.*-batching$',
    r'.*-parsing$',
]


def is_likely_real_person(filename):
    """Strict check if a filename represents a real person."""
    stem = filename.stem.lower()

    # Filter common words
    if stem in COMMON_WORDS:
        return False

    # Filter if contains tech terms
    parts = stem.split('-')
    if any(part in TECH_TERMS for part in parts):
        return False

    # Filter if matches non-person patterns
    if any(re.match(pattern, stem) for pattern in NON_PERSON_PATTERNS):
        return False

    # Filter sentence fragments with conjunctions/articles
    if any(f'-{word}-' in stem or stem.startswith(f'{word}-') or stem.endswith(f'-{word}')
           for word in ['and', 'or', 'but', 'the', 'a', 'an', 'as', 'is', 'are', 'was', 'were', 'of', 'to', 'for']):
        return False

    # Must have at least 2 parts (first and last name)
    if len(parts) < 2:
        return False

    # Filter if any part is less than 2 chars
    if any(len(part) < 2 for part in parts):
        return False

    # Filter phrases that are clearly not names
    phrases = [
        'anything', 'everything', 'nothing', 'something',
        'anyone', 'everyone', 'someone',
        'assistance', 'request', 'overview', 'architecture',
        'avoid', 'based', 'using'
    ]
    if any(phrase in parts for phrase in phrases):
        return False

    return True


def is_likely_real_term(filename):
    """Strict check if a filename represents a real technical term."""
    stem = filename.stem.lower()

    # Filter common words
    if stem in COMMON_WORDS:
        return False

    # Less than 3 characters (too short for meaningful term)
    if len(stem.replace('-', '')) < 3:
        return False

    # Filter random 2-3 letter combinations (likely false positives)
    if len(stem) <= 3 and stem not in ['api', 'aws', 's3', 'ec2', 'rds', 'sql', 'etl', 'elt', 'jwt', 'url', 'uri', 'sdk', 'cli', 'iam', 'vpc']:
        return False

    # Known good terms (whitelist)
    known_good = {
        'api', 'aws', 's3', 'ec2', 'rds', 'sqs', 'sns', 'iam', 'vpc',
        'sql', 'nosql', 'crud', 'rest', 'http', 'https', 'json', 'xml', 'yaml', 'csv',
        'etl', 'elt', 'olap', 'oltp', 'acid', 'rbac', 'jwt', 'cors',
        'sdk', 'cli', 'cicd', 'uuid', 'uri', 'url',
        'apache-iceberg', 'apache-kafka', 'apache-spark',
        'mongodb', 'postgres', 'mysql', 'redis', 'cassandra'
    }

    if stem in known_good:
        return True

    # Filter obvious false positives (random letter combinations)
    # If it's 3 chars and not in whitelist, likely bad
    if len(stem) == 3:
        return False

    return True


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 cleanup_bad_extractions_aggressive.py <project_dir>")
        sys.exit(1)

    project_dir = Path(sys.argv[1]).expanduser()
    kb_dir = project_dir / 'knowledge'

    if not kb_dir.exists():
        print("Error: knowledge/ directory not found")
        sys.exit(1)

    print("\nAggressive Cleanup of Bad Extractions")
    print("======================================\n")

    # Clean up people
    people_dir = kb_dir / 'people'
    if people_dir.exists():
        people_files = list(people_dir.glob('*.md'))
        bad_people = [f for f in people_files if not is_likely_real_person(f)]

        print(f"People profiles: {len(people_files)} total")
        print(f"  - Keeping (likely real people): {len(people_files) - len(bad_people)}")
        print(f"  - Removing (not people): {len(bad_people)}")

        if bad_people:
            for f in bad_people:
                f.unlink()
            print(f"  ✓ Removed {len(bad_people)} non-person files")

    # Clean up definitions
    defs_dir = kb_dir / 'definitions'
    if defs_dir.exists():
        def_files = list(defs_dir.glob('*.md'))
        bad_defs = [f for f in def_files if not is_likely_real_term(f)]

        print(f"\nDefinitions: {len(def_files)} total")
        print(f"  - Keeping (likely real terms): {len(def_files) - len(bad_defs)}")
        print(f"  - Removing (not meaningful terms): {len(bad_defs)}")

        if bad_defs:
            for f in bad_defs:
                f.unlink()
            print(f"  ✓ Removed {len(bad_defs)} meaningless definition files")

    # Summary
    print(f"\n\nCleanup Complete")
    print(f"================")
    people_removed = len(bad_people) if 'bad_people' in locals() else 0
    defs_removed = len(bad_defs) if 'bad_defs' in locals() else 0

    print(f"Removed: {people_removed} people files")
    print(f"Removed: {defs_removed} definition files")

    # Show remaining
    people_remaining = len(list(people_dir.glob('*.md'))) if people_dir.exists() else 0
    defs_remaining = len(list(defs_dir.glob('*.md'))) if defs_dir.exists() else 0

    print(f"\nFinal Count:")
    print(f"  - People profiles: {people_remaining}")
    print(f"  - Definitions: {defs_remaining}")

    # Show samples
    if people_remaining > 0:
        print(f"\nSample people (first 10):")
        for f in sorted(people_dir.glob('*.md'))[:10]:
            # Convert filename back to display name
            display = f.stem.replace('-', ' ').title()
            print(f"  - {display}")

    if defs_remaining > 0:
        print(f"\nSample definitions (first 10):")
        for f in sorted(defs_dir.glob('*.md'))[:10]:
            print(f"  - {f.stem}")


if __name__ == '__main__':
    main()
